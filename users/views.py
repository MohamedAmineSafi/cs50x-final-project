import os
from datetime import timedelta
import hashlib
import jwt

from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect
from django.conf import settings

from .models import User
from utils.parseBody import parseBody
from utils.giveError import throwError
from utils.getNMonthsFromNow import getNMonthsFromNow
from utils.isLoggedIn import isLoggedIn

SECRET_KEY = settings.SECRET_KEY


# Create your views here.
class RegisterPage(View):
    def get(self, req):
        return render(
            req,
            "users/register.html",
            {"isLoggedIn": isLoggedIn(req, User, SECRET_KEY)},
        )

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


class LoginPage(View):
    def get(self, req):
        return render(
            req, "users/login.html", {"isLoggedIn": isLoggedIn(req, User, SECRET_KEY)}
        )

    def post(self, req):
        # Get user data
        res = parseBody(req.body)
        username = res["username"]
        password = res["password"]

        try:
            rememberMe = res["rememberMe"]
        except:
            rememberMe = "off"

        # Hash the password
        salt = os.getenv("salt")
        tmp = password + salt
        hashedPassword = hashlib.sha256(tmp.encode("utf-8")).hexdigest()

        # Get User
        try:
            userFromDB = User.objects.values().get(
                username=username, password=hashedPassword
            )
            userFromDB = dict(userFromDB)
        except User.DoesNotExist:
            userFromDB = None

        # Check Info
        if userFromDB == None:
            return throwError()

        # Correct Name and Pass, Now update jwt and cookie

        # Encode JWT
        N = int(os.getenv("CookieLifeInMonths"))
        expireDate = getNMonthsFromNow(N)
        payload = {
            "username": username,
            "hashedPassword": hashedPassword,
            "exp": expireDate,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        # write new jwt to DB
        user = User.objects.get(username=username, password=hashedPassword)
        user.jwtToken = token
        user.save()

        # save cookie
        response = HttpResponseRedirect("/")

        if rememberMe == "on":
            delta = timedelta(days=N * 30)
            response.set_cookie(
                "jwt_token", token, secure=False, httponly=False, max_age=delta
            )
        else:
            response.set_cookie("jwt_token", token, secure=False, httponly=False)

        return response


class ChangePasswordPage(View):
    def get(self, req):
        return render(
            req,
            "users/changePassword.html",
            {"isLoggedIn": isLoggedIn(req, User, SECRET_KEY)},
        )

    def post(self, req):
        if not isLoggedIn(req, User, SECRET_KEY):
            return throwError()

        # Get data from form
        res = parseBody(req.body)
        currentPass = res["currentPassword"]
        newPassword = res["newPassword"]
        cNewPassword = res["confirmPassword"]

        # Make sure passwords are the same
        if not (newPassword == cNewPassword):
            return throwError()

        # Hash password
        salt = os.getenv("salt")
        tmp = currentPass + salt
        hashedPassword = hashlib.sha256(tmp.encode("utf-8")).hexdigest()

        # Get token from cookie
        token = req.COOKIES["jwt_token"]
        if not (bool(token)):
            return throwError()

        # Get user
        try:
            user = User.objects.get(password=hashedPassword, jwtToken=token)
        except User.DoesNotExist:
            return throwError()

        # hash new pass
        salt = os.getenv("salt")
        tmp = newPassword + salt
        hashNewPass = hashlib.sha256(tmp.encode("utf-8")).hexdigest()

        # save user
        user.password = hashNewPass
        user.jwtToken = ""
        user.save()
        return redirect("/")


class Logout(View):
    def get(self, req):
        response = HttpResponseRedirect("/")
        response.set_cookie("jwt_token", "", secure=False, httponly=False)
        return response
