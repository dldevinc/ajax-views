import logging

logger = logging.getLogger('ajax_views')


class Registry:
    def __init__(self):
        self._registry = {}

    def __iter__(self):
        return iter(self._registry)

    def register(self, name, view):
        if name in self._registry:
            logger.warning('view `%s` was already registered.' % name)
        self._registry[name] = view

    def get(self, name):
        return self._registry[name]


registry = Registry()
