from django.urls import path
from . import views

# python manage.py

urlpatterns = [
    path('', views.login),
    path('dashboard', views.dashboard),
    path('dashboard/orders', views.orders),
    path('orders/show/<int:id>', views.order_show),
    path('dashboard/products', views.products),
    path('dashboard/products/edit_product/<int:id>', views.edit_product),
    path('dashboard/products/delete_product/<int:id>', views.delete_product),
    path('product_edit', views.product_edit)
]
