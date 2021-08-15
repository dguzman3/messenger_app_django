from django.db import models
from accounts.models import CustomUser

class Chat(models.Model):
    text = models.TextField()
    from_user = models.ForeignKey(CustomUser, related_name='chat_from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='chat_to_user', on_delete=models.CASCADE)
    sent_time = models.TimeField(auto_now=True)
    date_available = models.DateField(auto_now=True)

    def __str__(self):
        return f'Message {self.id} from {self.from_user} to {self.to_user}'
