from rest_framework import serializers

from delivery.models import Order


class PaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Order
        fields = ("order_id",)
