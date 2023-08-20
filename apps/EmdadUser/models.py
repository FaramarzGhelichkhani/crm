from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from apps.EmdadUser.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    phone = PhoneNumberField(_('phone'), region="IR", unique=True)
    email = models.EmailField(blank=True, null=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'CustomUser'


def technecian_handle_upload(instance, filename):
    filename = filename if not hasattr(instance, 'name') else instance.name
    pk = instance.pk if not hasattr(instance, 'name') else instance.tech_id.pk
    return f"Technecian_files/Tec_{pk}/{filename}"


class Technician(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.DO_NOTHING, verbose_name=_('user'))
    id_card = models.CharField(
        _('id card'), max_length=10, null=True, blank=True)
    address = models.CharField(_('address'), max_length=320)
    commission = models.FloatField(_('commission'), default=0.2)
    balance = models.IntegerField(_('debt'), default=0)
    time_shift = models.CharField(_('time shift'), max_length=100)
    comment = models.TextField(_('explanation'), null=True, blank=True)

    STATUS_ACTIVE = _('active')
    STATUS_INACTIVE = _('inactive')
    STATUS_BANN = _('bann')

    status_choices = (
        (1, STATUS_ACTIVE),
        (2, STATUS_INACTIVE),
        (3, STATUS_BANN),
    )
    activation_status = models.IntegerField(
        _('status'), choices=status_choices, default=1)
    avatar = models.ImageField(
        null=True, blank=True, upload_to=technecian_handle_upload)

    class Meta:
        verbose_name = _('technician')
        verbose_name_plural = _('technicians')
        db_table = 'Technician'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Techdoc(models.Model):
    technician = models.ForeignKey(
        Technician, on_delete=models.PROTECT, verbose_name=_('technician'))
    name = models.CharField(
        _('file name'), max_length=150, null=True, blank=True)
    file = models.FileField(null=True, blank=True,
                            upload_to=technecian_handle_upload)

    def __str__(self):
        return f"{self.name}_{self.tech_id.first_name} {self.tech_id.last_name}"

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')
        db_table = 'Techdoc'
