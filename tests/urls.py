from django.conf.urls import url, include
from .app import views

urlpatterns = [
    url(r'^ajax/', include('ajax_views.urls', namespace='ajax_views')),
]
