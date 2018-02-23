from django.db import models


class GuestCheckout(models.Model):
    """docstring for GuestCheckout"""
    email = models.EmailField()

    def __str__(self):
        pass

class Order(models.Model):
    pass
