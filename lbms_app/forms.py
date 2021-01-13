from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.db.models import Q
from django.forms import ModelChoiceField
from django.utils.datetime_safe import date

from lbms_app.models import Expense, Group

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


class LbmsUserChangeForm(UserChangeForm):
    group = ModelChoiceField(queryset=Group.objects.all())


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = 'group',
        field_classes = {
            'category': CategoryChoiceField
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs['users']
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super().save(False)
        obj.group = self.user.group

        if commit:
            obj.save()

        return obj
