from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    # user_number = serializers.CharField(source='technician')
    
    class Meta:
        model = Transaction
        fields= ['id','time','technician','amount','doc','comment']