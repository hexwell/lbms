from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LbmsAppConfig(AppConfig):
    name = 'lbms_app'
    verbose_name = _('expenses')
