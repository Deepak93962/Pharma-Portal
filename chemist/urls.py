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
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:medicine_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    path("cart/update/<int:item_id>/<str:action>/", views.update_cart_qty, name="update_cart_qty"),
    path('category/<str:category>/', views.category_page, name='category_page'),
    path('payment/<int:order_id>/', views.payment_page, name='payment_page'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),
 



]
