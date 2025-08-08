from rest_framework import serializers
from ..models import CartItem
from products.api.serializers import ProductSerializer
from products.models import Product 


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'
