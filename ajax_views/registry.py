import re
from inspect import isfunction, isclass
from django.views.generic import View
from django.utils.module_loading import import_string
from .logging import logger

name_regex = re.compile(r'[-\w.]+')


class LazyView:
    __slots__ = ('path', 'initkwargs', 'view_func')

    def __init__(self, view_path, **initkwargs):
        self.path = view_path
        self.initkwargs = initkwargs
        self.view_func = None

    def __getattr__(self, item):
        if self.view_func is None:
            self._resolve()
        return getattr(self.view_func, item)

    def __call__(self, *args, **kwargs):
        if self.view_func is None:
            self._resolve()
        return self.view_func(*args, **kwargs)

    def _resolve(self):
        view = import_string(self.path)
        if isfunction(view):
            self.view_func = view
        elif isclass(view) and issubclass(view, View):
            self.view_func = view.as_view(**self.initkwargs)
        else:
            raise TypeError(view)
        logger.debug('View "%s" instantiated.' % self.path)


class Registry:
    __slots__ = ('_registry', )

    def __init__(self):
        self._registry = {}

    def __iter__(self):
        return iter(self._registry)

    def __getitem__(self, item):
        return self._registry[item]

    def register(self, names, view, **initkwargs):
        """
        :type names: str | list | tuple
        :type view: types.FunctionType | django.views.generic.View
        """
        if isinstance(names, str):
            names = [names]

        # check names
        for name in names:
            if not name_regex.fullmatch(name):
                raise ValueError(
                    "Invalid view name: '{}'. Names must contain only letters, "
                    "numbers, dots (.), dashes (-) and underscores (_)".format(
                        name
                    )
                )
            if name in self._registry:
                logger.warning('view `%s` was already registered.' % name)

        view_path = '.'.join((view.__module__, view.__qualname__))
        lazy_view = LazyView(view_path, **initkwargs)

        # assigning by reference
        for name in names:
            self._registry[name] = lazy_view


registry = Registry()
