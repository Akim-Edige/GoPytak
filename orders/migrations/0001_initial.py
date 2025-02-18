# Generated by Django 5.1.5 on 2025-02-02 09:13

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Equipment",
            fields=[
                (
                    "equipment_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                ("register_date", models.DateField(blank=True, null=True)),
                ("serial_number", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="EquipmentCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name="EquipmentSubCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "order_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("description", models.TextField(blank=True, null=True)),
                ("executor_id", models.CharField(blank=True, max_length=36, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
    ]
