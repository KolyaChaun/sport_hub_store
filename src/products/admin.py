from django.contrib import admin

from .models import (
    Category,
    Color,
    ProductColor,
    ProductItem,
    ProductSize,
    WarehouseItem,
)


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1


@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ("category", "title", "description", "price")
    list_filter = ("category", "price")
    search_fields = (
        "category__gender",
        "category__sub_category",
        "title",
        "description",
    )
    inlines = [ProductColorInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ["gender", "sub_category"]
    list_display = ["gender", "sub_category"]


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    fields = ["title"]
    list_display = ["title"]


@admin.register(ProductSize)
class SizeAdmin(admin.ModelAdmin):
    fields = ["value"]
    list_display = ["value"]


@admin.register(WarehouseItem)
class WarehouseAdmin(admin.ModelAdmin):
    fields = ["product", "color", "size", "status", "order"]
    list_display = ["product", "color", "size", "status", "order"]
    search_fields = ["product__title", "color__title", "size__value", "status"]
    list_filter = ["status", "color", "size"]
