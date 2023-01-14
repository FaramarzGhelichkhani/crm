from django.db import models
from django.db.models.signals import post_save
# from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField



def handle_upload_Madarek(instance):
    return f"technecian_madarek/tech_{instance.Agent.pk}/"


class Agent(models.Model):
    time = models.DateTimeField('تاریخ ثبت نام',auto_now_add=True)
    phone1 		= models.CharField('شماره تماس',max_length=20)
    phone2 		= models.CharField('شماره تماس۲',max_length=20, null=True,blank=True)
    first_name 	= models.CharField('نام',max_length=100)
    last_name 	= models.CharField('نام خانوادگی',max_length=100)
    expertise 	= models.CharField('تخصص',max_length=100)
    region		= models.CharField('مناطق کاری',max_length=100)
    time_shift  = models.CharField(' شیفت کاری',max_length=100)
    address 	= models.TextField('آدرس')
    comment 	= models.TextField('توضیحات',null=True, blank=True)
    weight		= models.FloatField('کارمزد',default=0.2, null=True,blank=True)
    balance 	= models.IntegerField('موجودی حساب',default=0, null=True,blank=True)
    STATUS_active = 1
    STATUS_deactive = 2
    STATUS_ban = 3
    status_choices = (
        (STATUS_active, "active"),
        (STATUS_deactive, "deactive"),
        (STATUS_ban, "ban"),
    )
    activation_status = models.IntegerField('وضعیت',choices=status_choices, default = 1)
    Image = models.ImageField(null=True, blank=True,upload_to=handle_upload_Madarek)
    file = models.FileField(null=True, blank=True, upload_to=handle_upload_Madarek)


    class Meta:
        verbose_name = 'تکنسین'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class AgentProfile(models.Model):
    agent = models.OneToOneField(Agent, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class LeadManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Lead(models.Model):
    time = models.DateTimeField('زمان',auto_now_add=True)
    customer_phone 		= models.CharField('شماره تماس مشتری',max_length=20)
    customer_full_name 	= models.CharField('نام مشتری',max_length=100,null=True,blank=True)

    PANCHARI = 'پنچری'
    DYNAM = 'دینام'
    BARGH = 'برق'
    TASMEH = 'تسمه'
    ROSHANNEMISAVAD = 'روشن نمی شود'
    STARTNEMIKHORAD = 'مشکل استارت'
    BADANEH = 'بدنه'
    TORMOZ  = 'ترمز'
    problem_choices = ((PANCHARI,'پنچری'),(DYNAM , 'دینام'),(BARGH , 'برق'),(TASMEH , 'تسمه'),
    (ROSHANNEMISAVAD , 'روشن نمی شود'), (STARTNEMIKHORAD , 'مشکل استارت'), (BADANEH , 'بدنه'),(TORMOZ ,'ترمز') )
    
    # problem 			= MultiSelectField('مشکل',choices=problem_choices,max_choices=7,blank=True, null=True)

    # 
    problem = models.CharField('مشکل',max_length=256,blank=True, null=True)


    motor_model 		= models.CharField('مدل موتور',max_length=100,null=True,blank=True)
    address		= models.CharField('آدرس',max_length=1500) 
    agent 	= models.ForeignKey(Agent, null=True,blank=True, on_delete=models.PROTECT, verbose_name = 'تکنسین')
    total_price_cusotmer = models.PositiveIntegerField('هزینه نهایی پرداخت شده توسط مشتری',null=True,blank=True)
    total_price_agent = models.PositiveIntegerField('اجرت نهایی پرداخت شده توسط تکنسین',null=True,blank=True)
    technician_messeg = models.BooleanField('ارسال پیامک به تکنسین',default=False)
    customer_messeg = models.BooleanField('ارسال پیامک به مشتری',default=False)
    grade = models.SmallIntegerField('امتیاز عملکرد', null= True , blank = True)
    comment 	= models.TextField('توضیحات',null=True,blank=True)
    
    status_choices = (
        ("در حال انجام", "در حال انجام"),
        ("انجام شد","انجام شد"),
        ("در آستانه کنسلی", "در آستانه کنسلی"),
        ("کنسلی قطعی",  "کنسلی قطعی"),
    )

    status = models.CharField('وضعیت سفارش',max_length = 15,choices=status_choices, default="در حال انجام")

    tr_status_choices = (
          ("تسویه شد","تسویه شد"),
        ("تسویه نشده","تسویه نشده"),
    )
    
    transaction_status = models.CharField('وضعیت تسویه',max_length=32 ,default= "تسویه نشده")

    objects = LeadManager()


    # def save():
    #     if not Order.objects.filter(pk=self.id).exists():
    #         super(Order, self).save(*args, **kwargs)
    #         # sending messeges to customer
    #         slef.customer_messeg = True
    #     else:
    #         super(Order, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'سفارش' 
        verbose_name_plural = verbose_name       
    def __str__(self):
        return f"{self.id}"




class FollowUp(models.Model):
    lead = models.ForeignKey(Lead, related_name="followups", on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    total_price_cusotmer = models.PositiveIntegerField('هزینه نهایی پرداخت شده توسط مشتری',null=True,blank=True)
    total_price_agent = models.PositiveIntegerField('هزینه نهایی پرداخت شده توسط تکنسین',null=True,blank=True)
    grade = models.SmallIntegerField('امتیاز عملکرد', null= True , blank = True)
    # grade  =  models.ForeignKey(Lead, related_name="followup_grade", on_delete=models.CASCADE,null= True , blank = True)
    
    class Meta:
        verbose_name = 'پیگیری'
        verbose_name_plural = verbose_name


    def __str__(self):
        return f"{self.lead.customer_full_name}"




class Messages(models.Model):
    time = models.DateTimeField('زمان',auto_now_add=True)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE,verbose_name = 'سفارش')
    groupId = models.CharField('شناسه پیامک',null=True,blank=True,max_length=256)
    status = models.CharField('وضعیت پیامک',max_length=100,null=True,blank=True)
    STATUS_reviever_customer = 1
    STATUS_reviever_technician = 2
    status_choices = (
        (STATUS_reviever_customer, "مشتری"),
        (STATUS_reviever_technician, "تکنسین"),
    )
    reciever = models.IntegerField('دریافت کننده',choices=status_choices)

    class Meta:
        verbose_name = 'پیامک'
        verbose_name_plural = verbose_name
            
class Transaction(models.Model):
    technician = models.ForeignKey(Agent, on_delete=models.PROTECT,verbose_name = 'تکنسین')
    time = models.DateTimeField('زمان',auto_now_add=True)
    order = models.ForeignKey(Lead, on_delete=models.PROTECT, null=True,blank=True, verbose_name = 'سفارش')
    total_amount = models.DecimalField('دریافتی کل',max_digits=12, decimal_places=2)
    company_amount = models.PositiveIntegerField('سهم شرکت')
    STATUS_INCOME = "دریافتی از سفارش"
    STATUS_DEPOSITE =  "واریزی توسط تکنسین"
    status_choices = (
        (STATUS_INCOME, "دریافتی از سفارش"),
        (STATUS_DEPOSITE, "واریزی توسط تکنسین" ),
    )
    category = models.CharField('عنوان',choices=status_choices,max_length=32) 
    comment = models.TextField('کامنت',null=True,blank=True)

    # def save(self, *args, **kwargs):
    #     super(Transaction, self).save(*args, **kwargs)
    #     if self.category == "واریزی توسط تکنسین" and self.total_amount == company_amount:
    #         super(Transaction, self).save(*args, **kwargs)
            
	
    def __str__(self):
        return "%s"\
            % (self.id)
            
    class Meta:
        verbose_name= 'تراکنش'
        verbose_name_plural=verbose_name


    # def post_user_created_signal(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)


# post_save.connect(post_user_created_signal, sender=User)