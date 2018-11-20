import logging
from django.template import Library
from django.utils.safestring import mark_safe
from ..registry import registry

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

try:
    import jinja2
except ImportError:
    jinja2 = None


register = Library()
logger = logging.getLogger('ajax_views')


@register.simple_tag(name='ajax_url')
def do_ajax_url(name):
    if name not in registry:
        logger.warning('view `%s` is not registered' % name)
    return reverse('ajax_views:router', kwargs={
        'name': name
    })


@register.simple_tag(name='ajax_views_json')
def ajax_views_json():
    return mark_safe(registry.to_json())


if jinja2 is not None:
    from jinja2.ext import Extension, nodes

    class AjaxViewsExtension(Extension):
        tags = {'ajax_views_json'}

        def parse(self, parser):
            lineno = next(parser.stream).lineno
            return nodes.CallBlock(self.call_method('_ajax_views_json'), [], [], []).set_lineno(lineno)

        @staticmethod
        def _ajax_views_json(caller):
            return registry.to_json()

    # Support django-jinja
    # https://github.com/niwinz/django-jinja
    try:
        from django_jinja.library import extension, global_function
    except ImportError:
        pass
    else:
        global_function(name='ajax_url')(do_ajax_url)
        extension(AjaxViewsExtension)