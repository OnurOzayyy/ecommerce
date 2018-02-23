from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse

from products.models import Variation
from carts.models import CartItem, Cart


class ItemCountView(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            cart_id = self.request.session.get("cart_id")
            if cart_id is None:
                count = 0
            else:
                cart = Cart.objects.get(id=cart_id)
                count = cart.items.count()
            request.session["cart_item_count"] = count
            return JsonResponse({"count": count})
        else:
            raise Http404

class CartView(View):
    model = Cart
    template_name = "carts/cart_view.html"


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
        flash_message = ""
        item_added = False
        if item_id:
            item_instance = get_object_or_404(Variation, id=item_id)
            qty = request.GET.get("qty", 1)
            try:
                if int(qty) <= 0:
                    delete_item = True
            except:
                raise Http404
            cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)

            if created:
                flash_message = "Successfully added to the cart"
                item_added = True
            if delete_item:
                flash_message = "Item removed successfully."
                cart_item.delete()
            else:
                if not created:
                    flash_message = "Quantity has been updated successfully."
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
            try:
                cart_total = cart_item.cart.total
            except:
                cart_total = None
            try:
                tax_total = cart_item.cart.tax_total
            except:
                tax_total = None
            try:
                total_items = cart_item.cart.items.count()
            except:
                total_items = 0
            data = {
                    "deleted": delete_item,
                    "item_added": item_added,
                    "subtotal": subtotal,
                    "line_total": total,
                    "flash_message" : flash_message,
                    "total_items": total_items,
                    "tax_total" : tax_total,
                    "cart_total": cart_total
            }
            return JsonResponse(data)

        context = {
            "object": self.get_object()
        }
        template = self.template_name
        return render(request, template, context)

class CheckoutView(DetailView):
    model = Cart
    template_name = "carts/checkout_view.html"

    def get_object(self, *args, **kwargs):
        """
        Return cart object to display if none, then redirect to the cart.
        """
        cart_id = self.request.session.get("cart_id")
        if cart_id == None:
            return redirect("cart")
        cart = Cart.objects.get(id=cart_id)
        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(*args, **kwargs)
        user_can_continue = False
        if not self.request.user.is_authenticated:
            context["login_form"] = AuthenticationForm()
            context["next_url"] = self.request.build_absolute_uri()
            print('???',context["next_url"])
        if self.request.user.is_authenticated:
            user_can_continue = True
        context["user_can_continue"] = user_can_continue
        return context
