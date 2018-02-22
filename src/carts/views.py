from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse

from products.models import Variation
from carts.models import CartItem, Cart


class CartView(View):
    model = Cart
    template_name = "carts/view.html"


    def get_object(self, *args, **kwargs):
        """
        Checks if cart exists in the session.
        if not, then creates and saves a new cart object and
        saves its id in the session. If the user authenticated,
        then associates the cart with that user.
        Returns the cart object.
        """
        self.request.session.set_expiry(0)
        cart_id = self.request.session.get("cart_id")
        if cart_id == None:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session["cart_id"] = cart_id
        cart = Cart.objects.get(id=cart_id)
        if self.request.user.is_authenticated:
            cart.user = self.request.user
            cart.save()
        return cart

    def get(self, request, *args, **kwargs):
        """
        Get method which would be called by dispatch.
        Calls the get_cart_object method to obtaint the cart object.
        Adds or Deletes the item, obtaining the item id and quantity from
        the Get request.
        """
        cart = self.get_object()
        item_id = request.GET.get("item")
        delete_item = request.GET.get("delete", False)
        item_added = False
        if item_id:
            print('inside if item id ',item_id)
            item_instance = get_object_or_404(Variation, id=item_id)
            qty = request.GET.get("qty", 1)
            try:
                if int(qty) <= 0:
                    delete_item = True
            except:
                raise Http404
            cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)

            if created:
                item_added = True
            if delete_item:
                cart_item.delete()
            else:
                cart_item.quantity = qty
                cart_item.save()
            if not request.is_ajax():
                return HttpResponseRedirect(reverse("cart"))

        if request.is_ajax():
            try:
                total = cart_item.line_item_total
            except:
                total = None
            try:
                subtotal = cart_item.cart.subtotal
            except:
                subtotal = None
            data = {
                    "deleted": delete_item,
                    "item_added": item_added,
                    "subtotal": subtotal,
                    "line_total": total
                    }
            print(request.GET.get("item"))
            return JsonResponse(data)

        context = {
            "object": self.get_object()
        }
        template = self.template_name
        return render(request, template, context)
