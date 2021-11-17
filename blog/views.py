from django.http import HttpRequest
from django.shortcuts import render


# Create your views here.
def base(request: HttpRequest):
    return render(request, 'blog/base.html', {})


def create_post():
    pass
