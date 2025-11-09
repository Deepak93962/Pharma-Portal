from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendor_dashboard, name='vendor_dashboard'),
    path('add/', views.add_medicine, name='add_medicine'), 
]
