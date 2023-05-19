from .models import Transaction
from .serializers import TransactionSerializer
from EmdadUser.models import CustomUser
from rest_framework import permissions,status, viewsets, generics


class TransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.all().order_by('-created_date')
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super(TransactionListView,self).get_queryset()
        return queryset.filter(user=self.request.user)[:40]
    #     if  self.kwargs.get('pk') is None:
    #         return queryset.filter(user=self.request.user)
    #     else:
    #         pk=int(self.kwargs['pk']) 
    #         return queryset.filter(user=self.request.user,id=pk)