from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.utils import timezone
from django.db.models import Q


from .models import Product


class ProductListView(ListView):
    model = Product
    queryset = Product.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context['now'] =timezone.now()
        context["query"] = self.request.GET.get('q')
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(*args, **kwargs) #default query set
        query = self.request.GET.get('q')
        if query:  # if there is a query then you want to overwrite the default query set.
            qs = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
                )
            try:
                qs2 = self.model.objects.filter(
                        Q(price=query))
                qs = (qs | qs2).distinct()
            except:
                pass
        return qs

class ProductDetailView(DetailView):
    model = Product
