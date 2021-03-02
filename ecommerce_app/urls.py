from django.urls import path
from . import views

# python manage.py

urlpatterns = [
    path('', views.login),
    path('dashboard', views.dashboard),
    path('dashboard/orders', views.orders),
    path('orders/show/<int:id>', views.order_show),
    path('dashboard/products', views. products)
]
