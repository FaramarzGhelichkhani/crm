from django.contrib import admin
from .models import Service, Motor, Region,Product

admin.site.register(Service)
admin.site.register(Region)
admin.site.register(Motor)
admin.site.register(Product)