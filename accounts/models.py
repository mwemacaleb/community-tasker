from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    POSTER = 'poster'
    TASKER = 'tasker'

    ROLE_CHOICES = [
        (POSTER, 'Poster'),
        (TASKER, 'Tasker'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=POSTER,
    )
    is_verified = models.BooleanField(default=False)
    student_id = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"