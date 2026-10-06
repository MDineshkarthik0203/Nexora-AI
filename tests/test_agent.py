from agentforge.graph import graph


def run_test(question):

    print("\n" + "=" * 70)

    print("QUESTION:")
    print(question)

    result = graph.invoke({
        "question": question
    })

    print("\n" + "-" * 70)

    print("SUPERVISOR ROUTE:")
    print(
        result.get("route")
    )

    print("\nSUPERVISOR REASON:")
    print(
        result.get("supervisor_reason")
    )

    print("\nPLAN:")

    for i, step in enumerate(
        result.get("plan", []),
        start=1
    ):
        print(f"{i}. {step}")

    print("\nRAG CONTEXT:")
    print(
        result.get(
            "rag_context",
            ""
        )
    )

    print("\nREVIEW:")
    print(
        result.get(
            "review",
            ""
        )
    )

    print("\nFINAL ANSWER:")
    print(
        result.get(
            "final_answer",
            ""
        )
    )

    print(
        "\n" + "=" * 70
    )


if __name__ == "__main__":

    run_test(
        "Research modern RAG architectures and explain how they can be used in AgentForge. Then use the private AgentForge knowledge base to relate the research to our architecture, and finally write a Python implementation demonstrating the improved RAG approach."
    )