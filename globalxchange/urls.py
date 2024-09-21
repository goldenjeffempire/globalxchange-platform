from django.conf.urls import handler404, handler500
from django.urls import path
from . import views
from .views import create_order

handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'

urlpatterns = [
    path('', views.home, name='home'),  # Home page that lists products
    path('signup/', views.signup, name='signup'),  # User sign-up
    path('login/', views.login_view, name='login'),  # User login
    path('logout/', views.logout_view, name='logout'),  # User logout
    path('profile/', views.profile, name='profile'),  # User profile
    path('order_history/', views.order_history, name='order_history'),  # Order history
    path('cart/', views.cart, name='cart'),  # Cart view
    path('place_order/<int:product_id>/', views.place_order, name='place_order'),  # Place order
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),  # Product detail
    path('products/', views.product_list, name='product_list'),  # Product list
    path('orders/create/<int:pk>/', views.create_order, name='create_order'),  # Create order
    path('search/', views.search_products, name='search_products'),  # Search products
    path('some_view/', views.some_view, name='some_view'),  # Example protected view
]
