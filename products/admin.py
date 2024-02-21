from django.contrib import admin
from products.models import *

class SkuInline(admin.StackedInline):
    model = Sku
    extra = 0

@admin.register(Sku)
class SkuAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'measurement_unit', 'selling_price', 'platform_commission', 'cost_price', 'status')
    search_fields = ('product__name',)
    list_filter = ('measurement_unit', 'status')
    autocomplete_fields = ('product',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "managed_by", "edited_at")
    ordering = ("-id",)
    search_fields = ("name",)
    list_filter = ("is_refrigerated", "category")
    fields = (
        ("name", "price"),
        ("category", "is_refrigerated"),
        "description",
        "ingredients",
        ("id", "created_at", "edited_at"),
        "managed_by",
    )
    autocomplete_fields = ("category", "managed_by")
    readonly_fields = ("id", "created_at", "edited_at")
    inlines = [SkuInline]


class ProductInline(admin.StackedInline):
    """
    For display in CategoryAdmin
    """

    model = Product
    extra = 0
    ordering = ("-id",)
    readonly_fields = ("name", "price", "is_refrigerated", "edited_at")
    fields = (readonly_fields,)
    show_change_link = True
