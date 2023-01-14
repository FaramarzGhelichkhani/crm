from django import forms
from django.core.exceptions import ValidationError
from .models import Lead, Agent, FollowUp, Transaction, Messages
from django.contrib.auth.models import User
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime

from django.contrib.auth.forms import UserCreationForm

class LeadModelForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(LeadModelForm, self).__init__(*args, **kwargs)
        # self.fields['time'] = JalaliDateField(label=_('time'), # date format is  "yyyy-mm-dd"
        #     widget=AdminJalaliDateWidget # optional, to use default datepicker
        # )
        # self.fields['customer_messeg'].disabled = True
        # self.fields['technician_messeg'].disabled = True
        # self.fields['transaction_status'].disabled = True
        # self.fields['status'].disabled = True

    class Meta:
        model = Lead
        fields = (
            # 'time',
      'customer_full_name',
      'customer_phone',
      'address',
      'motor_model',
        'agent',
        'problem',
        'comment',
    #   'status',
    #   'transaction_status',
      'technician_messeg',
      'customer_messeg',
 
        )
    field_order=['customer_full_name','customer_phone','address','motor_model','problem','agent',
    'customer_messeg','technician_messeg','comment']


    def clean(self):
        pass
        # first_name = self.cleaned_data["first_name"]
        # last_name = self.cleaned_data["last_name"]
        # if first_name + last_name != "Joe Soap":
        #     raise ValidationError("Your name is not Joe Soap")


class TransactionFormModel(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransactionFormModel, self).__init__(*args, **kwargs)
        # agentid =  kwargs['initial']['technician'].id
        # orders = Lead.objects.filter(
        #     transaction_status="تسویه نشده",agent__id=agentid)
         
        self.fields['technician'].widget =forms.HiddenInput()
        self.fields['category'].widget =forms.HiddenInput()
        self.fields["tech"].disabled = True
        self.fields['cat'].disabled = True
        # .attrs['readonly'] = True 
        if  'order' in kwargs['initial']: 
            self.fields['orders'].queryset = kwargs['initial']['order'] 


    tech = forms.CharField(label="کارشناس")
    cat = forms.CharField(label="عتوان")
    orders = forms.ModelMultipleChoiceField(queryset=Lead.objects.none(),widget=forms.CheckboxSelectMultiple)    
    
    class Meta:
        model = Transaction
        fields  =(
            'technician',
            'order',
            'total_amount',
            'company_amount',
            'category',
            'comment',
        )

    field_order=['tech','cat','orders','order','total_amount','company_amount','comment']

# class LeadForm(forms.Form):
#     customer_phone = forms.CharField()
#     customer_full_name = forms.CharField()
#     problem = forms.IntegerField(min_value=0)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        # field_classes = {'username': UsernameField}


# class AgentModelForm(forms.ModelForm):
#     class Meta:
#         model = Agent
#         fields = (

#         )

class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.filter(activation_status=1))
    status_choices = (
        ("در حال انجام", "در حال انجام"),
        ("انجام شد","انجام شد"),
        ("در آستانه کنسلی", "در آستانه کنسلی"),
        ("کنسلی قطعی",  "کنسلی قطعی"),
    )
    status = forms.ChoiceField(choices = status_choices, label="وضعیت سفارش", widget=forms.Select(), required=False)
    # def __init__(self, *args, **kwargs):
    #     request = kwargs.pop("request")
    #     # agents = Agent.objects.filter(id=request.agent.id)
    #     super(AssignAgentForm, self).__init__(*args, **kwargs)
    #     self.fields["agent"].queryset = agent




class FollowUpModelForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     # lead = kwargs.pop("lead",None)
    #     # id = request.followup.id
    #     # lead = FollowUp.objects.get(id=id).lead
    #     lead = self.lead
    #     grade = lead.grade
    #     super(FollowUpModelForm, self).__init__(*args, **kwargs)
    #     self.fields['grade'] =  grade

    status_choices = (
        ("در حال انجام", "در حال انجام"),
        ("انجام شد","انجام شد"),
        ("در آستانه کنسلی", "در آستانه کنسلی"),
        ("کنسلی قطعی",  "کنسلی قطعی"),
    )
    status = forms.ChoiceField(choices = status_choices, label="وضعیت سفارش", widget=forms.Select(), required=False)

    tr_status_choices = (
          ("تسویه شد","تسویه شد"),
        ("تسویه نشده","تسویه نشده"),
    )
    tr_status = forms.ChoiceField(choices = tr_status_choices, label="وضعیت تسویه", widget=forms.Select(), required=False)
    # so_tien=forms.CharField(label="Số tiền",widget=forms.TextInput(attrs={"class":"form-control", 'onfocusout': 'numberWithCommas()',}),required=False)
    class Meta:
        model = FollowUp
        fields = (
            'notes',
            'grade',
            'total_price_cusotmer',
            'total_price_agent'
            #'date_added'
        )


