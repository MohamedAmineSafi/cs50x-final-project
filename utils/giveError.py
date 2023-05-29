from django.shortcuts import redirect

link = "https://dumacollective.com/404"


def throwError():
    return redirect(link)
