from django.db import models
from users.models import User
import uuid


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    customer = models.ForeignKey(User, models.DO_NOTHING, related_name='customer')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ])
    executor = models.ForeignKey(User, models.DO_NOTHING, related_name='executor', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    service = models.ForeignKey(Service, models.DO_NOTHING)
    description = models.TextField(blank=True, null=True)


class Equipment(models.Model):
    equipment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='equipment')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    register_date = models.DateField(blank=True, null=True)
    serial_number = models.CharField(max_length=50, unique=True)
    services = models.ManyToManyField(Service, related_name='equipments', blank=True)

    def __str__(self):
        return f"{self.name} - {self.serial_number}"

