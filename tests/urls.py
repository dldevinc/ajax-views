try:
    from django.urls import include, re_path
except:
    from django.conf.urls import include, url as re_path


urlpatterns = [
    re_path(r'^ajax/', include('ajax_views.urls', namespace='ajax_views')),
    re_path(r'', include('app.urls')),
]
