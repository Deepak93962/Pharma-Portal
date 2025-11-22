from django.shortcuts import render ,redirect, get_object_or_404
from vendor.models import Medicine
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import ChemistRegisterForm
from .models import ChemistProfile
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .models import Order ,OrderItem,CartItem
from .models import CartOrder, CartOrderItem ,Payment
from django.http import JsonResponse
from django.http import HttpResponse



@never_cache
def home(request):
    return render(request, 'index.html')


def home(request):
    medicines = Medicine.objects.all()
    return render(request, 'index.html', {'medicines': medicines})

def chemist_register(request):
    if request.method == 'POST':
        form = ChemistRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            ChemistProfile.objects.create(
                user=user,
                shop_name=form.cleaned_data['shop_name'],
                address=form.cleaned_data['address'],
                phone=form.cleaned_data['phone']
            )
            login(request, user)  # auto-login after registration
            return redirect('home')
    else:
        form = ChemistRegisterForm()
    return render(request, 'chemist_register.html', {'form': form})

def chemist_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # ✅ redirect directly to home (not re-render login page)
            # messages.success(request, f"Welcome {user.username} 👋")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'chemist_login.html')

    else:
        # clear any previous messages so login page doesn't show old success messages
        list(messages.get_messages(request))   # consume and discard
        return render(request, 'chemist_login.html')


def chemist_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('chemist_login')

@login_required
def place_order(request):
    # 👇 Step 1: Get medicine_id from URL
    medicine_id = request.GET.get('medicine_id')
    selected_medicine = None

    # 👇 Step 2: If ID exists, get that medicine safely
    if medicine_id:
        selected_medicine = get_object_or_404(Medicine, id=medicine_id)

    # 👇 Step 3: If POST (form submission)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.chemist = request.user
            order.total_price = order.medicine.price * order.quantity
            order.save()
            return redirect('order_success')
    else:
        # 👇 Step 4: If medicine clicked → pre-select that medicine in form
        if selected_medicine:
            form = OrderForm(initial={'medicine': selected_medicine})
        else:
            form = OrderForm()

    # 👇 Step 5: Render the form + selected medicine info
    return render(request, 'place_order.html', {
        'form': form,
        'selected_medicine': selected_medicine
    })

def order_success(request):
    return render(request, 'order_success.html')

@login_required
def chemist_dashboard(request):
    single_orders = Order.objects.filter(chemist=request.user).order_by('-order_date')
    cart_orders = CartOrder.objects.filter(chemist=request.user).order_by('-order_date')

    return render(request, 'chemist_dashboard.html', {
        'single_orders': single_orders,
        'cart_orders': cart_orders
    })


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(chemist=request.user)
    if not cart_items:
        return redirect('view_cart')

    # ✅ Create one order
    total = sum(item.get_total_price() for item in cart_items)
    order = Order.objects.create(
        chemist=request.user,
        total_amount=total,
        status='Pending',
        payment_status='Pending'
    )

    # ✅ Add items to that order
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            medicine=item.medicine,
            quantity=item.quantity,
            price=item.medicine.price
        )

    # ✅ Clear cart after placing order
    cart_items.delete()

    # Redirect to success page
    return redirect('order_success')


# ADD TO CART
@login_required
def add_to_cart(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    cart_item, created = CartItem.objects.get_or_create(
        chemist=request.user,
        medicine=medicine
    )
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')


# VIEW CART
@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(chemist=request.user)
    total = sum(item.get_total() for item in cart_items)
    return render(request, 'chemist_cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# REMOVE ITEM
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, chemist=request.user)
    item.delete()
    return redirect('view_cart')


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(chemist=request.user)

    if not cart_items:
        return redirect('view_cart')

    # Create CartOrder (MASTER ORDER)
    total_amount = sum(item.get_total() for item in cart_items)

    cart_order = CartOrder.objects.create(
        chemist=request.user,
        total_amount=total_amount,
        status="Pending",
        payment_status="Pending"
    )

    # Create CartOrderItem (ALL ITEMS INSIDE ORDER)
    for item in cart_items:
        CartOrderItem.objects.create(
            order=cart_order,
            medicine=item.medicine,
            quantity=item.quantity,
            price=item.medicine.price
        )

    # Clear the cart
    cart_items.delete()

    return redirect('order_success')




@login_required
def update_cart_qty(request, item_id, action):
    try:
        item = CartItem.objects.get(id=item_id, chemist=request.user)
    except:
        return JsonResponse({"success": False})

    if action == "increase":
        item.quantity += 1
    elif action == "decrease" and item.quantity > 1:
        item.quantity -= 1

    item.save()

    # Recalculate total cart amount
    cart_items = CartItem.objects.filter(chemist=request.user)
    total = sum(i.get_total() for i in cart_items)

    return JsonResponse({
        "success": True,
        "new_qty": item.quantity,
        "new_total": total
    })

def category_page(request, category):
    medicines = Medicine.objects.filter(category__iexact=category)

    return render(request, "category.html", {
        "category": category.capitalize(),
        "medicines": medicines
    })

def payment_page(request, order_id):
    order = get_object_or_404(CartOrder, id=order_id, chemist=request.user)
    return render(request, "payment_page.html", {"order": order})

def payment_page(request, order_id):
    order_type = request.GET.get("type")

    # Single Order
    if order_type == "single":
        order = get_object_or_404(Order, id=order_id)
        amount = order.total_price

    # Cart Order
    elif order_type == "cart":
        order = get_object_or_404(CartOrder, id=order_id)
        amount = order.total_amount

    else:
        return HttpResponse("Invalid payment type")

    return render(request, "payment_page.html", {
        "order": order,
        "order_type": order_type,
        "amount": amount,
    })


def payment_success(request, order_id):
    order_type = request.GET.get("type")

    if request.method != "POST":
        return HttpResponse("Invalid Request")

    method = request.POST.get("method", "Online Payment")

    # SINGLE ORDER PAYMENT
    if order_type == "single":
        order = Order.objects.get(id=order_id, chemist=request.user)
        Payment.objects.create(
            chemist=request.user,
            single_order=order,
            amount=order.total_price,
            method=method,
        )
        order.status = "Paid"
        order.save()

    elif order_type == "cart":
        order = CartOrder.objects.get(id=order_id, chemist=request.user)
        Payment.objects.create(
            chemist=request.user,
            cart_order=order,
            amount=order.total_amount,
            method=method,
        )
        order.status = "Paid"
        order.save()


    else:
        return HttpResponse("Invalid Order Type")

    return render(request, "payment_success.html", {
        "id": order_id,
        "type": order_type,
        "method": method,
    })
