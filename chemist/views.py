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
from .models import Order


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
    # ✅ Fetch only the logged-in chemist’s orders
    orders = Order.objects.filter(chemist=request.user).order_by('-order_date')
    return render(request, 'chemist_dashboard.html', {'orders': orders})
