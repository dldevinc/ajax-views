import json
from typing import Any, Dict

from django.template import Library
from django.urls import reverse
from django.utils.safestring import mark_safe

from .. import helpers
from ..registry import registry

try:
    import jinja2
except ImportError:
    jinja2 = None


register = Library()


def registry_to_json():
    data = {}  # type: Dict[str, Any]
    for name in registry:
        target = data
        path, _, key = name.rpartition('.')
        if path:
            for part in path.split('.'):
                target = target.setdefault(part, {})
        target[key] = reverse("ajax_views:router", args=[name])
    return json.dumps(data)


@register.simple_tag(name="ajax_url")
def do_ajax_url(name):
    return helpers.ajax_url(name)


@register.simple_tag(name="ajax_views_json")
def ajax_views_json():
    return mark_safe(registry_to_json())


if jinja2 is not None:
    from jinja2 import nodes
    from jinja2.ext import Extension

    class AjaxViewsExtension(Extension):
        tags = {"ajax_views_json"}

        def parse(self, parser):
            lineno = next(parser.stream).lineno
            return nodes.CallBlock(
                self.call_method("_ajax_views_json"), [], [], []
            ).set_lineno(lineno)

        @staticmethod
        def _ajax_views_json(caller):
            return registry_to_json()

    # django-jinja support
    try:
        from django_jinja import library
    except ImportError:
        pass
    else:
        library.global_function(name="ajax_url")(do_ajax_url)
        library.extension(AjaxViewsExtension)
