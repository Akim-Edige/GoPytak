from django.db import models
from users.models import User
import uuid

class EquipmentCategory(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class EquipmentSubCategory(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(EquipmentCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    subcategory = models.ForeignKey(EquipmentSubCategory, models.DO_NOTHING, related_name='subcategory')

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    customer = models.ForeignKey(User, models.DO_NOTHING, related_name='customer')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    service = models.ForeignKey(Service, models.DO_NOTHING)
    description = models.TextField(blank=True, null=True)
    subcategory = models.ForeignKey(EquipmentSubCategory, models.DO_NOTHING)
    executor_id = models.CharField(max_length=36, blank=True, null=True)


class Equipment(models.Model):
    equipment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='equipment')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    register_date = models.DateField(blank=True, null=True)
    serial_number = models.CharField(max_length=50, unique=True)
    subcategory = models.ForeignKey(EquipmentSubCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.serial_number}"



