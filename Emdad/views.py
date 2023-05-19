from rest_framework import generics
from .models import Service, Motor, Product
from .serializers import ServiceSerializer, MotorListSerializer, ProductSerializer

class ServiceList(generics.ListAPIView):
    queryset = Service.objects.all().values('id', 'name')
    serializer_class = ServiceSerializer

class MotorList(generics.ListAPIView):
    queryset = Motor.objects.all()
    serializer_class = MotorListSerializer    

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer