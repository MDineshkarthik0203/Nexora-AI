import sys
import uuid
from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================
#
# AgentForge/
# ├── src/
# │   └── agentforge/
# └── backend/
#     └── api/
#         └── services.py
#
# We need to add AgentForge/src to Python's import path so
# Django can import the existing LangGraph application.
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv()

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


# Import your EXISTING LangGraph graph.
from agentforge.graph import graph

from langgraph.types import Command


def create_session_id():
    """Create a unique session ID for a new AgentForge request."""
    return f"agentforge-{uuid.uuid4()}"


def get_graph_config(session_id: str):
    """
    LangGraph uses thread_id to persist/resume graph state.

    The same session_id MUST be used when:
        1. Starting the graph
        2. Resuming after Human-in-the-Loop
    """
    return {
        "configurable": {
            "thread_id": session_id,
        }
    }


def get_interrupt_data(result):
    """
    Read LangGraph interrupt information.

    When human_review() calls interrupt(...), graph.invoke()
    returns a state containing __interrupt__.
    """

    interrupts = result.get("__interrupt__", [])

    if not interrupts:
        return None

    interrupt_value = interrupts[0].value

    if isinstance(interrupt_value, dict):
        return interrupt_value

    return {
        "message": str(interrupt_value),
    }


def serialize_result(result, session_id):
    """
    Convert LangGraph state into a JSON-safe Django response.
    """

    interrupt_data = get_interrupt_data(result)

    # --------------------------------------------------------
    # HUMAN REVIEW REQUIRED
    # --------------------------------------------------------

    if interrupt_data:
        return {
            "success": True,
            "requires_human_review": True,
            "session_id": session_id,

            "message": interrupt_data.get(
                "message",
                "Human review is required.",
            ),

            "review": {
                "question": interrupt_data.get(
                    "question",
                    result.get("question", ""),
                ),

                "review": interrupt_data.get(
                    "review",
                    result.get("review", ""),
                ),

                "code": interrupt_data.get(
                    "code",
                    result.get("code", ""),
                ),

                "execution_output": interrupt_data.get(
                    "execution_output",
                    result.get(
                        "code_execution_output",
                        "",
                    ),
                ),

                "options": interrupt_data.get(
                    "options",
                    ["approve", "revise"],
                ),

                "route": result.get(
                    "route",
                    "",
                ),
            },

            "final_answer": "",

            "state": {
                "route": result.get(
                    "route",
                    "",
                ),

                "plan": result.get(
                    "plan",
                    [],
                ),

                "agent_plan": result.get(
                    "agent_plan",
                    [],
                ),

                "current_agent_index": result.get(
                    "current_agent_index",
                    0,
                ),

                "review": result.get(
                    "review",
                    "",
                ),

                "review_status": result.get(
                    "review_status",
                    "",
                ),

                "code_execution_success": result.get(
                    "code_execution_success",
                    False,
                ),
            },
        }

    # --------------------------------------------------------
    # NORMAL COMPLETION
    # --------------------------------------------------------

    return {
        "success": True,
        "requires_human_review": False,
        "session_id": session_id,
        "message": "AgentForge completed successfully.",

        "review": None,

        "final_answer": result.get(
            "final_answer",
            "",
        ),

        "state": {
            "route": result.get(
                "route",
                "",
            ),

            "plan": result.get(
                "plan",
                [],
            ),

            "agent_plan": result.get(
                "agent_plan",
                [],
            ),

            "research": result.get(
                "research",
                "",
            ),

            "rag_context": result.get(
                "rag_context",
                "",
            ),

            "code": result.get(
                "code",
                "",
            ),

            "review": result.get(
                "review",
                "",
            ),

            "review_status": result.get(
                "review_status",
                "",
            ),

            "code_execution_success": result.get(
                "code_execution_success",
                False,
            ),

            "code_execution_output": result.get(
                "code_execution_output",
                "",
            ),
        },
    }


def run_agent(question: str, session_id: str):
    """
    Start a new AgentForge workflow.
    """

    config = get_graph_config(session_id)

    result = graph.invoke(
        {
            "question": question,
        },
        config=config,
    )

    return serialize_result(
        result,
        session_id,
    )


def resume_agent(
    session_id: str,
    action: str,
    feedback: str = "",
):
    """
    Resume a paused AgentForge workflow.

    Approve:
        {
            "action": "approve",
            "feedback": ""
        }

    Revise:
        {
            "action": "revise",
            "feedback": "Improve the code..."
        }
    """

    config = get_graph_config(session_id)

    human_response = {
        "action": action,
        "feedback": feedback,
    }

    result = graph.invoke(
        Command(
            resume=human_response,
        ),
        config=config,
    )

    return serialize_result(
        result,
        session_id,
    )
