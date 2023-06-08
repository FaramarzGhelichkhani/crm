from django.contrib.auth.models import Group, PermissionsMixin,AbstractBaseUser, Permission
from django.db import models
from django.utils import timezone
# from phonenumber_field.modelfields import PhoneNumberField
from .managers import CustomUserManager, generate_password


class CustomUser(AbstractBaseUser, PermissionsMixin):  
    username    = None 
    raw_password =  models.CharField(' گذرواژه خام',max_length=6)
    first_name 	= models.CharField('نام',max_length=100)
    last_name 	= models.CharField('نام خانوادگی',max_length=100) 
    phone       = models.CharField('شماره تماس',max_length=11, unique=True)
    email       = models.EmailField('ایمیل',blank=True,null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff    = models.BooleanField(default=False)  
    is_active   = models.BooleanField(default=True)  
          
    USERNAME_FIELD = 'phone'  
    REQUIRED_FIELDS= []  
      
    objects = CustomUserManager() 

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_users_groups'  # Add or change the related_name here
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_users_permissions'  # Add or change the related_name here
    )
                
    @property  
    def is_admin(self):  
        "Is the user a admin member?"  
        return self.is_superuser  
    
    def __str__(self):  
        return self.full_name() 
    
    def full_name(self):  
        return f"{self.first_name} {self.last_name}"
    

    # def save(self, *args, **kwargs):
    #     if not self.pk:  # Check if it's a new user
    #         password = generate_password(6)
    #         self.raw_password = password
    #         self.set_password(password)
    #     super().save(*args, **kwargs)
        


def Technecian_handle_upload(instance,filename):
    filename = filename if not hasattr(instance,'name') else instance.name
    pk       = instance.pk if not hasattr(instance,'name') else instance.tech_id.pk 
    return f"Technecian_files/Tec_{pk}/{filename}"

class Technecian(models.Model):
    user_id    = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name = 'کاربر')
    id_card    = models.CharField('کد ملی',max_length=10, null=True,blank=True)
    address    = models.CharField('آدرس',max_length=320)
    commission = models.FloatField('کارمزد',default=0.2)
    balance    = models.IntegerField('بدهی ',default=0)
    time_shift  = models.CharField(' شیفت کاری',max_length=100)
    comment    = models.TextField('توضیحات',null=True, blank=True)

    STATUS_active = 1
    STATUS_deactive = 2
    STATUS_ban = 3
    status_choices = (
        (STATUS_active, "فعال"),
        (STATUS_deactive, "غیرفعال"),
        (STATUS_ban, "تعلیق"),
    )
    activation_status = models.IntegerField('وضعیت',choices=status_choices, default = 1)
    avatar            = models.ImageField(null=True, blank=True,upload_to=Technecian_handle_upload)


    class Meta:
        verbose_name = 'کارشناس'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user_id.first_name} {self.user_id.last_name}"
      
    
class Tech_doc(models.Model):
    tech_id = models.ForeignKey(Technecian, on_delete=models.PROTECT, verbose_name = 'کارشناس')
    name    = models.CharField('نام فایل',max_length=150, null=True,blank=True)
    file    = models.FileField(null=True, blank=True, upload_to=Technecian_handle_upload) 

    def __str__(self):
        return f"{self.name}_{self.tech_id.first_name} {self.tech_id.last_name}"

    class Meta:
        verbose_name = 'مدارک'
        verbose_name_plural = verbose_name