from rest_framework import serializers
from .models import Order, OrderProduct
from apps.Emdad.serializers import ServiceNameSerializer, MotorSerializer
from jalali_date import datetime2jalali


class OrderProductListSerializer(serializers.ListSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['child'] = OrderProductSerializer()
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        order = self.context['order']
        order_products = [OrderProduct(order=order, **item)
                          for item in validated_data]
        return OrderProduct.objects.bulk_create(order_products)


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ('product', 'number', 'price')

    def create(self, validated_data):
        order = self.context['order']
        order_product = OrderProduct.objects.create(
            order=order, **validated_data)
        return order_product


class OrderSerializer(serializers.ModelSerializer):
    technecian_name = serializers.CharField(source='technician')
    services_list = ServiceNameSerializer(
        source='services', many=True, read_only=True)
    motors_list = MotorSerializer(source='motors', many=True, read_only=True)
    time = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'time', 'technecian_name', 'address', 'services_list',
                  'motors_list', 'status', 'wage', 'expanse', 'customer_full_name', 'customer_phone']

    def get_time(self, instance):
        return datetime2jalali(instance.time).strftime('14%y/%m/%d')


class OrderAcceptSerializer(serializers.Serializer):
    technecian_id = serializers.IntegerField()
