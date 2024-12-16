# ajax-views

A simple Django application to easily use AJAX views with JavaScript.

[![PyPI](https://img.shields.io/pypi/v/ajax-views.svg)](https://pypi.org/project/ajax-views/)
[![Build Status](https://github.com/dldevinc/ajax-views/actions/workflows/tests.yml/badge.svg)](https://github.com/dldevinc/ajax-views)
[![Software license](https://img.shields.io/pypi/l/ajax-views.svg)](https://pypi.org/project/ajax-views/)

## Compatibility

-   `django` >= 3.2
-   `python` >= 3.9

## Features

-   Ability to expose your AJAX URLs to JavaScript
-   Supported Function-Based and Class-Based Views
-   One URL pattern ~~to rule them all~~ for all AJAX views
-   Jinja2 support

## Installation

Install the package via Pip:

```
pip install ajax-views
```

Add it to your `INSTALLED_APPS` list:

```python
INSTALLED_APPS = (
    # ...
    "ajax_views",
    # ...
)
```

Add `ajax_views.urls` to your URLconf:

```python
from django.urls import include, path

urlpatterns = [
    path("ajax/", include("ajax_views.urls")),
]
```

## Usage

#### @ajax_view("name")

Use this decorator to register your views (Function-Based or Class-Based).

```python
from ajax_views.decorators import ajax_view

@ajax_view("myapp.form")
def form_view(request):
    ...

@ajax_view("myapp.form_cbv")
class AjaxFormView(FormView):
    ...
```

**NOTE**: The specified name has to be unique.

You can combine `ajax_view` with other decorators:

```python
@csrf_exempt
@require_POST
@ajax_view("myapp.contact_form")
def csrf_exempt_view(request):
    # ...
```

#### {% ajax_views_json %}

Template tag to output registered URLs as JSON.

```djangotemplate
{% load ajax_views %}

<script>
    window.ajax_views = {% ajax_views_json %};
</script>
```

Now you can use the declared object to refer to the corresponding urls like this:

```javascript
$.ajax({
    url: window.ajax_views.myapp.form,
    ...
});
```

#### {% ajax_url 'name' %}

This tag is used to add AJAX URLs in the template files:

```djangotemplate
{% load ajax_views %}

<form action="{% ajax_url 'myapp.form' %}" method="post">
    ...
</form>
```

#### Multiple names

You can have multiple names for the same view:

```python
from ajax_views.decorators import ajax_view

@ajax_view(["myapp.form", "myapp.fallback"])
def example_view(request):
    ...
```

## Jinja2 support

Enable Jinja2 extension

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "OPTIONS": {
            "extensions": [
                # ...
                "ajax_views.templatetags.ajax_views.AjaxViewsExtension",
            ]
        }
    }
]
```

**NOTE**: If you are using [django-jinja](https://niwinz.github.io/django-jinja/latest/), you don't need to do this.

The usage is similar to Django, except that `ajax_url` is a global function:

```jinja2
<form action="{{ ajax_url('myapp.form') }}" method="post">
    ...
</form>
```

## Development and Testing

After cloning the Git repository, you should install this
in a virtualenv and set up for development:

```shell script
virtualenv .venv
source .venv/bin/activate
pip install -r ./requirements.txt
pre-commit install
```
