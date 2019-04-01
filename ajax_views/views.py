from django.http import HttpResponseNotFound
from .logging import logger
from .registry import registry


def router(request, name, *args, **kwargs):
    try:
        view = registry[name]
    except KeyError:
        logger.debug('Resolving "%s"...' % name)
        return HttpResponseNotFound()
    else:
        return view(request, *args, **kwargs)
