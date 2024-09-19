from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Order, OrderItem
from .forms import SignUpForm

# Home view
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

# Product list view
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# Product detail view
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})

# Place an order for a specific product
@login_required
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

# View user's order history
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'orders': orders})

# Cart view to add items to session-based cart
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
    return render(request, 'login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('home')

# Sign-up view
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# Profile view
@login_required
def profile(request):
    return render(request, 'profile.html')
