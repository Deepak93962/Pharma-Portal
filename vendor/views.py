from django.shortcuts import render, redirect
from .models import Medicine
from .forms import MedicineForm
from chemist.models import Order 
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def vendor_dashboard(request):
    medicines = Medicine.objects.all().order_by('name')
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'vendor_dashboard.html', {
        'medicines': medicines,
        'orders': orders
    })

def vendor_orders(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'vendor_orders.html', {'orders': orders})


def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vendor_dashboard')  # go back to dashboard after saving
    else:
        form = MedicineForm()
    return render(request, 'add_medicine.html', {'form': form})

@csrf_exempt
def update_order_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order = Order.objects.get(id=order_id)

        # ✅ Always define medicine early
        medicine = order.medicine  

        old_status = order.status

        # ✅ Reduce quantity once when first approved OR delivered
        if new_status in ["Approved", "Delivered"] and not order.is_stock_updated:
            if medicine.quantity >= order.quantity:
                medicine.quantity -= order.quantity
                medicine.save()
                order.is_stock_updated = True
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'Not enough stock! Only {medicine.quantity} left.'
                })

        # ✅ Add back quantity only if stock was previously updated
        if new_status == "Cancelled" and order.is_stock_updated:
            medicine.quantity += order.quantity
            medicine.save()
            order.is_stock_updated = False  # reset flag

        # ✅ Save updated order
        order.status = new_status
        order.save()

        return JsonResponse({
            'success': True,
            'order_id': order.id,
            'new_status': order.status,
            'new_quantity': medicine.quantity
        })

    return JsonResponse({'success': False})