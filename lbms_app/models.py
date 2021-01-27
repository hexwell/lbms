from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class NamedMixin(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=100, verbose_name=_('name'))


class Group(NamedMixin):
    def __str__(self):
        return self.name


class GroupMixin(models.Model):
    class Meta:
        abstract = True

    lbms_group = models.ForeignKey(Group, on_delete=models.CASCADE)


class User(AbstractUser, GroupMixin):
    lbms_group = models.ForeignKey(Group, on_delete=models.PROTECT)


class Category(NamedMixin, GroupMixin):
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        related_name='child_set',  # TODO in queries, children would look better
        # TODO check if related query name is required
        verbose_name=_('parent')
    )
    add_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent:
            if self in self.parent.ancestors():
                raise ValidationError(_('Parent and child nodes cannot be the same, or have a cyclic relationship.'))

            if self.parent.lbms_group != self.lbms_group:
                raise ValidationError('Parent and child must have the same group')

    def ancestors(self):
        if self.parent:
            yield from self.parent.ancestors()

        yield self


class Source(NamedMixin, GroupMixin):
    class Meta:
        verbose_name = _('source')
        verbose_name_plural = _('sources')

    def __str__(self):
        return self.name


class Expense(GroupMixin):
    class Meta:
        verbose_name = _('expense')
        verbose_name_plural = _('expenses')

    amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_('amount') + ' (€)',
                                 validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, verbose_name=_('category'))
    source = models.ForeignKey(Source, on_delete=models.RESTRICT, verbose_name=_('source'))
    date = models.DateField(default=date.today, verbose_name=_('date'))

    def clean(self):
        if not all((
                hasattr(self, 'lbms_group', ),
                hasattr(self, 'source'),
                hasattr(self, 'category')
        )):
            raise ValidationError(_('Required fields missing.'))

        if not (self.lbms_group == self.source.lbms_group == self.category.lbms_group):
            raise ValidationError('Expense, source and category must have the same group')

    def __str__(self):
        return _('€ {amount} on {date} for {category} form {source}').format(
            amount=self.amount,
            date=self.date,
            category=self.category,
            source=self.source
        )
