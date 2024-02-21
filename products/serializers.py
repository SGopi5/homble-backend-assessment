from rest_framework import serializers

from products.models import Product,Sku


class ProductListSerializer(serializers.ModelSerializer):
    """
    To show list of products.
    """

    class Meta:
        model = Product
        fields = ["name", "price","edited_at","created_at"]


class SkuSerializer(serializers.ModelSerializer):
    measurement_unit_display = serializers.CharField(source='get_measurement_unit_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Sku
        fields = '__all__'
        read_only_fields = ('measurement_unit_display', 'status_display')
