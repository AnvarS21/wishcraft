from django.db import models

class FriendshipStatusChoices(models.TextChoices):
    PENDING = 'pending', 'Рассматривается'
    ACCEPTED = 'accepted', 'Принято'
    REJECTED = 'rejected', 'Отклонено'
