from django.urls import reverse

from .logging import logger
from .registry import registry


def ajax_url(name):
    if name not in registry:
        logger.warning("view `%s` is not registered" % name)
    return reverse("ajax_views:router", kwargs={"name": name})
