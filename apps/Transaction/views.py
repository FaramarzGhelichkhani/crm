from .models import Transaction
from .serializers import TransactionSerializer
from apps.EmdadUser.models import Technician
from rest_framework import permissions, generics
from jalali_date import datetime2jalali


def get_created_jalali(obj):
    return datetime2jalali(obj.time).strftime('14%y/%m/%d')


class TransactionListView_app(generics.ListAPIView):
    queryset = Transaction.objects.all().order_by('-time')
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super(TransactionListView_app, self).get_queryset()
        tech = Technician.objects.get(user=self.request.user)
        data = queryset.filter(technician=tech)[:40]
        for trans in data:
            trans.time = get_created_jalali(trans)
        return data
