# ajax-views
A simple Django application to easily use AJAX views with JavaScript.

## Compatibility
* `django` >= 1.8, <=2.1
* `python` >= 3.3

## Features
* Ability to expose your AJAX URLs to JavaScript
* Support Function-Based and Class-Based Views
* One URL pattern ~~to rule them all~~ for all AJAX views
* Jinja2 support

## Installation
Install the package via Pip:

```
pip install git+git://github.com/dldevinc/ajax-views@v0.1.1#egg=ajax_views
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
Each view must have a **unique** name.

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

#### ... and use them
```javascript
$.ajax({
    url: window.ajax_views.myapp.form,
    ...
});
```

#### Combining with others decorators
```python
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ajax_views.decorators import ajax_view

@ajax_view('myapp.form')
@csrf_exempt
def form_view(request):
    ...

@ajax_view('myapp.form_cbv')
@method_decorator(csrf_exempt, name='dispatch')
class AjaxFormView(FormView):
    ...
```

## Jinja2 support
Make sure you have the [jinja2](http://jinja.pocoo.org/) package installed.

#### Export URLs from Django to JavaScript
```jinja2
<script>
    window.ajax_views = {% ajax_views_json %};
</script>
```

#### {{ ajax_url(...) }}
```jinja2
<form action="{{ ajax_url('myapp.form') }}" method="post">
    ...
</form>
```

## License
Copyright (c) 2018 Mihail Mishakin Released under the MIT license (see LICENSE)
