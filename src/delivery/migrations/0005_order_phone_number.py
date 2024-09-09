# Generated by Django 4.2.11 on 2024-09-09 10:56

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("delivery", "0004_order_branch"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                default=0, max_length=128, region=None, unique=True
            ),
            preserve_default=False,
        ),
    ]