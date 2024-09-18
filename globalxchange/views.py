from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Order, OrderItem
from .forms import SignUpForm  # Ensure this form is defined in your forms.py

@login_required
def place_order(request):
    if request.method == 'POST':
        # Assuming items are stored in session for simplicity
        cart = request.session.get('cart', [])
        order = Order.objects.create(user=request.user, status='Pending')
        for item_id in cart:
            product = get_object_or_404(Product, id=item_id)
            OrderItem.objects.create(order=order, product=product)
        request.session['cart'] = []
        return redirect('order_history')
    return render(request, 'place_order.html')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'orders': orders})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        # Add product to cart logic here
        # Example: Append to session cart
        cart = request.session.get('cart', [])
        if product_id not in cart:
            cart.append(product_id)
            request.session['cart'] = cart
        return redirect('cart')
    return render(request, 'cart.html')

def search_products(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        products = Product.objects.all()
    return render(request, 'search_results.html', {'products': products})

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

def logout_view(request):
    logout(request)
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to the homepage after successful signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')
