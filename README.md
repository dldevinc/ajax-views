# ajax-views
A simple AJAX framework for Django

Requirements
------------
* `python` >= 3.4
* `django` >= 1.8

Installation
------------
Install the package via Pip:

```
pip install git+git://github.com/dldevinc/ajax-views#egg=ajax_views
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
    url(r'^ajax/', include('ajax_views.urls')),
)
```

Usage
-----

**@ajax_view decorator**
```python
from ajax_views.decorators import ajax_view

@ajax_view(name='myapp.form')
def form_view(request):
    ...
    
# CBV also supported
@ajax_view(name='myapp.form_cbv')
class AjaxFormView(FormView):
    ...
```
Each view must have a **unique** name.

**{% ajax_url %} template tag**
```djangotemplate
{% load ajax_views %}

<form action="{% ajax_url 'myapp.form' %}" method="post">
    ...
</form>
```

**Export URLs from Django to JavaScript**
```djangotemplate
{% load ajax_views %}

<script>
    window.ajax_views={% ajax_views_json %};
</script>
```

**... and use them**
```javascript
$.ajax({
    url: window.ajax_views.myapp.form,
    ...
});
```

**Combining with others decorators**
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

Jinja2 support
--------------
Make sure you have the [jinja2](http://jinja.pocoo.org/) package installed.

**Export URLs from Django to JavaScript**
```jinja2
<script>
    window.ajax_views={% ajax_views_json %};
</script>
```

**{{ ajax_url(...) }} template function**
```jinja2
<form action="{{ ajax_url('myapp.form') }}" method="post">
    ...
</form>
```

## License
Copyright (c) 2018 Mihail Mishakin Released under the MIT license (see LICENSE)
