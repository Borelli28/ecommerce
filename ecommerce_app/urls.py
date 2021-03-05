from django.urls import path
from . import views

# python manage.py

urlpatterns = [
    path('', views.login),
    path('clear', views.clear),
    path('add_seller', views.register_seller),
    path('log_seller', views.log_seller),
    path('dashboard', views.dashboard),
    path('dashboard/orders', views.orders),
    path('orders/show/<int:id>', views.order_show),
    path('dashboard/products', views.products),
    path('dashboard/products/edit_product/<int:id>', views.edit_product),
    path('dashboard/products/delete_product/<int:id>', views.delete_product),
    path('product_edit/<int:id>', views.product_edit),
    path('add_product', views.add_product),
    path('product_add', views.create_product),
    path('update_status_order/<int:id>', views.update_status_order),

    # Customer site
    path('login', views.login_page),
    path('home', views.home)

]
