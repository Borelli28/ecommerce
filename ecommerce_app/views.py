from django.shortcuts import render, redirect

# python manage.py

# renders login page
def login(request):

    return render(request, 'login.html')

# Renders dashbaord html Page
def dashboard(request):

    return render(request, 'dashboard.html')

# Renders the orders page
def orders(request):

    return render(request, 'orders.html')

# Render the display order Page
def order_show(request, id):

    context = {"id": id}

    return render(request, 'order_show.html', context)

# Renders the products html
def products(request):

    return render(request, 'products.html')
