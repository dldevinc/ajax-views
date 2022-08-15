import django

from .registry import registry
from .views import router

if django.VERSION >= (4, 1):  # noqa
    from django.urls import ResolverMatch, URLPattern
    from django.urls.resolvers import RegexPattern

    class AjaxURLPattern(URLPattern):
        def resolve(self, path):
            match = self.pattern.match(path)
            if match:
                new_path, args, captured_kwargs = match
                # Pass any default args as **kwargs.
                kwargs = {**captured_kwargs, **self.default_args}

                name = kwargs.pop('name')
                if name not in registry:
                    return

                view = registry[name]
                return ResolverMatch(
                    view,
                    args,
                    kwargs,
                    self.pattern.name,
                    route=str(self.pattern),
                    captured_kwargs=captured_kwargs,
                    extra_kwargs=self.default_args,
                )

    def ajax_url(regex, view, kwargs=None, name=None):
        pattern = RegexPattern(regex, name=name, is_endpoint=True)
        return AjaxURLPattern(pattern, view, kwargs, name)


elif django.VERSION >= (2, 2):  # noqa
    from django.urls import ResolverMatch, URLPattern
    from django.urls.resolvers import RegexPattern

    class AjaxURLPattern(URLPattern):
        def resolve(self, path):
            match = self.pattern.match(path)
            if match:
                new_path, args, kwargs = match

                name = kwargs.pop('name')
                if name not in registry:
                    return

                view = registry[name]
                return ResolverMatch(
                    view, args, kwargs, self.pattern.name, route=str(self.pattern)
                )

    def ajax_url(regex, view, kwargs=None, name=None):
        pattern = RegexPattern(regex, name=name, is_endpoint=True)
        return AjaxURLPattern(pattern, view, kwargs, name)


elif django.VERSION >= (2, 0):
    from django.urls import ResolverMatch, URLPattern
    from django.urls.resolvers import RegexPattern

    class AjaxURLPattern(URLPattern):  # type: ignore
        def resolve(self, path):
            match = self.pattern.match(path)
            if match:
                new_path, args, kwargs = match

                name = kwargs.pop('name')
                if name not in registry:
                    return

                view = registry[name]
                return ResolverMatch(view, args, kwargs, self.pattern.name)

    def ajax_url(regex, view, kwargs=None, name=None):
        pattern = RegexPattern(regex, name=name, is_endpoint=True)
        return AjaxURLPattern(pattern, view, kwargs, name)


else:
    from django.core.urlresolvers import RegexURLPattern, ResolverMatch

    class AjaxURLPattern(RegexURLPattern):  # type: ignore
        def resolve(self, path):
            match = self.regex.search(path)
            if match:
                kwargs = match.groupdict()
                name = kwargs.pop('name')
                if name not in registry:
                    return
                view = registry[name]
                return ResolverMatch(view, (), kwargs, self.name)

    def ajax_url(regex, view, kwargs=None, name=None):
        return AjaxURLPattern(regex, view, kwargs, name)


app_name = 'ajax_views'
urlpatterns = [
    ajax_url(r'(?P<name>[-\w.]+)/', router, name='router'),
]
