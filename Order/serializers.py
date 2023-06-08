from rest_framework import serializers
from .models import Order, Order_Product
from Emdad.serializers import ServiceNameSerializer, MotorSerializer
from jalali_date import datetime2jalali


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
    time = serializers.SerializerMethodField()
    

    class Meta:
        model = Order
        fields = ['id', 'time', 'technecian_name', 'address', 'services_list',
                   'motors_list', 'status', 'wage','expanse' ,'customer_full_name', 'customer_phone']

    def get_time(self,instance):
	    return datetime2jalali(instance.time).strftime('14%y/%m/%d')    


class OrderAcceptSerializer(serializers.Serializer):
    technecian_id = serializers.IntegerField()