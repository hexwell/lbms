from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from lbms_app.forms import ExpenseForm, CategoryForm, SourceForm
from lbms_app.models import Category, Source, Expense, User


class LbmsUserAdmin(UserAdmin):
    pass


LbmsUserAdmin.fieldsets[0][1]['fields'] += ('lbms_group',)
LbmsUserAdmin.add_fieldsets[0][1]['fields'] += ('lbms_group',)


class GroupModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, *args):
        obj.group = request.user.lbms_group

        super().save_model(request, obj, *args)


class CategoryAdmin(GroupModelAdmin):
    form = CategoryForm


class SourceAdmin(GroupModelAdmin):
    form = SourceForm


class ExpenseAdmin(GroupModelAdmin):
    form = ExpenseForm


admin.site.register(User, LbmsUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Expense, ExpenseAdmin)
