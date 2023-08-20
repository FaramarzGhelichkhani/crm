from django.urls import path
from .views import ServiceList, MotorList, ProductList

app_name = "emdad"
urlpatterns = [
    path('services/', ServiceList.as_view()),
    path('motors/', MotorList.as_view()),
    path('products/', ProductList.as_view()),
]
