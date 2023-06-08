from django.db import models
from EmdadUser.models import Technecian

class Service(models.Model):
    name      = models.CharField('نام سرویس',max_length=150) 
    min_price = models.IntegerField('کمینه قیمت',default=250000)
    max_price = models.IntegerField('بیشینه قیمت',default=250000)
    STATUS_active = 1
    STATUS_deactive = 2
    status_choices = (
        (STATUS_active, "فعال"),
        (STATUS_deactive, "غیرفعال"),
    )
    activation_status = models.IntegerField('وضعیت',choices=status_choices, default = 1)
    technecians = models.ManyToManyField(Technecian, null=True, blank=True)
    comment    = models.TextField('توضیحات',null=True, blank=True)

    class Meta:
        verbose_name = 'خدمات'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"


class Region(models.Model):
    city = models.CharField('شهر',max_length=150)
    area = models.CharField('منطقه یا ناحیه',max_length=150)
    STATUS_active = 1
    STATUS_deactive = 2
    status_choices = (
        (STATUS_active, "فعال"),
        (STATUS_deactive, "غیرفعال"),
    )
    activation_status = models.IntegerField('وضعیت',choices=status_choices, default = 1)
    technecians = models.ManyToManyField(Technecian,  null=True, blank=True)
    
    class Meta:
        verbose_name = 'مناطق تحت پوشش'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.city} {self.area}"


class Motor(models.Model):
    company = models.CharField('کمپانی',max_length=150,null=True,blank=True)
    brand   = models.CharField('برند',max_length=150)
    model   = models.CharField('مدل',max_length=150,null=True,blank=True)
    year    = models.CharField('سال ساخت',max_length=5,null=True,blank=True)
    
    INJECTOR = 1
    CARBURETOER = 2
    status_choices = (
        (INJECTOR, "انژکتور"),
        (CARBURETOER, "کاربراتور"),
    )
    engine_type = models.IntegerField('نوع موتور',choices=status_choices, default = 1)
    technecians = models.ManyToManyField(Technecian,  null=True, blank=True)
      
    class Meta:
        verbose_name = 'موتور'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.brand}" 

class Product(models.Model):
    name = models.CharField('نام قطعه',max_length=150)

    class Meta:
        verbose_name = 'لوازم و قطعات'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}" 