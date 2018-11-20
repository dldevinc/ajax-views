from django.http import HttpResponseNotFound
from .registry import registry


def router(request, name, *args, **kwargs):
    if name not in registry:
        return HttpResponseNotFound()
    return registry.get(name)(request, *args, **kwargs)
