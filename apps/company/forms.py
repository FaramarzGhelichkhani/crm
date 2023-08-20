from django import forms
from .models import Expend


class ExpendModelForm(forms.ModelForm):

    class Meta:
        model = Expend
        fields = ('time', 'amount', 'comment',)
