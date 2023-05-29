from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class LoginPage(TemplateView):
    http_method_names = ["get"]
    template_name = "users/login.html"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["name"] = "Amine"
        return context


class RegisterPage(TemplateView):
    http_method_names = ["get"]
    template_name = "users/register.html"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["name"] = "Amine"
        return context


class ChangePasswordPage(TemplateView):
    http_method_names = ["get"]
    template_name = "users/changePassword.html"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["name"] = "Amine"
        return context
