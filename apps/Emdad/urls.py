from django.urls import path
from .views import ServiceList, MotorList, ProductList, change_language

app_name = "emdad"
urlpatterns = [
    path('services/', ServiceList.as_view()),
    path('motors/', MotorList.as_view()),
    path('products/', ProductList.as_view()),
    path('change-language/<str:language_code>/',
         change_language, name='change_language'),
]
