from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # For using built-in User model if needed
from django.conf import settings


class PassengerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"

