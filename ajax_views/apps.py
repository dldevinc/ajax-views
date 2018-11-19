from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Config(AppConfig):
    name = 'ajax_views'
    verbose_name = _('AJAX Views')
