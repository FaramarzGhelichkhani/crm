from rest_framework import serializers
from .models import Service, Motor, Product

class ServiceSerializer(serializers.ModelSerializer):  
      
    class Meta:
        model = Service
        fields = ['name','id']
    
    

class ServiceNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name']
    def to_representation(self, value):
        return value.name     


class MotorSerializer(serializers.ModelSerializer):  
      
    class Meta:
        model = Motor
        fields = []
    
    def to_representation(self, value):
        return  value.brand + ' ' + value.model

class MotorListSerializer(serializers.ModelSerializer):  
      
    class Meta:
        model  = Motor
        fields = ['id', 'brand', 'model']
    
    def to_representation(self, value):
        return {
            'id': value.id,
            'name': value.brand + ' ' + value.model,
        }

class ProductSerializer(serializers.ModelSerializer):  
      
    class Meta:
        model = Product
        fields = ['id','name']
    
    # def to_representation(self, value):
    #     return value.name