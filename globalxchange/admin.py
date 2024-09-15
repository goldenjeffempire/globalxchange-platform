from django.contrib import admin
from .models import Product, Order

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    search_fields = ('name', 'description')

admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'status')
    list_filter = ('status',)

admin.site.register(Order, OrderAdmin)
