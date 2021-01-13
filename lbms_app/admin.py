from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from lbms_app.models import Category, Source, Expense, User

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Source)
admin.site.register(Expense)  # , ExpenseAdmin)
