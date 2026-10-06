from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    question = serializers.CharField(
        required=True,
        allow_blank=False,
    )
    session_id = serializers.CharField(
        required=False,
        allow_blank=False,
        allow_null=True,
        default=None,
    )


class HumanReviewRequestSerializer(serializers.Serializer):
    session_id = serializers.CharField(
        required=True,
        allow_blank=False,
    )
    action = serializers.ChoiceField(
        choices=["approve", "revise"],
    )
    feedback = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
    )
