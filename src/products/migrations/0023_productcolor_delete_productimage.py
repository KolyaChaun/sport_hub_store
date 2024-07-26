# Generated by Django 4.2.11 on 2024-07-11 20:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0022_alter_productimage_product_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductColor",
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
                ("image", models.ImageField(upload_to="products/")),
                (
                    "color",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="products.color"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="colors",
                        to="products.productitem",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="ProductImage",
        ),
    ]