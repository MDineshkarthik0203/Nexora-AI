import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from .tools.web_search import web_search,format_search_results
from .tools.rag import (retrieve_and_rerank,format_documents)
from .tools.code_execution import execute_python_code
from langgraph.types import interrupt

from .state import AgentState

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv()


class LazyChatGroq:
    """Lazy wrapper for ChatGroq that initializes only when invoked."""

    def __init__(self):
        self._llm = None

    def _get_llm(self):
        if self._llm is None:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError(
                    "GROQ_API_KEY is not set. Please add GROQ_API_KEY to your .env file."
                )
            model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
            self._llm = ChatGroq(
                model=model,
                temperature=0,
                groq_api_key=api_key,
            )
        return self._llm

    def invoke(self, *args, **kwargs):
        return self._get_llm().invoke(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._get_llm(), name)


llm = LazyChatGroq()


def chat_agent(state: AgentState):
    """
    Handles simple conversational messages that do not
    require research, RAG, coding, or multi-agent execution.
    """

    question = state["question"]

    prompt = f"""
You are AgentForge, an AI engineering copilot.

The user sent a simple conversational message.

USER:
{question}

Respond naturally and briefly.

If the user is greeting you, greet them back and
offer help with technical work such as:

- Research
- Private knowledge/RAG
- Python programming
- Debugging
- AI/ML
- Agentic AI
- LangGraph
- Backend development

Do not perform web research.
Do not invent sources.
Do not generate unnecessary technical content.

Return only the conversational response.
"""

    response = llm.invoke(prompt)

    return {
        "final_answer": response.content.strip()
    }


def supervisor(state: AgentState):

    question = state["question"]

    prompt = f"""
You are the supervisor of AgentForge,
a multi-agent AI engineering system.

Your job is to classify the user's request.

AVAILABLE ROUTES:

CHAT
Use this when the user is having simple conversation,
such as:

- hi
- hello
- hey
- good morning
- good evening
- thanks
- thank you
- bye
- simple conversational questions
- casual conversation

Do NOT use research for simple greetings.

RESEARCH
Use this when the user wants:

- Technical research
- Explanations of concepts
- Current information
- Web research
- Comparisons
- Literature research

RAG
Use this when the user explicitly asks about:

- Private documents
- Uploaded documents
- Internal company knowledge
- Local knowledge base

CODING
Use this when the user wants:

- Write code
- Generate code
- Debug code
- Fix programming errors
- Implement an algorithm
- Build a software feature

MULTI_AGENT
Use this when the request clearly requires multiple
specialized capabilities such as:

- Research + coding
- Research + private knowledge
- RAG + coding
- Research + RAG + coding

USER REQUEST:

{question}

You MUST return exactly this format:

ROUTE: chat

REASON: The user is having a simple conversation.

The ROUTE must be exactly ONE of:

ROUTE: chat
ROUTE: research
ROUTE: rag
ROUTE: coding
ROUTE: multi_agent

Do not return any other route.
"""

    response = llm.invoke(prompt)

    output = response.content.strip()

    route = "research"

    if "ROUTE: multi_agent" in output:
        route = "multi_agent"

    elif "ROUTE: rag" in output:
        route = "rag"

    elif "ROUTE: coding" in output:
        route = "coding"

    elif "ROUTE: chat" in output:
        route = "chat"

    elif "ROUTE: research" in output:
        route = "research"

    reason = ""

    if "REASON:" in output:
        reason = output.split(
            "REASON:",
            1
        )[1].strip()

    return {
        "route": route,
        "supervisor_reason": reason
    }


def planner(state: AgentState):

    question = state["question"]

    route = state.get(
        "route",
        "research"
    )

    if route == "chat":

        return {
            "plan": [
                "Handle the conversation directly"
            ],
            "agent_plan": [
                "chat"
            ],
            "current_agent_index": 0
        }

    # -----------------------------------------
    # existing planner code below
    # -----------------------------------------

    prompt = f"""
You are the Planning Agent of AgentForge.

USER REQUEST:
{question}

SUPERVISOR ROUTE:
{route}

Available specialized agents:

1. research
   - Web research
   - Current technical information
   - Technical analysis

2. rag
   - Private AgentForge knowledge
   - Internal documents
   - Local knowledge base

3. coding
   - Python programming
   - Code generation
   - Debugging
   - Implementation

Your job is to determine which specialized agents
are required to solve the user's request.

If the supervisor route is not multi_agent,
select only the corresponding specialized agent.

If the supervisor route is multi_agent,
select all agents that are genuinely necessary.

Return exactly:

PLAN:
1. ...

AGENTS:
research
rag
coding

Do not include unnecessary agents.
"""

    response = llm.invoke(prompt)

    output = response.content.strip()

    plan = []

    in_plan = False

    for line in output.splitlines():

        line = line.strip()

        if line == "PLAN:":
            in_plan = True
            continue

        if line == "AGENTS:":
            in_plan = False
            continue

        if in_plan and line:

            cleaned = line.lstrip(
                "0123456789.- "
            ).strip()

            if cleaned:
                plan.append(cleaned)

    agent_plan = []

    in_agents = False

    for line in output.splitlines():

        line = line.strip().lower()

        if line == "agents:":
            in_agents = True
            continue

        if in_agents:

            if line in [
                "research",
                "rag",
                "coding"
            ]:

                if line not in agent_plan:
                    agent_plan.append(line)

    if not agent_plan:

        if route == "coding":
            agent_plan = ["coding"]

        elif route == "rag":
            agent_plan = ["rag"]

        else:
            agent_plan = ["research"]

    return {
        "plan": plan,
        "agent_plan": agent_plan,
        "current_agent_index": 0
    }

def research_agent(state: AgentState):

    question = state["question"]

    # 1. Search the web
    raw_results = web_search(question)

    # 2. Format results for the LLM
    search_results = format_search_results(raw_results)

    # 3. Extract real URLs
    sources = []

    for result in raw_results.get("results", []):

        url = result.get("url", "")

        if url:
            sources.append(url)

    # 4. Ask LLM to summarize ONLY the provided evidence
    prompt = f"""
You are the Research Agent of AgentForge.

User question:

{question}

WEB SEARCH RESULTS:

{search_results}

Your job is to create a technical research summary.

IMPORTANT RULES:

1. Use ONLY information contained in the web search results.
2. Do NOT invent facts.
3. Do NOT invent papers.
4. Do NOT invent URLs.
5. Do NOT create citations that are not present in the search results.
6. If the search results are insufficient, explicitly say:
   "The available search results are insufficient."
7. Clearly distinguish facts from interpretation.
8. Keep the answer technically accurate.

Return:

RESEARCH SUMMARY:
<your summary>

EVIDENCE:
<important evidence from the search results>
"""

    response = llm.invoke(prompt)

    return {
        "research": response.content,
        "search_results": search_results,
        "sources": sources
    }


def rag_agent(state: AgentState):

    question = state["question"]

    research = state.get(
        "research",
        ""
    )

    print(
        "\n[RAG AGENT] Searching private knowledge base..."
    )

    documents = retrieve_and_rerank(
        query=question,
        retrieval_k=10,
        top_k=3
    )

    print(
        f"[RAG AGENT] Retrieved {len(documents)} documents."
    )

    context = format_documents(documents)

    if not documents:

        return {
            "rag_context": (
                "No relevant information was found "
                "in the private knowledge base."
            )
        }

    prompt = f"""
You are the RAG Agent of AgentForge.

USER QUESTION:

{question}


RESEARCH AGENT FINDINGS:

{research}


PRIVATE KNOWLEDGE BASE:

{context}


Your task is to analyze the private knowledge
in relation to the user's question.

Use the Research Agent findings only as
additional context.

Rules:

1. Use the private knowledge base as the
   primary source for private/internal information.

2. Do not invent information.

3. Do not use outside knowledge.

4. If the private knowledge is insufficient,
   clearly say so.

5. Explain how the private knowledge relates
   to the research findings when appropriate.

6. Do not create fake sources.

Return a clear technical analysis.
"""

    response = llm.invoke(prompt)

    return {
        "rag_context": response.content
    }


def coding_agent(state: AgentState):

    question = state["question"]

    research = state.get(
        "research",
        ""
    )

    rag_context = state.get(
        "rag_context",
        ""
    )

    previous_code = state.get(
        "code",
        ""
    )

    previous_error = state.get(
        "code_execution_error",
        ""
    )

    human_feedback = state.get(
        "human_feedback",
        ""
    )

    attempt = state.get(
        "code_attempts",
        0
    )

    prompt = f"""
You are the Coding Agent of AgentForge.

USER REQUEST:

{question}


RESEARCH AGENT FINDINGS:

{research}


RAG AGENT FINDINGS:

{rag_context}


PREVIOUS CODE:

{previous_code}


PREVIOUS EXECUTION ERROR:

{previous_error}


HUMAN REVIEW FEEDBACK:

{human_feedback}


CURRENT ATTEMPT:

{attempt}


Your task is to create the implementation
required by the user.

Use the Research and RAG findings as context.

Rules:

1. Generate correct Python code.

2. Follow the user's requirements.

3. Use relevant information from the Research Agent.

4. Use relevant private knowledge from the RAG Agent.

5. If previous code failed, fix the error.

6. If human feedback exists, apply it.

7. Do not invent requirements.

8. Do not use interactive input() unless the
   user explicitly requests it.

9. Make the code executable automatically.

10. Keep the implementation readable.

11. Return ONLY executable Python code.

Do not use markdown code fences.
"""

    response = llm.invoke(prompt)

    code = response.content.strip()

    # Remove markdown fences

    if code.startswith("```python"):

        code = code[len("```python"):].strip()

    elif code.startswith("```"):

        code = code[3:].strip()

    if code.endswith("```"):

        code = code[:-3].strip()

    return {
        "code": code,
        "code_attempts": attempt + 1,
        "code_execution_error": "",
        "code_execution_output": "",
        "code_execution_success": False
    }


def execute_code(state:AgentState):
    code=state.get("code","")
    result=execute_python_code(code)
    if result["success"]:
        print("[CODE EXECUTOR] Execution successful")
    else:
        print("[CODE EXECUTOR] Execution Failed")
    return {
        "code_execution_success":result["success"],
        "code_execution_output":result["output"],
        "code_execution_error":result["error"]
    }

def multi_agent_start(state: AgentState):

    agent_plan = state.get(
        "agent_plan",
        []
    )

    print(
        "\n[MULTI-AGENT] Execution plan:"
    )

    for index, agent in enumerate(
        agent_plan,
        start=1
    ):

        print(
            f"{index}. {agent}"
        )

    return {
        "current_agent_index": 0,
        "agent_current_index": 0,
        "is_multi_agent": True
    }

def advance_agent(state: AgentState):
    current_index = state.get("current_agent_index", state.get("agent_current_index", 0))
    next_index = current_index + 1
    return {
        "current_agent_index": next_index,
        "agent_current_index": next_index
    }


def reviewer(state: AgentState):

    question = state["question"]

    research = state.get(
        "research",
        ""
    )

    rag_context = state.get(
        "rag_context",
        ""
    )

    code = state.get(
        "code",
        ""
    )

    execution_output = state.get(
        "code_execution_output",
        ""
    )

    execution_error = state.get(
        "code_execution_error",
        ""
    )

    execution_success = state.get(
        "code_execution_success",
        False
    )

    prompt = f"""
You are the technical reviewer of AgentForge.

USER QUESTION:

{question}


RESEARCH:

{research}


RAG:

{rag_context}


CODE:

{code}


CODE EXECUTION SUCCESS:

{execution_success}


CODE EXECUTION OUTPUT:

{execution_output}


CODE EXECUTION ERROR:

{execution_error}


Review the result.

Check:

1. Technical correctness
2. Code correctness
3. Execution result
4. Missing information
5. Unsupported claims
6. Clarity

If the code executed successfully and the
solution is technically correct, return:

STATUS: PASS

Otherwise return:

STATUS: REVISE
"""

    response = llm.invoke(prompt)

    review = response.content.strip()

    if "STATUS: PASS" in review:

        status = "pass"

    else:

        status = "revise"

    return {
        "review": review,
        "review_status": status
    }

def human_review(state: AgentState):

    print("\n[HUMAN REVIEW] Waiting for human approval...")

    question = state.get(
        "question",
        ""
    )

    review = state.get(
        "review",
        ""
    )

    code = state.get(
        "code",
        ""
    )

    execution_output = state.get(
        "code_execution_output",
        ""
    )

    request = {
        "message": "Please review the agent result.",

        "question": question,

        "review": review,

        "code": code,

        "execution_output": execution_output,

        "options": [
            "approve",
            "revise"
        ]
    }

    decision = interrupt(request)

    print(
        f"[HUMAN REVIEW] Decision: {decision}"
    )



    if isinstance(decision, dict):

        action = decision.get(
            "action",
            "revise"
        )

        feedback = decision.get(
            "feedback",
            ""
        )

        return {
            "human_decision": action,
            "human_feedback": feedback
        }


    return {
        "human_decision": str(decision),
        "human_feedback": ""
    }

def writer(state: AgentState):

    question = state["question"]

    research = state.get(
        "research",
        ""
    )

    rag_context = state.get(
        "rag_context",
        ""
    )

    code = state.get(
        "code",
        ""
    )

    execution_output = state.get(
        "code_execution_output",
        ""
    )

    execution_error = state.get(
        "code_execution_error",
        ""
    )

    review = state.get(
        "review",
        ""
    )

    prompt = f"""
You are the final report writer of AgentForge.

USER QUESTION:

{question}


RESEARCH:

{research}


PRIVATE KNOWLEDGE:

{rag_context}


CODE:

{code}


EXECUTION OUTPUT:

{execution_output}


EXECUTION ERROR:

{execution_error}


REVIEW:

{review}


Create the final answer.

Rules:

1. Use the available evidence.
2. Do not invent facts.
3. If code was executed successfully,
   explain the result.
4. If execution failed after maximum retries,
   clearly mention the failure.
5. Keep the answer technically accurate.

Use:

# Summary

# Explanation

# Implementation

# Verification
"""

    response = llm.invoke(prompt)

    return {
        "final_answer": response.content
    }