from django import forms
from django.contrib.auth.models import User
from .models import ChemistProfile
from .models import Order

class ChemistRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = ChemistProfile
        fields = ['shop_name', 'address', 'phone', 'username', 'password', 'email']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['medicine', 'quantity']