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


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = 'group',


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        exclude = 'group',


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = 'group',
        field_classes = {
            'category': CategoryChoiceField
        }
