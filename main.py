import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


def main():
    print("=" * 60)
    print("  Nexora-AI / AgentForge - Multi-Agent Engineering Copilot")
    print("=" * 60)
    print("To start the backend server:")
    print("  python backend/manage.py runserver")
    print("\nTo start the frontend UI:")
    print("  cd frontend && npm run dev")
    print("\nTo run the agent test:")
    print("  python tests/test_agent.py")
    print("\nTo run Human-in-the-Loop test:")
    print("  python tests/test_hitl.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
