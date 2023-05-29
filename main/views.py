from django.shortcuts import render
from django.conf import settings
from django.views.generic import TemplateView

from users.models import User
from utils.isLoggedIn import isLoggedIn

SECRET_KEY = settings.SECRET_KEY


# Create your views here.
class HomePage(TemplateView):
    http_method_names = ["get"]
    template_name = "main/index.html"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["isLoggedIn"] = isLoggedIn(self.request, User, SECRET_KEY)
        return context


class Add(TemplateView):
    http_method_names = ["get"]
    template_name = "main/addFriend.html"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["isLoggedIn"] = isLoggedIn(self.request, User, SECRET_KEY)
        return context
