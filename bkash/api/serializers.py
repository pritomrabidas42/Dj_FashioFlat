from rest_framework import serializers
from ..models import BkashPayment
from orders.models import Order

class BkashPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BkashPayment
        fields = ['order', 'transaction_id', 'phone_number', 'paid_amount', 'payment_time']
        read_only_fields = ['payment_time']

class BkashInitiateSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

class BkashExecuteSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    payment_id = serializers.CharField()

