from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from lbms_app.forms import ExpenseForm, LbmsUserChangeForm
from lbms_app.models import Category, Source, Expense, User


class LbmsUserAdmin(UserAdmin):
    form = LbmsUserChangeForm


class ExpenseAdmin(admin.ModelAdmin):
    form = ExpenseForm

    def get_form(self, request, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.user = request.user
        return form


admin.site.register(User, LbmsUserAdmin)
admin.site.register(Category)
admin.site.register(Source)
admin.site.register(Expense, ExpenseAdmin)
