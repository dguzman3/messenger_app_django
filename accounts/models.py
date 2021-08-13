from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    friends = models.ManyToManyField("CustomUser", blank=True)

    def __str__(self):
        return self.username

class FriendRequest(models.Model):
    from_user = models.ForeignKey("CustomUser", related_name="from_user", 
        on_delete=models.CASCADE)
    to_user = models.ForeignKey("CustomUser", related_name="to_user", 
        on_delete=models.CASCADE)