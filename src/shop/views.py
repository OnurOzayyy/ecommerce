from django.shortcuts import render


from products.models import Product


def home_page(request):
    products = Product.objects.all()
    context = {
        "title": 'Welcome to SF Home Design',
        "products": products
    }
    return render(request, 'shop/home.html', context)
