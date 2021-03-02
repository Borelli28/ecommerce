from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('dashboard', views.dashboard),
    path('dashboard/orders/<int:id>', views.orders)
]
