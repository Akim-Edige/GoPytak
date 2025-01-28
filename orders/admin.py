from django.contrib import admin
from .models import Equipment, Order, Service


# Register your models here.

class EquipmentInline(admin.TabularInline):  # or use StackedInline for a different layout
    model = Equipment
    extra = 1  # Number of empty forms displayed to add new equipment
    fields = ['name', 'description', 'register_date', 'serial_number']
    readonly_fields = ['serial_number']  # Optional: Mark some fields as readonly


# Inline for Equipment Services
class EquipmentsInServiceInline(admin.TabularInline):
    model = Equipment.services.through  # Access the ManyToMany relationship table
    extra = 1  # Number of empty rows for adding services

# Equipment Admin
@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'serial_number', 'register_date']
    search_fields = ['name', 'serial_number']
    inlines = [EquipmentsInServiceInline]  # Inline for services
    filter_horizontal = ['services']  # Adds a better UI for managing services



@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    inlines = [EquipmentsInServiceInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer', 'executor', 'service', 'status', 'created_at']  # Customize the list view
    list_filter = ['status', 'created_at']  # Add filters for quick navigation
    search_fields = ['customer__username', 'executor__username', 'service__name']  # Enable searching
    autocomplete_fields = ['customer', 'executor', 'service']  # Auto-complete fields for FK relationships
    ordering = ['-created_at']  # Sort orders by creation date (most recent first)
    date_hierarchy = 'created_at'  # Add a date hierarchy filter
