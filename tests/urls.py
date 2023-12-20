from django.urls import include, path


urlpatterns = [
    path("ajax/", include("ajax_views.urls")),
    path("", include("app.urls")),
]
