import django
from .registry import registry
from . import views


if django.VERSION >= (2, 0):
    from django.urls import URLPattern, ResolverMatch
    from django.urls.resolvers import RegexPattern

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
else:
    from django.core.urlresolvers import RegexURLPattern, ResolverMatch

    class AjaxURLPattern(RegexURLPattern):
        def resolve(self, path):
            match = self.regex.search(path)
            if match:
                kwargs = match.groupdict()
                view = registry.get(kwargs.pop('name'))
                if view is None:
                    return
                return ResolverMatch(view, (), kwargs, self.name)

    def ajax_url(regex, view, kwargs=None, name=None):
        return AjaxURLPattern(regex, view, kwargs, name)


app_name = 'ajax_views'
urlpatterns = [
    ajax_url('(?P<name>[-\w.]+)/', views.router, name='router'),
]
