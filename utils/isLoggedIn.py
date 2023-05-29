import jwt


def isLoggedIn(req, UserModel, SECRET_KEY):
    User = UserModel

    # Get token from cookie
    try:
        tokenFromCookie = req.COOKIES["jwt_token"]
    except:
        return False

    if not (bool(tokenFromCookie)):
        return False

    # Get token from DB
    try:
        user = User.objects.values().get(jwtToken=tokenFromCookie)
        user = dict(user)
    except:
        return False

    tokenFromDB = user["jwtToken"]

    if tokenFromDB == "":
        return False

    try:
        jwt.decode(tokenFromDB, SECRET_KEY, algorithms=["HS256"])
    except:
        return False

    return True
