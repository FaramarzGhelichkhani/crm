from django import forms
from .models import Followup , Expend

class FollowModelForm(forms.ModelForm):


    class Meta:
        model = Followup
        fields = ('time','comment','link','status',)


class ExpendModelForm(forms.ModelForm):


    class Meta:
        model = Expend
        fields = ('time','amount','comment',)        