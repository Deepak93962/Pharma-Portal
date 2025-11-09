from django.shortcuts import render

# Create your views here.
def vendor_dashboard(request):
    return render(request, 'vendor_dashboard.html')