from django.urls import path, re_path, include

from .views import CategoryListView, CategoryDetailView



urlpatterns = [

    re_path(r'^$', CategoryListView.as_view(), name='categories'),
    re_path(r'^(?P<slug>[\w-]+)/$', CategoryDetailView.as_view(), name='category_detail')
]
