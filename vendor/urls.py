from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendor_dashboard, name='vendor_dashboard'),
    path('add/', views.add_medicine, name='add_medicine'), 
    
    path('orders/', views.vendor_orders, name='vendor_orders'),
    path('payments/', views.vendor_payments, name='vendor_payments'),
    path('update-order/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path("about/", views.about_vendor, name="about_vendor"),
    path("login/", views.vendor_login, name="vendor_login"),
]
