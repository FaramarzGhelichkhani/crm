from django.urls import path
from .views import (
ExpendListView,
ExpendUpdateView,
ExpendCreateView,
)
app_name = 'company'

urlpatterns = [
    path('', ExpendListView.as_view(), name='expend-list'),
    path('<int:pk>/update/', ExpendUpdateView.as_view(), name='expend-update'),
    path('create/', ExpendCreateView.as_view(), name='expend-create'),
]