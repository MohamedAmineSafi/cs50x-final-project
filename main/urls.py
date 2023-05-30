from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.HomePage.as_view(), name="index"),
    path("add/", views.Add.as_view(), name="add"),
    path("delete/<int:friend_id>", views.Delete.as_view(), name="add"),
]
