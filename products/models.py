from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    name = models.CharField(
        _("display name"),
        max_length=150,
        unique=True,
        help_text=_("This will be displayed to user as-is"),
    )
    price = models.PositiveSmallIntegerField(
        _("selling price (Rs.)"),
        help_text=_("Price payable by customer (Rs.)"),
    )
    description = models.TextField(
        _("descriptive write-up"),
        unique=True,
        help_text=_("Few sentences that showcase the appeal of the product"),
    )
    is_refrigerated = models.BooleanField(
        help_text=_("Whether the product needs to be refrigerated"),
        default=False,
    )
    ingredients = models.CharField(
        _("ingredients"),
        max_length=500,
        blank=True,
        help_text=_("List of ingredients in the product"),
    )
    edited_at = models.DateTimeField(
        _("last edited at"),
        auto_now=True,
        help_text=_("Timestamp of the most recent object edit"),
    )
    category = models.ForeignKey(
        "categories.Category",
        related_name="products",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    managed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="managed_products",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.name = self.name.strip().title()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (Rs. {self.price})"

    class Meta:
        db_table = "product"
        ordering = []
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Sku(models.Model):
    MEASUREMENT_UNIT_CHOICES = (
        ('g', _('Grams')),
        ('kg', _('Kilograms')),
        ('ml', _('Milliliters')),
        ('L', _('Liters')),
    )

    STATUS_CHOICES = (
        (0, _('Inactive')),
        (1, _('Active')),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.PositiveSmallIntegerField(validators=[MaxValueValidator(999)], help_text=_("Size"))
    measurement_unit = models.CharField(max_length=2, choices=MEASUREMENT_UNIT_CHOICES, default='g')
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    platform_commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    class Meta:
        unique_together = ('product', 'size')

    def save(self, *args, **kwargs):
        self.selling_price = self.cost_price + self.platform_commission
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - Size: {self.size}{self.measurement_unit} - Selling Price: Rs. {self.selling_price}"