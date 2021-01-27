from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from lbms_app.forms import ExpenseForm, CategoryForm, SourceForm
from lbms_app.models import Category, Source, Expense, User


class LbmsUserAdmin(UserAdmin):
    pass

LbmsUserAdmin.fieldsets[0][1]['fields'] += ('lbms_group',)
LbmsUserAdmin.add_fieldsets[0][1]['fields'] += ('lbms_group',)
admin.site.register(User, LbmsUserAdmin)
admin.site.site_header = 'LBMS'
admin.site.site_title = 'LBMS'
admin.site.index_title = _("Welcome to the LBMS app")
admin.site.site_url = '/stats'  # TODO reverse('lbms_app:stats')


class GroupModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        q = super(GroupModelAdmin, self).get_queryset(request)
        return q.filter(lbms_group=request.user.lbms_group)

    def get_form(self, request, *args, **kwargs):
        OldForm = super().get_form(request, *args, **kwargs)

        class TempForm(OldForm):
            def __init__(obj, *a, **ka):
                obj.lbms_group = request.user.lbms_group

                super().__init__(*a, **ka)

                obj.instance.lbms_group = obj.lbms_group

        return TempForm


@admin.register(Category)
class CategoryAdmin(GroupModelAdmin):
    form = CategoryForm


@admin.register(Source)
class SourceAdmin(GroupModelAdmin):
    form = SourceForm


@admin.register(Expense)
class ExpenseAdmin(GroupModelAdmin):
    form = ExpenseForm
