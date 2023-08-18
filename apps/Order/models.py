from django.db import models
from apps.EmdadUser.models import Technician, CustomUser
from apps.Emdad.models import Service, Motor, Product
from datetime import datetime
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    time = models.DateTimeField(_("time"), auto_now_add=True)
    services = models.ManyToManyField(Service, verbose_name=_('services'))
    motors = models.ManyToManyField(Motor, verbose_name=_('motors'))
    address = models.CharField(_('address'), max_length=100)
    customer_phone = models.CharField(_('customer call number'), max_length=20)
    customer_full_name = models.CharField(
        _('customer name'), max_length=100, null=True, blank=True)
    technecian = models.ForeignKey(
        Technician, on_delete=models.PROTECT, null=True, blank=True)
    WORKING = _('working')
    DONE = _('done')
    CANCELLATION = _('cancellation')
    CANCELED = _('canceled')

    status_choices = (
        ("w", WORKING),
        ("d", DONE),
        ('c', CANCELLATION),
        ("cc", CANCELED),
    )

    status = models.CharField(
        _("order's status"), max_length=15, choices=status_choices, default="w")
    grade = models.SmallIntegerField(
        _('grade'), null=True, blank=True, default=5)
    wage = models.PositiveIntegerField(_('wage'), default=0)
    commission = models.PositiveIntegerField(
        _('commission'), null=True, blank=True)
    expanse = models.PositiveIntegerField(_('expenses'), default=0)
    total_price_cusotmer = models.PositiveIntegerField(
        _('The final cost paid by the customer'), null=True, blank=True)

    comment = models.TextField(_('explanation'), null=True, blank=True)

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        db_table = 'Order'

    def __str__(self):
        return f"{self.pk}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True)
    number = models.SmallIntegerField(_('number'), null=True, blank=True)
    price = models.PositiveIntegerField(_('price'), null=True, blank=True)
    description = models.TextField(_('explanation'), null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'product'], name='unique_order_product')
        ]


class Followup(models.Model):
    time = models.DateTimeField(_('time'), auto_now_add=True)
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name="followups")
    notes = models.TextField(_('explanation'), null=True, blank=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, null=True)
    total_price_cusotmer = models.PositiveIntegerField(
        '', null=True, blank=True)
    total_wage_agent = models.PositiveIntegerField(
        _('total cost paid by customer'), null=True, blank=True)
    total_expanse_agent = models.PositiveIntegerField(
        _('total wage paid, declered by technician'), null=True, blank=True)
    grade = models.SmallIntegerField(_('grade'), null=True, blank=True)

    class Meta:
        verbose_name = _('followup')
        verbose_name_plural = _('followups')
        db_table = 'Followup'

    def __str__(self):
        return f"{self.user.full_name()} noted on {self.order}"
