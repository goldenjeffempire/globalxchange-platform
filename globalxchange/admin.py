from django.contrib import admin
from .models import Product, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'quantity', 'created_at')  
    list_filter = ('status', 'created_at')  # Changed 'ordered_at' to 'created_at'
    search_fields = ('user__username', 'orderitem__product__name')  # Ensure 'orderitem' relationship is correct

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    list_filter = ('order', 'product')
