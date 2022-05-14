from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USER_ROLES = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=USER_ROLES,
        default=USER
    )
    bio = models.TextField(blank=True)

    @property
    def is_admin(self):
        return self.role == User.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR
