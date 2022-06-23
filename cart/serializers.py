
from .models import OrderItem, User, Cart, DeliveryCost
from rest_framework import serializers
from products.serializers import ProductSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'created_at', 'updated_at']



class OrderItemSerializer(serializers.ModelSerializer):

    """Serializer for the OrderItem model."""

    class Meta:
        model = OrderItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    """Serializer for the Cart model."""
    # used to represent the target of the relationship using its __unicode__ method

    class Meta:
        model = Cart
        fields ='__all__'



class DeliveryCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryCost
        fields = ['id', 'status', 'cost_per_delivery', 'cost_per_product', 'fixed_cost', 'created_at', 'updated_at']