from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.datetime_safe import date

from lbms_app.models import Expense, Category, Source

User = get_user_model()


class CategoryChoiceField(forms.ModelChoiceField):
    def __init__(self, queryset, **kwargs):
        first_of_month = date.today().replace(day=1)

        queryset = queryset \
            .filter(add_date__lt=first_of_month) \
            .filter(Q(child_set=None) | Q(child_set__add_date__gt=first_of_month)) \
            .distinct() \
            .order_by('name')

        super().__init__(queryset, **kwargs)


class NoGroupForm(forms.ModelForm):
    class Meta:
        exclude = 'lbms_group',


class CategoryForm(NoGroupForm):
    class Meta(NoGroupForm.Meta):
        model = Category


class SourceForm(NoGroupForm):
    class Meta(NoGroupForm.Meta):
        model = Source


class ExpenseForm(NoGroupForm):
    class Meta(NoGroupForm.Meta):
        model = Expense
        field_classes = {
            'category': CategoryChoiceField
        }
