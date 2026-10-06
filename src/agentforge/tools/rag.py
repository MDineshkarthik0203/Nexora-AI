# src/agentforge/tools/rag.py

from dotenv import load_dotenv

from langchain_mistralai import MistralAIEmbeddings
from langchain_chroma import Chroma

from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from sentence_transformers import CrossEncoder


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# 1. MISTRAL EMBEDDINGS
# ============================================================

embeddings = MistralAIEmbeddings(
    model="mistral-embed"
)


# ============================================================
# 2. CHROMA VECTOR DATABASE
# ============================================================

vectorstore = Chroma(
    collection_name="agentforge_mistral_rag",
    embedding_function=embeddings,
    persist_directory="chroma_db"
)


# ============================================================
# 3. LOCAL RERANKER
# ============================================================

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


# ============================================================
# 4. DOCUMENT INGESTION
# ============================================================

def ingest_documents(
    data_directory: str = "data"
):

    print("\n" + "=" * 60)
    print("AGENTFORGE RAG - DOCUMENT INGESTION")
    print("=" * 60)

    # --------------------------------------------------------
    # Load documents
    # --------------------------------------------------------

    print("\nLoading documents...")

    loader = DirectoryLoader(
        data_directory,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={
            "encoding": "utf-8"
        }
    )

    documents = loader.load()

    print(
        f"Loaded {len(documents)} documents."
    )

    if not documents:

        print("No documents found.")

        return 0

    # --------------------------------------------------------
    # Split documents into chunks
    # --------------------------------------------------------

    print("\nSplitting documents...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(
        documents
    )

    print(
        f"Created {len(chunks)} chunks."
    )

    # --------------------------------------------------------
    # Add chunks to Chroma
    # --------------------------------------------------------

    print("\nGenerating Mistral embeddings...")

    vectorstore.add_documents(
        chunks
    )

    print(
        "Documents successfully stored in Chroma."
    )

    print("=" * 60)

    return len(chunks)


# ============================================================
# 5. VECTOR RETRIEVAL
# ============================================================

def retrieve_documents(
    query: str,
    k: int = 10
):

    print(
        f"\n[RAG] Retrieving top {k} documents..."
    )

    documents = vectorstore.similarity_search(
        query,
        k=k
    )

    print(
        f"[RAG] Retrieved {len(documents)} documents."
    )

    return documents


# ============================================================
# 6. RERANK DOCUMENTS
# ============================================================

def rerank_documents(
    query: str,
    documents: list,
    top_k: int = 3
):

    if not documents:

        return []

    print(
        "\n[RAG] Reranking documents..."
    )

    # --------------------------------------------------------
    # Create query-document pairs
    # --------------------------------------------------------

    pairs = [
        [
            query,
            document.page_content
        ]
        for document in documents
    ]

    # --------------------------------------------------------
    # Calculate relevance scores
    # --------------------------------------------------------

    scores = reranker.predict(
        pairs
    )

    # --------------------------------------------------------
    # Combine documents with scores
    # --------------------------------------------------------

    ranked_documents = sorted(
        zip(documents, scores),
        key=lambda item: item[1],
        reverse=True
    )

    # --------------------------------------------------------
    # Display scores
    # --------------------------------------------------------

    for rank, (document, score) in enumerate(
        ranked_documents,
        start=1
    ):

        source = document.metadata.get(
            "source",
            "unknown"
        )

        print(
            f"[RAG] Rank {rank}: "
            f"{score:.4f} - {source}"
        )

    # --------------------------------------------------------
    # Select top K
    # --------------------------------------------------------

    top_documents = [
        document
        for document, score
        in ranked_documents[:top_k]
    ]

    print(
        f"[RAG] Selected top {len(top_documents)} documents."
    )

    return top_documents


# ============================================================
# 7. RETRIEVE + RERANK
# ============================================================

def retrieve_and_rerank(
    query: str,
    retrieval_k: int = 10,
    top_k: int = 3
):

    # --------------------------------------------------------
    # Step 1: Vector retrieval
    # --------------------------------------------------------

    documents = retrieve_documents(
        query=query,
        k=retrieval_k
    )

    # --------------------------------------------------------
    # Step 2: Reranking
    # --------------------------------------------------------

    ranked_documents = rerank_documents(
        query=query,
        documents=documents,
        top_k=top_k
    )

    return ranked_documents


# ============================================================
# 8. FORMAT DOCUMENTS FOR LLM
# ============================================================

def format_documents(
    documents: list
):

    if not documents:

        return (
            "No relevant documents were found "
            "in the private knowledge base."
        )

    formatted_documents = []

    for index, document in enumerate(
        documents,
        start=1
    ):

        source = document.metadata.get(
            "source",
            "unknown"
        )

        content = document.page_content

        formatted_documents.append(
            f"""
DOCUMENT {index}

SOURCE:
{source}

CONTENT:
{content}
"""
        )

    return "\n\n".join(
        formatted_documents
    )