from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from .models import User
import hashlib

from utils.parseBody import parseBody
from utils.giveError import throwError
from dotenv import load_dotenv
from pathlib import Path
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = Path(os.path.join(PROJECT_DIR, "config.env"))
load_dotenv(dotenv_path=dotenv_path)


# Create your views here.
class RegisterPage(View):
    def get(self, req):
        return render(req, "users/register.html")

    def post(self, req):
        # Get user data
        res = parseBody(req.body)
        username = res["username"]
        password = res["password"]
        confirmPassword = res["confirmPassword"]

        try:
            rememberMe = res["rememberMe"]
        except:
            rememberMe = "off"

        # Check password
        if not (password == confirmPassword):
            return throwError()

        # Check username
        user_count = User.objects.filter(username=username).count()
        if user_count > 0:
            return throwError()

        # Save user
        salt = os.getenv("salt")
        tmp = password + salt
        hashedPassword = hashlib.sha256(tmp.encode("utf-8")).hexdigest()
        newUser = User(username=username, password=hashedPassword)
        newUser.save()

        # Store cookie

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
