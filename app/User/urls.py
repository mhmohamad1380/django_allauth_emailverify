from django.urls import include, path
from . import views

urlpatterns = [
    path("login", views.login_page, name="login_view"),
    path("logout", views.logout_view, name="logout_view"),
    path("register", views.register_page, name="register_view"),
    path("user",views.email_verify,name="email_verify"),
]
