from django import forms
from .models import Technecian, CustomUser


class AgentModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AgentModelForm, self).__init__(*args, **kwargs)
        self.fields['balance'].disabled = True


    
    class Meta:
        model = Technecian
        fields = (
'user_id',
'address',
'commission',
'balance',
'activation_status',
'time_shift',
'comment',
'avatar',
        )


class UserModelForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = (
'phone','first_name','last_name',

        )     


class reciptForm(forms.ModelForm):
    start_date_offset = forms.IntegerField(label='روز شروع')
    end_date_offset = forms.IntegerField(label='روز پایان')  

    class Meta:
        model = CustomUser
        fields =  ('start_date_offset', 'end_date_offset',)