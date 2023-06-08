from django.db import models
from EmdadUser.models import Technecian,CustomUser
from Emdad.models import Service, Motor,Product


class Order(models.Model):
    time   = models.DateTimeField('زمان ایجاد',auto_now_add=True)
    services       = models.ManyToManyField(Service,verbose_name=  'خدمات')
    motors         = models.ManyToManyField(Motor,verbose_name='موتور')
    address       = models.CharField('آدرس',max_length= 100 )
    customer_phone 		= models.CharField('شماره تماس مشتری',max_length=20)
    customer_full_name 	= models.CharField('نام مشتری',max_length=100,null=True,blank=True)    
    technecian     = models.ForeignKey(Technecian,on_delete=models.PROTECT, null=True,blank=True)
    status_choices = (
        ("در حال انجام", "در حال انجام"),
        ("انجام شد","انجام شد"),
        ("در آستانه کنسلی", "در آستانه کنسلی"),
        ("کنسلی قطعی",  "کنسلی قطعی"),
    )
    status = models.CharField('وضعیت سفارش',max_length = 15,choices=status_choices, default="در حال انجام")
    grade  = models.SmallIntegerField('امتیاز عملکرد', null= True , blank = True, default=5)
    wage   = models.PositiveIntegerField('اجرت',default=0)
    commission = models.PositiveIntegerField('کمیسیون', null=True, blank=True)
    expanse= models.PositiveIntegerField('خرجکرد',default=0)
    total_price_cusotmer = models.PositiveIntegerField('هزینه نهایی پرداخت شده توسط مشتری',null=True,blank=True)

    comment= models.TextField('توضیحات',null=True,blank=True)

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.pk}" 


    def save(self, *args, **kwargs):
        if self.status == "انجام شد" and self.technecian is not None:
            commission = int(float(self.wage) * self.technecian.commission)
            if self.commission != commission:
                self.commission = commission

        super().save(*args, **kwargs)


class Order_Product(models.Model):
    order  = models.ForeignKey(Order,on_delete=models.PROTECT)
    product= models.ForeignKey(Product,on_delete=models.PROTECT,null=True)
    number = models.SmallIntegerField('تعداد',null=True,blank=True)    
    price  = models.PositiveIntegerField('قیمت',null=True,blank=True)
    description = models.TextField('توضیحات',null=True,blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order', 'product'], name='unique_order_product')
        ]

class Followup(models.Model):
    time   = models.DateTimeField('زمان ایجاد',auto_now_add=True)
    order  = models.ForeignKey(Order,on_delete=models.PROTECT,related_name="followups")
    notes = models.TextField('توضیحات',null=True,blank=True)
    user = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING,null=True)
    total_price_cusotmer = models.PositiveIntegerField('هزینه نهایی پرداخت شده  (مشتری)',null=True,blank=True)
    total_wage_agent = models.PositiveIntegerField('اجرت نهایی پرداخت شده (تکنسین)',null=True,blank=True)    
    total_expanse_agent = models.PositiveIntegerField('خرجکرد نهایی پرداخت شده (تکنسین)',null=True,blank=True)
    grade = models.SmallIntegerField('امتیاز عملکرد', null= True , blank = True)


    class Meta:
        verbose_name = 'پیگیری'
        verbose_name_plural = verbose_name


    def __str__(self):
        return f"{self.user.full_name()} noted on {self.order}"