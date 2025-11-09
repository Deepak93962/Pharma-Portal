from django.shortcuts import render
from vendor.models import Medicine

def home(request):
    medicines = Medicine.objects.all()
    return render(request, 'index.html', {'medicines': medicines})
