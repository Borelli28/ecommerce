from django.shortcuts import render, redirect

# renders login page
def login(request):

    return render(request, 'login.html')

# Renders dashbaord html Page
def dashboard(request):

    return render(request, 'dashboard.html')
