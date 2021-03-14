from django.urls import path
from . import views

# python manage.py

urlpatterns = [
    # Seller site urls
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

    # Customer site urls
    path('login', views.login_page),
    path('add_customer', views.register_customer),
    path('log_customer', views.log_customer),
    path('home', views.home),
    path('home/<int:id>', views.home_category),
    path('show/<int:id>', views.show),
    path('cart/<int:id>', views.cart),
    path('cart_show', views.show_cart),
    path('clear_cart', views.clear_cart),
    path('process_payment/<int:prod_id>', views.payment),
]
