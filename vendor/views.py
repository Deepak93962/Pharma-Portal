from django.shortcuts import render, redirect
from .models import Medicine
from .forms import MedicineForm

# Create your views here.
def vendor_dashboard(request):
    medicines = Medicine.objects.all()   # ✅ fetch all medicines
    return render(request, 'vendor_dashboard.html',{'medicines': medicines})

def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vendor_dashboard')  # go back to dashboard after saving
    else:
        form = MedicineForm()
    return render(request, 'add_medicine.html', {'form': form})