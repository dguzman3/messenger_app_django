from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import CreateView

from .forms import CreateChat
from .models import Chat

@login_required
def chat_view(request, userID):
    context = {}
    queryset = Chat.objects.filter(
        (Q(from_user=request.user) & Q(to_user__id=userID)) | 
        (Q(from_user__id=userID) & Q(to_user=request.user))
        )
    context["chats"] = queryset.order_by("sent_time")
    return render(request, "social/chat_room.html", context)

class CreateChatView(CreateView):
    form_class = CreateChat
    success_url = "chats"
    template_name = "social/chat_room.html"

    def get_context_data(self, **kwargs):
        userID = self.kwargs["userID"]
        context = {}
        queryset = Chat.objects.filter(
            (Q(from_user=self.request.user) & Q(to_user__id=userID)) | 
            (Q(from_user__id=userID) & Q(to_user=self.request.user))
            )
        context["chats"] = queryset.order_by("sent_time")
        return context
