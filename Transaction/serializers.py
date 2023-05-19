from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    user_number = serializers.CharField(source='user')
    
    class Meta:
        model = Transaction
        fields= ['id','created_date','user','user_number','amount','doc','description']