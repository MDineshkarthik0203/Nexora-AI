from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    ChatRequestSerializer,
    HumanReviewRequestSerializer,
)

from .services import (
    create_session_id,
    run_agent,
    resume_agent,
)


@api_view(["GET"])
def health_check(request):
    """
    GET /api/health/
    """

    return Response({
        "status": "ok",
        "service": "AgentForge Django API",
    })


@api_view(["POST"])
def chat(request):
    """
    POST /api/chat/

    Example:

    {
        "question": "give me python code for palindrome",
        "session_id": "agentforge-test-001"
    }
    """

    serializer = ChatRequestSerializer(
        data=request.data,
    )

    serializer.is_valid(
        raise_exception=True,
    )

    question = serializer.validated_data[
        "question"
    ]

    session_id = serializer.validated_data.get(
        "session_id"
    )

    if not session_id:
        session_id = create_session_id()

    try:
        result = run_agent(
            question=question,
            session_id=session_id,
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )

    except Exception as exc:
        return Response(
            {
                "success": False,
                "error": str(exc),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def human_review(request):
    """
    POST /api/human-review/

    Approve:

    {
        "session_id": "agentforge-test-001",
        "action": "approve",
        "feedback": ""
    }

    Revise:

    {
        "session_id": "agentforge-test-001",
        "action": "revise",
        "feedback": "Use a more efficient algorithm."
    }
    """

    serializer = HumanReviewRequestSerializer(
        data=request.data,
    )

    serializer.is_valid(
        raise_exception=True,
    )

    session_id = serializer.validated_data[
        "session_id"
    ]

    action = serializer.validated_data[
        "action"
    ]

    feedback = serializer.validated_data.get(
        "feedback",
        "",
    )

    try:
        result = resume_agent(
            session_id=session_id,
            action=action,
            feedback=feedback,
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )

    except Exception as exc:
        return Response(
            {
                "success": False,
                "error": str(exc),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
