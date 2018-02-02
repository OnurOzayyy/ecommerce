
from django.urls import path, re_path, include


from .views import ProductDetailView

urlpatterns = [
    re_path('^(?P<pk>\d+)/$', ProductDetailView.as_view() , name='product_detail'),
]
