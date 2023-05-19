from .views import TransactionListView
from django.urls import path

app_name = "transactions"
urlpatterns = [
    path('', TransactionListView.as_view(),name='transactions-list'),
    path('<int:pk>/',TransactionListView.as_view(), name='transaction')
]
