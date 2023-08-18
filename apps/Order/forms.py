from django import forms
from .models import Order, Followup
from apps.Emdad.models import Motor, Service
from apps.EmdadUser.models import CustomUser, Technician
from django.contrib.auth.forms import UserCreationForm

class OrderModelForm(forms.ModelForm):
    
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        frequented_services = [ '.','پنچری', 'زنجیر', 'تسمه', 'باطری', 'لاستیک', 'سیم کلاج', 'سیم گاز', 'روشن نمی شود', 'سرویس', 'مغزی و سوییچ', 'چرخ عقب قفل', 'قفل', 'حرکت نمیکند', 'جلوبندی', 'اچارکشی',  'صفحه','موارد دیگر']
        frequented_motors = [187,111,218,300,122,263,316,64,70,152,34,200,40,3,170,57,256,181,219]
        self.fields['services'].queryset = Service.objects.filter(name__in=frequented_services)
        self.fields['motors'].queryset = Motor.objects.filter(id__in=frequented_motors)
    



 
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("phone",)


class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Technician.objects.filter(activation_status=1))
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
    agent = forms.ModelChoiceField(queryset=Technician.objects.filter(activation_status=1))
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

    field_order = ['notes','agent','grade',]
