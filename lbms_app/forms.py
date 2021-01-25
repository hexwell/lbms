from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.datetime_safe import date
from django.utils.translation import gettext as _

from lbms_app.models import Expense, Category, Source

User = get_user_model()


class NoGroupForm(forms.ModelForm):
    class Meta:
        exclude = 'lbms_group',


class CategoryForm(NoGroupForm):
    class Meta(NoGroupForm.Meta):
        model = Category

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        queryset = CategoryForm.Meta.model.objects \
            .filter(lbms_group=self.lbms_group) \
            .order_by('name')

        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        self.fields['parent'] = forms.ModelChoiceField(queryset, required=False, label=_('parent').title())


class SourceForm(NoGroupForm):
    class Meta(NoGroupForm.Meta):
        model = Source


class ExpenseForm(NoGroupForm):
    class Meta(NoGroupForm.Meta):
        model = Expense

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        first_of_month = date.today().replace(day=1)

        category_queryset = Category.objects \
            .filter(lbms_group=self.lbms_group) \
            .filter(add_date__lt=first_of_month) \
            .filter(Q(child_set=None) | Q(child_set__add_date__gt=first_of_month)) \
            .order_by('name')

        source_queryset = Source.objects \
            .filter(lbms_group=self.lbms_group) \
            .order_by('name')

        self.fields['category'] = forms.ModelChoiceField(category_queryset, label=_('category').title())
        self.fields['source'] = forms.ModelChoiceField(source_queryset, label=_('source').title())
