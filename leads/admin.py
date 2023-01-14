from django.contrib import admin

from .models import  Lead, Agent, AgentProfile,  FollowUp, Transaction, Messages
from jalali_date import datetime2jalali


class LeadAdmin(admin.ModelAdmin):
    list_display = ['__str__','get_created_jalali']

    def get_created_jalali(self,obj):
	    return datetime2jalali(obj.time).strftime('%y/%m/%d %H:%M:%S')




admin.site.register(Lead, LeadAdmin)
admin.site.register(Messages)
admin.site.register(Agent)
admin.site.register(Transaction)
admin.site.register(FollowUp)
