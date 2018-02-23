from decimal import Decimal
from django.db import models
from django.conf import settings
from products.models import Variation
from django.db.models.signals import pre_save, post_save



class CartItem(models.Model):
    """
    Cart Item Model.
    """
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
    item = models.ForeignKey(Variation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.item.title

    def remove(self):
        """
        Removes the item from the cart by calling the
        remove_from_cart method of the Variation.
        """
        return self.item.remove_from_cart()


def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    """
    Sets the price for item before it is saved to the database.
    """
    qty = int(instance.quantity)
    if qty >= 1:
        price = instance.item.get_price()
        line_item_total = Decimal(qty) * Decimal(price)
        instance.line_item_total = line_item_total

pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)

def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    instance.cart.update_subtotal()

post_save.connect(cart_item_post_save_receiver, sender=CartItem)


class Cart(models.Model):
    """
    Cart Model.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    items = models.ManyToManyField(Variation, through=CartItem)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    subtotal = models.DecimalField(max_digits=6, decimal_places=2, default=25.00)
    tax_total = models.DecimalField(max_digits=6, decimal_places=2, default=25.00)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=25.00)

    def __str__(self):
        return str(self.id)

    def update_subtotal(self):
        """
        Calculate the cart subtotal by adding the each item's price.
        """
        subtotal = 0
        items = self.cartitem_set.all()
        print(items)
        for item in items:
            subtotal += item.line_item_total
        self.subtotal = subtotal
        self.save()

def do_tax_and_total_receiver(sender, instance, *args, **kwargs):
    subtotal = Decimal(instance.subtotal)
    tax_total = round(subtotal * Decimal(0.085), 2)
    total = round(subtotal + Decimal(tax_total), 2)
    instance.tax_total = tax_total
    instance.total = total

pre_save.connect(do_tax_and_total_receiver, sender=Cart)

