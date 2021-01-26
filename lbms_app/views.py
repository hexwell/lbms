from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from lbms_app.models import Expense, Category, Source
from utils import lul


def expense_sum(expenses):
    return sum(expense.amount for expense in expenses)


def month_expenses(group, year, month):
    return Expense.objects.filter(lbms_group=group, date__year=year, date__month=month)


def total_source_category(expenses, group):
    categories = set(expense.category for expense in expenses)
    hierarchies = lul.hierarchies_by_root(categories, Category.ancestors)
    luls = lul.mapdict(lambda cats: lul.lul(cats, Category.ancestors), hierarchies)
    buckets = lul.buckets(luls, categories, Category.ancestors)

    return {
        'total': expense_sum(expenses),

        'by_category': {
            category.name: expense_sum(expenses.filter(category__in=buckets[category]))
            for category in buckets
        },

        'by_source': {
            source.name: expense_sum(expenses.filter(source=source))
            for source in Source.objects.filter(lbms_group=group)
        },
    }


@login_required
def get_monthly_data(request):
    year, month = 2021, 1

    # noinspection PyUnresolvedReferences
    group = request.user.lbms_group
    month_expenses_ = month_expenses(group, year, month)

    return JsonResponse({
        **total_source_category(month_expenses_, group),
    })


@login_required
def get_yearly_data(request):
    year = 2021

    # noinspection PyUnresolvedReferences
    group = request.user.lbms_group
    year_expenses = Expense.objects.filter(lbms_group=group, date__year=year)

    return JsonResponse({
        **total_source_category(year_expenses, group),

        'by_month': {
            month: expense_sum(month_expenses(group, year, month))
            for month in range(1, 12 + 1)
        }
    })
