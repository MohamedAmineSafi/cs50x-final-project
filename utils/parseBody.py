from django.http import QueryDict


def parseBody(reqBody):
    res = QueryDict(reqBody.decode("utf-8"))
    return res
