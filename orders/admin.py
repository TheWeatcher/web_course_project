 
from django.contrib import admin
 
from .models import OrderItem, Order
 
 
# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['game']
 
 
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname','first_name', 'last_name', 'email', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
 
 
admin.site.register(Order, OrderAdmin)