# Generated by Django 4.2.11 on 2024-06-20 17:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "products",
            "0020_category_color_productimage_productitem_productsize_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="sub_category",
            field=models.CharField(default="", max_length=128),
            preserve_default=False,
        ),
    ]