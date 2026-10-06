from .state import AgentState
from .nodes import chat_agent,supervisor,coding_agent,execute_code,research_agent,planner,rag_agent,reviewer,writer,human_review,advance_agent,multi_agent_start
from .router import supervisor_router,code_execution_router,human_review_router,multi_agent_router,multi_agent_next_router,agent_completion_router
from langgraph.graph import StateGraph , START, END
from langgraph.checkpoint.memory import InMemorySaver


builder=StateGraph(AgentState)
builder.add_node("supervisor",supervisor)
builder.add_node("chat",chat_agent)
builder.add_node("planner",planner)
builder.add_node("research",research_agent)
builder.add_node("rag",rag_agent)
builder.add_node("coding",coding_agent)
builder.add_node("execute_code",execute_code)
builder.add_node("reviewer",reviewer)
builder.add_node("human_review",human_review)
builder.add_node("multi_agent_start",multi_agent_start)
builder.add_node("advance_agent",advance_agent)
builder.add_node("writer",writer)


builder.add_edge(START,"supervisor")
builder.add_edge("supervisor","planner")

builder.add_conditional_edges(
    "planner",
    supervisor_router,
    {
        "chat":"chat",
        "research":"research",
        "rag":"rag",
        "coding":"coding",
        "multi_agent":"multi_agent_start"
    }
)
builder.add_conditional_edges(
    "multi_agent_start",
    multi_agent_router,
    {
        "research":"research",
        "coding":"coding",
        "rag":"rag",
        "done":"reviewer"
    }
)

builder.add_conditional_edges(
    "research",
    agent_completion_router,
    {
        "advance":"advance_agent",
        "reviewer":"reviewer"
    }
)
builder.add_conditional_edges(
    "rag",
    agent_completion_router,
    {
        "advance":"advance_agent",
        "reviewer":"reviewer"
    }
)
builder.add_edge("coding","execute_code")
builder.add_conditional_edges(
    "execute_code",
    code_execution_router,
    {
        "success":"reviewer",
        "retry":"coding",
        "failed":"reviewer",
        "advance":"advance_agent"
    }
)

builder.add_conditional_edges(
    "advance_agent",
    multi_agent_next_router,
    {
        "research":"research",
        "rag":"rag",
        "coding":"coding",
        "done":"reviewer"
    }
)
builder.add_edge("reviewer","human_review")
builder.add_conditional_edges(
    "human_review",
    human_review_router,
    {
        "approve":"writer",
        "revise":"coding"
    }
)

builder.add_edge("chat",END)
builder.add_edge("writer",END)
memory =InMemorySaver()
graph=builder.compile(checkpointer=memory)
