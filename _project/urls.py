from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from _project.routes import urlpatterns as api_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urls)),
]

urlpatterns += staticfiles_urlpatterns()
