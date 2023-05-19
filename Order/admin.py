from django.contrib import admin
from .models import Order, Order_Product

admin.site.register(Order)
admin.site.register(Order_Product)