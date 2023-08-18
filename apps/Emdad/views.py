from django.utils.translation import activate
from django.shortcuts import redirect
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


def change_language(request, language_code):
    activate(language_code)
    response = redirect('admin:index')  # Redirect to the admin index page
    response.set_cookie('django_language', language_code)
    return response
