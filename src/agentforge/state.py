from typing import TypedDict


class AgentState(TypedDict, total=False):

    # User request
    question: str

    # Supervisor
    route: str
    supervisor_reason: str

    # Planner
    plan: list[str]
    agent_plan: list[str]
    current_agent_index: int
    agent_current_index: int
    is_multi_agent: bool

    # Agent outputs
    research: str
    search_results: str
    sources: list[str]
    
    rag_context: str
    code: str

    code_execution_success: bool
    code_execution_output: str
    code_execution_error: str
    code_attempts: int

    # Review
    review: str
    review_status: str

    # Human
    human_decision: str
    human_feedback: str

    # Final response
    final_answer: str