from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Group(models.Model):
    name = models.CharField


class Category(models.Model):
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    name = models.CharField(max_length=100, verbose_name=_('name'))
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='children',
        verbose_name=_('parent')
    )

    add_date = models.DateField(auto_now_add=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.PROTECT,
        related_name='categories',
    )

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent == self:
            raise ValidationError(_('Node cannot be a parent to itself'))

    def ancestors(self):
        if self.parent:
            yield from self.parent.ancestors()

        yield self
