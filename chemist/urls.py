from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page for chemists
    path('register/', views.chemist_register, name='chemist_register'),
    path('login/', views.chemist_login, name='chemist_login'),
    path('logout/', views.chemist_logout, name='chemist_logout'),
    path('order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),
    path('dashboard/', views.chemist_dashboard, name='chemist_dashboard'),

]
