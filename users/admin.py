from django.contrib import admin
from django.contrib import admin
from .models import User
from orders.admin import EquipmentInline
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [EquipmentInline]  # Add the inline to the UserAdmin
    list_display = ['username', 'email', 'is_staff', 'is_active']  # Optional: Show these fields in the list view
    search_fields = ['username', 'email']  # Optional: Add search functionality
    ordering = ['username']  # Optional: Sort users alphabetically