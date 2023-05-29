from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View

from utils.parseBody import parseBody


# Create your views here.
class RegisterPage(View):
    def get(self, req):
        return render(req, "users/register.html")

    def post(self, req):
        res = parseBody(req.body)
        username = res["username"]
        password = res["password"]
        confirmPassword = res["confirmPassword"]
        rememberMe = res["rememberMe"]  # on OR off
        return redirect("/")


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
