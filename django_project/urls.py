from django.urls import path, include
from monitor.admin import custom_admin_site

urlpatterns = [
    path("admin/", custom_admin_site.urls),
    path("", include("monitor.urls")),
]
