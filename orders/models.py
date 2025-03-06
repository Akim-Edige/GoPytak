from django.db import models
from users.models import User
import uuid
import shortuuid


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


class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    users_online = models.ManyToManyField(User, related_name='online_in_groups', blank=True)
    members = models.ManyToManyField(User, related_name='chat_groups', blank=True)

    def __str__(self):
        return self.group_name


class Offer(models.Model):
    # Details
    group = models.ForeignKey(ChatGroup, related_name="chat_offers", on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, models.CASCADE, related_name='offers')
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # Direction
    proposer = models.ForeignKey(User, models.DO_NOTHING, related_name='proposer')
    # offeree = models.ForeignKey(User, models.DO_NOTHING, related_name='offeree')
    # Body
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.proposer.is_customer:
            return f'Offer from {self.proposer.username} to executor'

        return f'Offer from {self.proposer.username} to client'

    class Meta:
        ordering = ['-created']


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



