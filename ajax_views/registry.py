import json
import logging

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

logger = logging.getLogger('ajax_views')


class AjaxRegistry:
    def __init__(self):
        self._registry = {}

    def __iter__(self):
        return iter(self._registry)

    def register(self, name, func):
        if name in self._registry:
            logger.warning('view `%s` was already registered' % name)
        self._registry[name] = func

    def get(self, name):
        return self._registry.get(name)

    def to_json(self):
        data = {}
        for name in self._registry:
            path, _, key = name.rpartition('.')
            target = data
            for part in path.split('.'):
                target = target.setdefault(part, {})
            target[key] = reverse('ajax_views:router', args=[name])
        return json.dumps(data)


registry = AjaxRegistry()
