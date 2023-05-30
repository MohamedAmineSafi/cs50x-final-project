from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import View, TemplateView
from users.models import User
from utils.giveError import throwError
from utils.isLoggedIn import isLoggedIn
from utils.parseBody import parseBody
from .models import Friend

SECRET_KEY = settings.SECRET_KEY


# Create your views here.
class HomePage(View):
    def get(self, req):
        if not isLoggedIn(req, User, SECRET_KEY):
            return redirect("/auth/login/")

        # Get friends from DB
        token = req.COOKIES["jwt_token"]
        user = User.objects.get(jwtToken=token)
        friends = Friend.objects.values().filter(addedBy=user)

        return render(
            req,
            "main/index.html",
            {"isLoggedIn": isLoggedIn(req, User, SECRET_KEY), "friends": friends},
        )


class Add(View):
    def get(self, req):
        return render(
            req,
            "main/addFriend.html",
            {"isLoggedIn": isLoggedIn(req, User, SECRET_KEY)},
        )

    def post(self, req):
        if not isLoggedIn(req, User, SECRET_KEY):
            return throwError()

        # Get form data
        res = parseBody(req.body)
        name = res["name"]
        birthday = res["birthday"]
        hobbies = res["hobbies"]
        personality = res["personality"]

        if name == "":
            return throwError()

        # Get logged in user
        token = req.COOKIES["jwt_token"]
        user = User.objects.get(jwtToken=token)

        # save to DB
        newFriend = Friend(
            addedBy=user,
            name=name,
            birthday=birthday,
            hobbies=hobbies,
            personality=personality,
        )
        newFriend.save()
        return redirect("/")
