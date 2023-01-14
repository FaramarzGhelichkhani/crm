from datetime import datetime
from tabnanny import verbose
from xml.etree.ElementTree import Comment
from django.db import models
from django.utils import timezone

class Expend(models.Model):
    time = models.DateTimeField('زمان',null=True,blank=True, default=timezone.now)
    amount = models.PositiveIntegerField('مقدار')
    comment = models.CharField('عنوان',max_length=320) 

    class Meta:
        verbose_name = 'خرج کردها'
        verbose_name_plural=verbose_name


class Followup(models.Model):
    time = models.DateTimeField('زمان')
    comment =  models.TextField('عنوان')
    link = models.URLField("لینک",  max_length=200, blank=True, null=True)
    status = models.CharField('وضعیت',choices=(('در حال پیگیری','در حال پیگیری'),('پیگیری شد','پیگیری شد')),max_length=32,default='در حال پیگیری') 

    class Meta:
        verbose_name =  'پیگیری ها'
        verbose_name_plural=verbose_name


