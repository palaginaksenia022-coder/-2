from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    path("test/", lambda request: HttpResponse("Тест работает"), name="test"),
    path("", views.index, name="index"),
    path("admin/login/", views.admin_login_view, name="admin_login"),
    path("admin/panel/", views.admin_panel, name="admin_panel"),
    path("admin/logout/", views.admin_logout_view, name="admin_logout"),
]
