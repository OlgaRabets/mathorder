from django.urls import path
from .views import base, create_task, api_categories

urlpatterns = [
    path('api/categories/', api_categories),
    path('', base),
    path('create-task', create_task, name='create_task'),
]
