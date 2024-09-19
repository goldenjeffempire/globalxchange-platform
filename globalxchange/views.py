from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from .models import Product, Order, OrderItem
from .forms import SignUpForm, OrderForm

# Home view
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

# Product list view
@login_required(login_url=settings.LOGIN_URL)
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# Product detail view
@login_required(login_url=settings.LOGIN_URL)
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})

# Place an order for a specific product
@login_required(login_url=settings.LOGIN_URL)
def place_order(request, product_id=None):
    if product_id:
        product = get_object_or_404(Product, pk=product_id)
        if request.method == 'POST':
            quantity = int(request.POST.get('quantity', 1))
            order = Order.objects.create(user=request.user, status='Pending')
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
            return redirect('order_history')
        return render(request, 'place_order.html', {'product': product})
    else:
        # Handle cart-based order placement
        if request.method == 'POST':
            cart = request.session.get('cart', [])
            order = Order.objects.create(user=request.user, status='Pending')
            for item_id in cart:
                product = get_object_or_404(Product, id=item_id)
                OrderItem.objects.create(order=order, product=product)
            request.session['cart'] = []
            return redirect('order_history')
        return render(request, 'place_order.html')

# Create an order (similar to place order but with an OrderForm)
@login_required(login_url=settings.LOGIN_URL)
def create_order(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.product = product
            order.save()
            return redirect('order_history')
    else:
        form = OrderForm()
    return render(request, 'create_order.html', {'form': form, 'product': product})

# View user's order history
@login_required(login_url=settings.LOGIN_URL)
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'orders': orders})

# Cart view to add items to session-based cart
@login_required(login_url=settings.LOGIN_URL)
def cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get('cart', [])
        if product_id not in cart:
            cart.append(product_id)
            request.session['cart'] = cart
        return redirect('cart')
    return render(request, 'cart.html')

# Search for products
def search_products(request):
    query = request.GET.get('q')
    products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)) if query else Product.objects.all()
    return render(request, 'search_results.html', {'products': products})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Sign-up view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Profile view
@login_required(login_url=settings.LOGIN_URL)
def profile(request):
    return render(request, 'profile.html')

# Example of a protected view
@login_required(login_url=settings.LOGIN_URL)
def some_view(request):
    # Your view logic here
    return render(request, 'some_template.html')  # Replace 'some_template.html' with your template
