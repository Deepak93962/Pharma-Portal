from django import forms
from .models import Medicine

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'category', 'price', 'quantity', 'description', 'image', 'image_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter medicine name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price (₹)'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock quantity'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Online image link (optional)'}),
        }
