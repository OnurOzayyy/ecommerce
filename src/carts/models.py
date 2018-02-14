from django.db import models
from django.conf import settings
from products.models import Variation

class CartItem(models.Model):
    """
    Cart Item Model.
    """
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
    item = models.ForeignKey(Variation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return self.item.title

class Cart(models.Model):
    """
    Cart Model.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    items = models.ManyToManyField(Variation, through=CartItem)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


    def __str__(self):
        return str(self.id)
