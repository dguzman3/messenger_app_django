from django.urls import path
from .views import CreateChatView, chat_view

urlpatterns = [
    path("chat/<int:userID>/", CreateChatView.as_view(), name="chats"),
]