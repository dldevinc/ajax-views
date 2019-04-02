SECRET_KEY = 'fake-key'

INSTALLED_APPS = [
    "ajax_views",
    "tests",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

ROOT_URLCONF = 'tests.urls'
