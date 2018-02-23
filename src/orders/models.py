from django.db import models
from django.conf import settings

class UserCheckout(models.Model):
    """docstring for UserCheckout"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class Order(models.Model):
    pass
