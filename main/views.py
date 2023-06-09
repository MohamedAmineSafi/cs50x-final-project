from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import View

from users.models import User
from .models import Friend
from utils.isLoggedIn import isLoggedIn
from utils.parseBody import parseBody
from utils.giveError import throwError

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


class Delete(View):
    def get(self, req, *args, **kwargs):
        if not isLoggedIn(req, User, SECRET_KEY):
            return throwError()

        idToDelete = kwargs.get("friend_id")

        # Get logged in user
        token = req.COOKIES["jwt_token"]
        user = User.objects.get(jwtToken=token)

        # Delete
        try:
            Friend.objects.get(addedBy=user, id=idToDelete).delete()
        except:
            return throwError()

        return redirect("/")
