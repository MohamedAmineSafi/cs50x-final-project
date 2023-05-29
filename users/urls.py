from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginPage.as_view(), name="login"),
    path("register/", views.RegisterPage.as_view(), name="register"),
    path("changePassword/", views.ChangePasswordPage.as_view(), name="changePassword"),
]
