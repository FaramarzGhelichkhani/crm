from .views import TransactionListView_app
from django.urls import path

app_name = "transaction"
urlpatterns = [
    path('', TransactionListView_app.as_view(),name='transactions-list_app'),
    # path('<int:pk>/',TransactionListView.as_view(), name='transaction')
]
