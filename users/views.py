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
import jwt
from utils.getNMonthsFromNow import getNMonthsFromNow
from django.conf import settings
from django.http import HttpResponseRedirect
from datetime import timedelta

# Prepare .env file
dotenv_path = Path(os.path.join(settings.PROJECT_DIR, "config.env"))
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
        if password == "":
            return throwError()

        if not (password == confirmPassword):
            return throwError()

        # Check username
        user_count = User.objects.filter(username=username).count()
        if user_count > 0:
            return throwError()

        # Hash Password
        salt = os.getenv("salt")
        tmp = password + salt
        hashedPassword = hashlib.sha256(tmp.encode("utf-8")).hexdigest()

        # encode jwt token
        N = int(os.getenv("CookieLifeInMonths"))
        expireDate = getNMonthsFromNow(N)
        payload = {
            "username": username,
            "hashedPassword": hashedPassword,
            "exp": expireDate,
        }
        SECRET_KEY = os.getenv("SECRET_KEY")
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        # save user
        newUser = User(username=username, password=hashedPassword, jwtToken=token)
        newUser.save()

        # save cookie
        response = HttpResponseRedirect("/")  # Like HttpResponse, but redirects you

        if rememberMe == "on":
            delta = timedelta(days=N * 30)
            response.set_cookie(
                "jwt_token", token, secure=False, httponly=False, max_age=delta
            )
        else:
            response.set_cookie("jwt_token", token, secure=False, httponly=False)

        return response  # DONT FORGET


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
