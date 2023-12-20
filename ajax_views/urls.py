import django
from django.urls import ResolverMatch, URLPattern
from django.urls.resolvers import RegexPattern

from .registry import registry
from .views import router

if django.VERSION >= (4, 1):  # noqa
    class AjaxURLPattern(URLPattern):
        def resolve(self, path):
            match = self.pattern.match(path)
            if match:
                new_path, args, captured_kwargs = match
                # Pass any default args as **kwargs.
                kwargs = {**captured_kwargs, **self.default_args}

                name = kwargs.pop("name")
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
else:
    class AjaxURLPattern(URLPattern):
        def resolve(self, path):
            match = self.pattern.match(path)
            if match:
                new_path, args, kwargs = match

                name = kwargs.pop("name")
                if name not in registry:
                    return

                view = registry[name]
                return ResolverMatch(
                    view, args, kwargs, self.pattern.name, route=str(self.pattern)
                )

    def ajax_url(regex, view, kwargs=None, name=None):
        pattern = RegexPattern(regex, name=name, is_endpoint=True)
        return AjaxURLPattern(pattern, view, kwargs, name)


app_name = "ajax_views"
urlpatterns = [
    ajax_url(r"(?P<name>[-\w.]+)/", router, name="router"),
]
