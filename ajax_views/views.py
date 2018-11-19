from django.http import HttpResponseNotFound
from .registry import registry


def router(request, name, *args, **kwargs):
    view = registry.get(name)
    if view is None:
        return HttpResponseNotFound()
    return view(request, *args, **kwargs)
