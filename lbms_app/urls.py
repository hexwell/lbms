from django.urls import re_path

from lbms_app.views import get_monthly_data, get_yearly_data, MonthlyStatsView, YearlyStatsView

app_name = 'lbms_app'

urlpatterns = [
    re_path(r'^data/m$', get_monthly_data, name='get_monthly_data'),
    re_path(r'^data/y$', get_yearly_data, name='get_yearly_data'),
    re_path(r'^stats/m$', MonthlyStatsView.as_view(), name='stats'),
    re_path(r'^stats/m$', MonthlyStatsView.as_view(), name='m_stats'),
    re_path(r'^stats/y$', YearlyStatsView.as_view(), name='y_stats'),
]
