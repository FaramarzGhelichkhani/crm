from django import forms
from .models import Order, Followup
# from django.contrib.auth.models import User
from EmdadUser.models import CustomUser, Technecian
from django.contrib.auth.forms import UserCreationForm

class OrderModelForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(OrderModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Order
        fields = (
      'customer_full_name',
      'customer_phone',
      'address',
      'motors',
        'technecian',
        'services',
        # 'comment',
    
 
        )
    field_order=['customer_full_name','customer_phone','address','motors','services','technecian'
    ,'comment']



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("phone",)


class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Technecian.objects.filter(activation_status=1))
    status_choices = (
        ("در حال انجام", "در حال انجام"),
        ("انجام شد","انجام شد"),
        ("در آستانه کنسلی", "در آستانه کنسلی"),
        ("کنسلی قطعی",  "کنسلی قطعی"),
    )
    status = forms.ChoiceField(choices = status_choices, label="وضعیت سفارش", widget=forms.Select(), required=False)   




class FollowUpModelForm(forms.ModelForm):
    
    status_choices = (
        ("در حال انجام", "در حال انجام"),
        ("انجام شد","انجام شد"),
        ("در آستانه کنسلی", "در آستانه کنسلی"),
        ("کنسلی قطعی",  "کنسلی قطعی"),
    )
    status = forms.ChoiceField(choices = status_choices, label="وضعیت سفارش", widget=forms.Select(), required=False)

    class Meta:
        model = Followup
        fields = (
            'notes',
            'grade',
            'total_price_cusotmer',
            'total_wage_agent','total_expanse_agent',
            # 'user',
            # 'time'
        )


