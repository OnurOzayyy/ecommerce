from django.shortcuts import render



def home_page(request):
    context = {
        "title": 'Welcome to SF Home Design'
    }
    return render(request, 'shop/home.html', context)
