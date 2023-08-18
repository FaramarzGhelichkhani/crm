from django import forms
from .models import Transaction
from apps.Order.models import Order

class TransactionFormModel(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransactionFormModel, self).__init__(*args, **kwargs)

    
    class Meta:
        model = Transaction
        fields  =(
            'technician',
            'amount',
            'comment',
        )

    field_order=['technician',
            'amount',
            'comment',]