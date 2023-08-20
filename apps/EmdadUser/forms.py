from django import forms
from .models import Technician, CustomUser
from django.utils.translation import gettext_lazy as _


class AgentModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AgentModelForm, self).__init__(*args, **kwargs)
        self.fields['balance'].disabled = True

    class Meta:
        model = Technician
        fields = (
            'user',
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
            'phone', 'first_name', 'last_name',

        )


class reciptForm(forms.ModelForm):
    start_date_offset = forms.IntegerField(label=_('start day'))
    end_date_offset = forms.IntegerField(label=_('end day'))

    class Meta:
        model = CustomUser
        fields = ('start_date_offset', 'end_date_offset',)
