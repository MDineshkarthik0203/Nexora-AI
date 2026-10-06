from agentforge.tools.rag import ingest_documents


if __name__ == "__main__":

    count = ingest_documents("data")

    print(
        f"\nIndexed chunks: {count}"
    )