from django.urls import path

from .views import show_persons, create_person, show_person_visits

urlpatterns = [
    path('', show_persons),
    path('create-person/<str:name>/<slug:privilege>', create_person),
    path('show-person-visits/<int:person_id>/', show_person_visits)
]