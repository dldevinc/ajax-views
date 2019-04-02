from django.conf.urls import url, include

urlpatterns = [
    url(r'^ajax/', include('ajax_views.urls', namespace='ajax_views')),
]
