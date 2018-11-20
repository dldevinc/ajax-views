import logging

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


registry = AjaxRegistry()
