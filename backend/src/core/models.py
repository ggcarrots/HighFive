from django.contrib.auth.models import AbstractUser, User
from django.db import models


class User(AbstractUser):
    BADGE_CHOICES = (
        ('Nowicjusz', 'Nowicjusz'),
        ('Lokalny Bohater', 'Lokalny Bohater'),
        ('Urzędnik', 'Urzędnik'),
    )
    badge = models.TextField(choices=BADGE_CHOICES)
