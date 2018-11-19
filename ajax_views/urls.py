from django.urls import URLPattern, ResolverMatch
from django.urls.resolvers import RegexPattern
from .registry import registry
from . import views


class AjaxURLPattern(URLPattern):
    def resolve(self, path):
        match = self.pattern.match(path)
        if match:
            new_path, args, kwargs = match
            view = registry.get(kwargs.pop('name'))
            if view is None:
                return
            return ResolverMatch(view, args, kwargs, self.pattern.name)


def ajax_url(route, view, kwargs=None, name=None):
    pattern = RegexPattern(route, name=name, is_endpoint=True)
    return AjaxURLPattern(pattern, view, kwargs, name)


app_name = 'ajax_views'
urlpatterns = [
    ajax_url('(?P<name>[-\w.]+)/', views.router, name='router'),
]
