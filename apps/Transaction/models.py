from django.db import models
from apps.EmdadUser.models import Technician
from django.utils.translation import gettext_lazy as _ 

def transaction_handle_upload(instance,filename):
    return f"Transaction_files/Transaction_{instance.pk}/{filename}"

class Transaction(models.Model):
    time            = models.DateTimeField(_('time'), auto_now=True)
    technician      = models.ForeignKey(Technician,on_delete=models.PROTECT)
    amount          = models.PositiveIntegerField(_('amount transaction'))
    doc             = models.FileField(null=True, blank=True, upload_to=transaction_handle_upload) 
    comment         = models.TextField(_('explanation'),null=True,blank=True)

    def __str__(self):
        return f"{self.pk}"
    
    class Meta:
        verbose_name= _('transaction')
        verbose_name_plural= _('transactions')
        db_table  = 'Transaction'
