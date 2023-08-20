from django.db import models
from apps.EmdadUser.models import Technician
from django.utils.translation import gettext_lazy as _


class Service(models.Model):
    name = models.CharField(_('name of service'), max_length=150)
    min_price = models.IntegerField(_('minimum price'), default=250000)
    max_price = models.IntegerField(_('maximum price'), default=250000)

    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0

    status_choices = (
        (STATUS_ACTIVE,     _('active')),
        (STATUS_INACTIVE,   _('inactive')),
    )

    activation_status = models.IntegerField(
        _('status'), choices=status_choices, default=STATUS_ACTIVE)
    technecians = models.ManyToManyField(Technician, null=True, blank=True)
    comment = models.TextField(_('explanation'), null=True, blank=True)

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')
        db_table = 'Service'

    def __str__(self):
        return f"{self.name}"


class Region(models.Model):
    city = models.CharField(_('city'), max_length=150)
    area = models.CharField(_('area'), max_length=150)

    STATUS_ACTIVE = _('active')
    STATUS_INACTIVE = _('inactive')

    status_choices = (
        (1, STATUS_ACTIVE),
        (0, STATUS_INACTIVE),
    )
    activation_status = models.IntegerField(
        _('status'), choices=status_choices, default=1)
    technecians = models.ManyToManyField(Technician,  null=True, blank=True)

    class Meta:
        verbose_name = _('region')
        verbose_name_plural = _('regions')
        db_table = 'Region'

    def __str__(self):
        return f"{self.city} {self.area}"


class Motor(models.Model):
    company = models.CharField(
        _('company'), max_length=150, null=True, blank=True)
    brand = models.CharField(_('brand'), max_length=150)
    model = models.CharField(_('model'), max_length=150, null=True, blank=True)
    year = models.CharField(_('year of construction'),
                            max_length=5, null=True, blank=True)

    INJECTOR = _('injector')
    CARBURETOER = _('carburetoer')

    status_choices = (
        (1, INJECTOR),
        (2, CARBURETOER),
    )
    engine_type = models.IntegerField(
        _('engine type'), choices=status_choices, default=1)
    technecians = models.ManyToManyField(Technician,  null=True, blank=True)

    class Meta:
        verbose_name = _('motor')
        verbose_name_plural = _('motors')
        db_table = 'Motor'

    def __str__(self):
        return f"{self.brand}"


class Product(models.Model):
    name = models.CharField(_('name of product'), max_length=150)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        db_table = 'Product'

    def __str__(self):
        return f"{self.name}"
