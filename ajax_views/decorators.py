import re
from inspect import isfunction, isclass
from django.views.generic import View
from .registry import registry

name_regex = re.compile(r'[-\w:.]+')


def _check_name(name):
    if not name_regex.fullmatch(name):
        raise ValueError(
            "Invalid view name: '{}'. "
            "Names must contain only letters, numbers, dots (.), dashes (-) and underscores (_)".format(
                name
            )
        )


def ajax_view(name):
    def decorator(view):
        if isclass(view) and issubclass(view, View):
            view = view.as_view()
        elif isfunction(view):
            pass
        else:
            raise TypeError(view)

        for name in names:
            registry.register(name, view)
        return view

    names = [name] if not isinstance(name, (tuple, list)) else name
    for name in names:
        _check_name(name)
    return decorator
