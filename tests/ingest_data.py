import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from agentforge.tools.rag import ingest_documents


if __name__ == "__main__":

    count = ingest_documents("data")

    print(
        f"\nIndexed chunks: {count}"
    )