from django.urls import path

from .views import (
    health_check,
    chat,
    human_review,
)


urlpatterns = [
    path(
        "health/",
        health_check,
        name="health",
    ),

    path(
        "chat/",
        chat,
        name="chat",
    ),

    path(
        "human-review/",
        human_review,
        name="human-review",
    ),
]
