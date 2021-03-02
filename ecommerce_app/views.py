from django.shortcuts import render, redirect

# python manage.py

# renders login page
def login(request):

    return render(request, 'login.html')

# Renders dashbaord html Page
def dashboard(request):

    return render(request, 'dashboard.html')

# Renders the orders page
def orders(request, id):

    context = {"id": id}

    return render(request, 'orders.html', context)
