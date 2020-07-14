try:
    from django.urls import re_path
except:
    from django.conf.urls import url as re_path
from .views import IndexView


app_name = 'app'
urlpatterns = [
    re_path(r'^$', IndexView.as_view()),
]
