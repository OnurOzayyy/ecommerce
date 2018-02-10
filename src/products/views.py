
"""
Display product list and detail. Search for a product.
"""
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.utils import timezone
from django.db.models import Q


from .models import Product, Category



class CategoryListView(ListView):
    """
    View for the List of the categories.
    """
    model = Category
    queryset = Category.objects.all()
    template_name = "products/product_list.html"


class CategoryDetailView(DetailView):
    """
    View for the Category Detail.
    """
    model = Category

    def get_context_data(self, *args, **kwargs):
        """
        Returns products both in default category and
        the category selected.
        """
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        obj = self.get_object()
        product_set = obj.product_set.all()
        default_products = obj.default_category.all()
        products = (product_set | default_products).distinct()
        context["products"] = products
        return context


class ProductListView(ListView):
    """
    Display products, allow search for specific product.
    """
    model = Product
    queryset = Product.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context['now'] = timezone.now()
        context["query"] = self.request.GET.get('q')
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super(ProductListView, self).get_queryset(*args, **kwargs) #default query set
        query = self.request.GET.get('q')
        if query:  # if there is a query then you want to overwrite the default query set.
            queryset = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
            try:
                queryset2 = self.model.objects.filter(
                    Q(price=query))
                queryset = (queryset | queryset2).distinct()
            except:
                pass
        return queryset

class ProductDetailView(DetailView):
    """
    Display product detail.
    """
    model = Product
