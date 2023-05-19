from django.db import models
from Order.models import Order
from EmdadUser.models import Technecian

def Transaction_handle_upload(instance,filename):
    return f"Transaction_files/Transaction_{instance.pk}/{filename}"

class Transaction(models.Model):
    time            = models.DateTimeField('زمان', auto_now=True)
    technician      = models.ForeignKey(Technecian,on_delete=models.PROTECT)
    amount          = models.PositiveIntegerField('مبلغ')
    doc             = models.FileField(null=True, blank=True, upload_to=Transaction_handle_upload) 
    comment         = models.TextField('توضیحات',null=True,blank=True)

    def __str__(self):
        return f"{self.pk}"
    
    class Meta:
        verbose_name= 'تراکنش'
        verbose_name_plural=verbose_name