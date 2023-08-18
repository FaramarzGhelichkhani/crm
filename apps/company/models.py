from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _ 

class Expend(models.Model):
    time = models.DateTimeField(_('time'), null=True, blank=True, default=timezone.now)
    amount = models.PositiveIntegerField(_('amount'))
    comment = models.CharField(_('title'), max_length=320)

    class Meta:
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')
        db_table = 'Expense'
