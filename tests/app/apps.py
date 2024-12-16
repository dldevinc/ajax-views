from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Config(AppConfig):
    name = "app"
    verbose_name = _("App")

    def ready(self):
        from . import views
