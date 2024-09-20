from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from globalxchange import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('globalxchange.urls')),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_history/', views.order_history, name='order_history'),
    path('search/', views.search_products, name='search_products'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
