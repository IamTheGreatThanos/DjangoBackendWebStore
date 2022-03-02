from django.contrib import admin
from .models import User, Product
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'displayID', 'token']
    list_filter = ['username', 'id']
    readonly_fields = ['username', 'token']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'price', 'in_stock']
    list_filter = ['name','in_stock']

admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)