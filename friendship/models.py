from django.db import models
from django.contrib.auth import get_user_model

from friendship.choices import FriendshipStatusChoices

User = get_user_model()


class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_requests_sent')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_requests_received')
    status = models.CharField(
        max_length=10,
        choices=FriendshipStatusChoices.choices,
        default=FriendshipStatusChoices.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField

    class Meta:
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'

    def __str__(self):
        return f'{self.user} - {self.friend}'
