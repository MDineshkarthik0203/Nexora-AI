from .state import AgentState

def supervisor_router(state:AgentState):
    route=state.get("route","research")
    if route == "chat":
        return "chat"
    if route == "research":
        return "research"
    if route =="coding":
        return "coding"
    if route =="rag":
        return "rag"
    if route == "multi_agent":
        return "multi_agent"
    return "research"

def code_execution_router(state:AgentState):
    success=state.get("code_execution_success",False)
    attempts=state.get("code_attempts",0)

    if success:
        if state.get("is_multi_agent",False):
            return "advance"
        return "success"
    if attempts<3:
        return "retry"
    return "failed"

def human_review_router(state: AgentState):

    decision = state.get(
        "human_decision",
        ""
    )

    print(
        f"[HUMAN ROUTER] Decision = {decision}"
    )

    if decision == "approve":

        return "approve"

    return "revise"


def multi_agent_router(state: AgentState):
    agent_plan = state.get("agent_plan", [])
    current_index = state.get("current_agent_index", state.get("agent_current_index", 0))

    if not agent_plan:
        return "research"
    if current_index is None or current_index >= len(agent_plan):
        return "done"
    current_agent = agent_plan[current_index]
    if current_agent == "research":
        return "research"
    if current_agent == "rag":
        return "rag"
    if current_agent == "coding":
        return "coding"
    return "research"

def multi_agent_next_router(state: AgentState):
    agent_plan = state.get("agent_plan", [])
    current_index = state.get("current_agent_index", state.get("agent_current_index", 0))

    if not agent_plan or current_index is None or current_index >= len(agent_plan):
        return "done"
    next_agent = agent_plan[current_index]
    if next_agent == "research":
        return "research"
    if next_agent == "rag":
        return "rag"
    if next_agent == "coding":
        return "coding"
    return "done"

    
def agent_completion_router(state: AgentState):

    if state.get(
        "is_multi_agent",
        False
    ):

        return "advance"

    return "reviewer"