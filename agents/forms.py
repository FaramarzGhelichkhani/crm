from django import forms
from leads.models import Agent


class AgentModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AgentModelForm, self).__init__(*args, **kwargs)
        self.fields['balance'].disabled = True

    class Meta:
        model = Agent
        fields = (
'phone1',
'phone2',
'first_name',
'last_name',
'expertise',
'region',
'time_shift',
'address',
'comment',
'weight',
'balance',
'activation_status',
'Image',
'file',
        )