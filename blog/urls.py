from django.urls import path
from .views import base, create_post

urlpatterns = [
    path('', base),
    path('create-task', create_post, name='create_task'),
]
