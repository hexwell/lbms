from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Group(models.Model):
    name = models.CharField(max_length=100)


class Category(models.Model):
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    name = models.CharField(max_length=100, verbose_name=_('name'))
    group = models.ForeignKey(Group, on_delete=models.PROTECT, related_name='categories')
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='children',
        verbose_name=_('parent')
    )
    add_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent == self:
            raise ValidationError(_('Node cannot be a parent to itself'))

    def ancestors(self):
        if self.parent:
            yield from self.parent.ancestors()

        yield self


class Source(models.Model):
    class Meta:
        verbose_name = _('source')
        verbose_name_plural = _('sources')

    name = models.CharField(max_length=100, verbose_name=_('name'))
    group = models.ForeignKey(Group, on_delete=models.PROTECT, related_name='sources')

    def __str__(self):
        return self.name


class Expense(models.Model):
    class Meta:
        verbose_name = _('expense')
        verbose_name_plural = _('expenses')

    group = models.ForeignKey(Group, on_delete=models.PROTECT, related_name='expenses')
    amount = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_('amount (€)'))
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name=_('category'))
    source = models.ForeignKey(Source, on_delete=models.PROTECT, verbose_name=_('source'))
    date = models.DateField(default=date.today, verbose_name=_('date'))

    def __str__(self):
        return _('€ {amount} on {date} for {category} form {source}').format(
            amount=self.amount,
            date=self.date,
            category=self.category,
            source=self.source
        )
