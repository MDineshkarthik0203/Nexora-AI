import os
from pathlib import Path
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
# ENVIRONMENT & PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]
CHROMA_DIR = PROJECT_ROOT / "chroma_db"
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv()

_embeddings = None
_vectorstore = None
_reranker = None


def get_embeddings():
    global _embeddings
    if _embeddings is None:
        api_key = os.getenv("MISTRAL_API_KEY") or os.getenv("MISTRALAI_API_KEY")
        if not api_key:
            raise ValueError(
                "MISTRAL_API_KEY is not set. Please add MISTRAL_API_KEY to your .env file."
            )
        _embeddings = MistralAIEmbeddings(
            model="mistral-embed",
            mistral_api_key=api_key,
        )
    return _embeddings


def get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = Chroma(
            collection_name="agentforge_mistral_rag",
            embedding_function=get_embeddings(),
            persist_directory=str(CHROMA_DIR),
        )
    return _vectorstore


def get_reranker():
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )
    return _reranker


class _LazyProxy:
    def __init__(self, getter):
        self._getter = getter

    def __getattr__(self, name):
        return getattr(self._getter(), name)


embeddings = _LazyProxy(get_embeddings)
vectorstore = _LazyProxy(get_vectorstore)
reranker = _LazyProxy(get_reranker)


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

    target_dir = Path(data_directory)
    if not target_dir.is_absolute():
        target_dir = PROJECT_ROOT / data_directory

    print(f"\nLoading documents from {target_dir}...")

    loader = DirectoryLoader(
        str(target_dir),
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

    get_vectorstore().add_documents(
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

    try:
        documents = get_vectorstore().similarity_search(
            query,
            k=k
        )
    except Exception as exc:
        print(f"[RAG] Retrieval error: {exc}")
        return []

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

    try:
        scores = get_reranker().predict(
            pairs
        )
    except Exception as exc:
        print(f"[RAG] Reranking notice: {exc}. Returning retrieved documents.")
        return documents[:top_k]

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