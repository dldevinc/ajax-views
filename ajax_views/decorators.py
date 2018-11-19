import re
from inspect import isclass, isfunction
from .registry import registry

name_regex = re.compile(r'[-\w.]+')


def ajax_view(name):
    def decorator(view):
        if isclass(view):   # CBV
            view = view.as_view()
        elif isfunction(view):
            pass
        else:
            raise TypeError(view)

        registry.register(name, view)
        return view

    if not name_regex.fullmatch(name):
        raise ValueError('name must contain only letters, numbers, dots (.), dashes (-) and underscores (_)')
    return decorator
