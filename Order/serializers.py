from rest_framework import serializers
from .models import Order, Order_Product
from Emdad.serializers import ServiceNameSerializer, MotorSerializer


class OrderProductListSerializer(serializers.ListSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['child'] = OrderProductSerializer()
        super().__init__(*args, **kwargs)


    def create(self, validated_data):
        order = self.context['order']
        order_products = [Order_Product(order=order, **item) for item in validated_data]
        return Order_Product.objects.bulk_create(order_products)


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Product
        fields = ('product', 'number', 'price')
    
    def create(self, validated_data):
        order = self.context['order']
        order_product = Order_Product.objects.create(order=order, **validated_data)
        return order_product




class OrderSerializer(serializers.ModelSerializer):
    technecian_name = serializers.CharField(source='technecian')
    services_list = ServiceNameSerializer(source='services',many=True, read_only=True) 
    motors_list = MotorSerializer(source='motors', many=True, read_only=True)
    customer_full_name = serializers.SerializerMethodField()
    customer_phone = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'created_date', 'requested_date', 'technecian_name', 'location', 'services_list',
                   'motors_list', 'status', 'wage','expanse' ,'customer_full_name', 'customer_phone']

    def get_customer_full_name(self, obj):
        if obj.customer:
            return obj.customer.full_name()
        else:
            return None

    def get_customer_phone(self, obj):
        if obj.customer and obj.customer.user_id.phone:
            return obj.customer.phonenumber()
        else:
            return None


class OrderAcceptSerializer(serializers.Serializer):
    technecian_id = serializers.IntegerField()