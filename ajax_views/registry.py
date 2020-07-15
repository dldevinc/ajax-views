import re
from inspect import isclass, isfunction
from typing import Callable, Dict, Iterable, Optional, Union

from django.utils.module_loading import import_string
from django.views.generic import View

from .logging import logger

name_regex = re.compile(r'[-\w.]+')


class LazyView:
    __slots__ = ('path', 'initkwargs', 'view_func')

    def __init__(self, view_path: str, **initkwargs):
        self.path = view_path
        self.initkwargs = initkwargs
        self.view_func = None  # type: Optional[Callable]

    def __getattr__(self, item):
        if self.view_func is None:
            self.view_func = self._resolve()
            logger.debug('View "%s" instantiated.' % self.path)
        return getattr(self.view_func, item)

    def __call__(self, *args, **kwargs):
        if self.view_func is None:
            self.view_func = self._resolve()
            logger.debug('View "%s" instantiated.' % self.path)
        return self.view_func(*args, **kwargs)

    def _resolve(self) -> Callable:
        view = import_string(self.path)
        if isfunction(view):
            return view
        elif isclass(view) and issubclass(view, View):
            return view.as_view(**self.initkwargs)
        else:
            raise TypeError(view)


class Registry:
    __slots__ = ('_registry',)

    def __init__(self):
        self._registry = {}  # type: Dict[str, Callable]

    def __iter__(self):
        return iter(self._registry)

    def __getitem__(self, item):
        return self._registry[item]

    def register(
        self, names: Union[str, Iterable], view: Union[Callable, View], **initkwargs
    ):
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
                    "numbers, dots (.), dashes (-) and underscores (_)".format(name)
                )
            if name in self._registry:
                logger.warning('view `%s` was already registered.' % name)

        view_path = '.'.join((view.__module__, view.__qualname__))
        lazy_view = LazyView(view_path, **initkwargs)

        # assigning by reference
        for name in names:
            self._registry[name] = lazy_view


registry = Registry()
