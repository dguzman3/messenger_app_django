from django import forms
from django.forms import fields
from .models import Chat

class CreateChat(forms.ModelForm):

    class Meta:
        model = Chat
        fields = "__all__"