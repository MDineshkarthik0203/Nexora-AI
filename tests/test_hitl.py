from agentforge.graph import graph
from langgraph.types import Command


def main():

    question = """
    Write a Python program to check whether a number is prime.
    """

    config = {
        "configurable": {
            "thread_id": "agentforge-hitl-002"
        }
    }

    # --------------------------------------------------
    # Start the graph
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("STARTING AGENTFORGE")
    print("=" * 70)

    result = graph.invoke(
        {
            "question": question
        },
        config=config
    )

    # --------------------------------------------------
    # Graph should pause at human_review
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("GRAPH PAUSED FOR HUMAN REVIEW")
    print("=" * 70)

    print("\nCurrent state:")

    print(
        "Question:",
        result.get("question")
    )

    print(
        "Route:",
        result.get("route")
    )

    print(
        "Plan:",
        result.get("plan")
    )

    print(
        "\nGenerated Code:\n",
        result.get("code")
    )

    print(
        "\nReviewer:\n",
        result.get("review")
    )


    # --------------------------------------------------
    # Human decision
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("HUMAN REVIEW")
    print("=" * 70)

    decision = input(
        "\nApprove the result? (yes/no): "
    ).strip().lower()


    if decision == "yes":

        human_response = {
            "action": "approve"
        }

    else:

        feedback = input(
            "Enter revision feedback: "
        )

        human_response = {
            "action": "revise",
            "feedback": feedback
        }


    # --------------------------------------------------
    # Resume graph
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("RESUMING AGENTFORGE")
    print("=" * 70)

    final_result = graph.invoke(
        Command(
            resume=human_response
        ),
        config=config
    )


    # --------------------------------------------------
    # Final answer
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("FINAL ANSWER")
    print("=" * 70)

    print(
        final_result.get(
            "final_answer",
            "No final answer generated."
        )
    )


if __name__ == "__main__":
    main()