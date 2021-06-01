from django.conf.urls import url

from lbms_app.views import get_monthly_data, get_yearly_data, MonthlyStatsView, YearlyStatsView

app_name = 'lbms_app'

urlpatterns = [
    url(r'^data/m$', get_monthly_data, name='get_monthly_data'),
    url(r'^data/y$', get_yearly_data, name='get_yearly_data'),
    url(r'^stats/m$', MonthlyStatsView.as_view(), name='stats'),
    url(r'^stats/m$', MonthlyStatsView.as_view(), name='m_stats'),
    url(r'^stats/y$', YearlyStatsView.as_view(), name='y_stats'),
]
