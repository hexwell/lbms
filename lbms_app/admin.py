from django.contrib import admin

from lbms_app.models import Category, Source, Expense, UserGroup

admin.site.register(UserGroup)
admin.site.register(Category)
admin.site.register(Source)
admin.site.register(Expense)  # , ExpenseAdmin)
