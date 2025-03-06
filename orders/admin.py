from django.contrib import admin
from .models import Equipment, Order, Service, EquipmentCategory, EquipmentSubCategory, ChatGroup, Offer
# Register your models here.


class EquipmentInline(admin.TabularInline):  # or use StackedInline for a different layout
    model = Equipment
    extra = 1  # Number of empty forms displayed to add new equipment
    fields = ['name', 'description', 'register_date', 'serial_number']
    readonly_fields = ['serial_number']  # Optional: Mark some fields as readonly


class OrderInline(admin.TabularInline):
    model = Order
    extra = 1
    fields = ['order_id', 'created_at', 'price', 'description', 'subcategory', 'service', 'executor_id']
    readonly_fields = ['order_id', 'created_at']


class SubCategoryInline(admin.TabularInline):
    model = EquipmentSubCategory
    extra = 1
    fields = ['name', 'description']
    readonly_fields = ['description']


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1
    fields = ['name', 'description']
    readonly_fields = ['description']
    inlines = [OrderInline]


# Equipment Admin
@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'serial_number', 'register_date']
    search_fields = ['name', 'serial_number']


@admin.register(EquipmentCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    inlines = [SubCategoryInline]


@admin.register(EquipmentSubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    inlines = [ServiceInline, OrderInline, EquipmentInline]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    inlines = [OrderInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer', 'service', 'created_at']  # Customize the list view
    list_filter = ['created_at']  # Add filters for quick navigation
    search_fields = ['customer__username', 'service__name']  # Enable searching
    autocomplete_fields = ['customer', 'service']  # Auto-complete fields for FK relationships
    ordering = ['-created_at']  # Sort orders by creation date (most recent first)
    date_hierarchy = 'created_at'  # Add a date hierarchy filter


admin.site.register(ChatGroup)
admin.site.register(Offer)