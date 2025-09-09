from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Registration (custom view)
    path("register/", views.register, name="register"),

    # Login (Django built-in auth view, with custom template)
    path(
        "login/",
        LoginView.as_view(template_name="relationship_app/login.html"),
        name="login",
    ),

    # Logout (Django built-in auth view, with custom template)
    path(
        "logout/",
        LogoutView.as_view(template_name="relationship_app/logout.html"),
        name="logout",
    ),
]



