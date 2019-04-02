from .registry import registry


def ajax_view(name, **initkwargs):
    def decorator(view):
        registry.register(name, view, **initkwargs)
        return view
    return decorator
