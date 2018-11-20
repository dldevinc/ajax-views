# ajax-views
A simple Django application to easily use AJAX views with JavaScript.

## Compatibility
* `django` >= 1.8
* `python` >= 3.3

## Features
* Ability to expose your AJAX URLs to JavaScript
* Support Function-Based and Class-Based Views
* One URL pattern ~~to rule them all~~ for all AJAX views
* Jinja2 support

## Installation
Install the package via Pip:

```
pip install ajax-views
```

Add it to your `INSTALLED_APPS` list:

```python
INSTALLED_APPS = (
    ...
    'ajax_views',
)
```

Add `ajax_views.urls` to your URLconf:

```python
urlpatterns = patterns('',
    ...
    
    # Django >= 2.0
    path('ajax/', include('ajax_views.urls')),
    
    # Django < 2.0
    url(r'^ajax/', include('ajax_views.urls', namespace='ajax_views')),
)
```

## Usage
#### @ajax_view
Use this decorator to register your views (Function-Based or Class-Based).
```python
from ajax_views.decorators import ajax_view

@ajax_view(name='myapp.form')
def form_view(request):
    ...

@ajax_view(name='myapp.form_cbv')
class AjaxFormView(FormView):
    ...
```
**NOTE**: Each view must have a **unique** name.

#### {% ajax_url %}
```djangotemplate
{% load ajax_views %}

<form action="{% ajax_url 'myapp.form' %}" method="post">
    ...
</form>
```

#### {% ajax_views_json %}
Template tag to render registered URLs as JSON.
```djangotemplate
{% load ajax_views %}

<script>
    window.ajax_views = {% ajax_views_json %};
</script>
```

```javascript
$.ajax({
    url: window.ajax_views.myapp.form,
    ...
});
```

#### Combining with other decorators
`@ajax_view` should be called **after** all decorators that returns a new function (such as `csrf_exempt`).
```python
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ajax_views.decorators import ajax_view

@ajax_view('example.fbv')
@csrf_exempt
def example_view(request):
    ...

@ajax_view('example.cbv')
@method_decorator(csrf_exempt, name='dispatch')
class ExampleView(View):
    ...
```

#### Multiple names for same view
```python
from ajax_views.decorators import ajax_view

@ajax_view(['myapp.form', 'myapp.fallback'])
def example_view(request):
    ...
```

## Jinja2 support
Enable Jinja2 extension
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'OPTIONS': {
            'extensions': [
                ...
                'ajax_views.templatetags.ajax_views.AjaxViewsExtension',
            ]
        }
    }
]
```

**NOTE**: If you are using [django-jinja](https://niwinz.github.io/django-jinja/latest/), you don't need to do this.

The usage is similar to Django, except `ajax_url` - it is global function:
```jinja2
<form action="{{ ajax_url('myapp.form') }}" method="post">
    ...
</form>
```

## License
Copyright (c) 2018 Mihail Mishakin Released under the MIT license (see LICENSE)
