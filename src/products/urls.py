
from django.urls import path, re_path, include


from .views import ProductDetailView, ProductListView

urlpatterns = [
    re_path('^(?P<pk>\d+)/$', ProductDetailView.as_view() , name='product_detail'),
    re_path('^$', ProductListView.as_view(), name='products'),
]
