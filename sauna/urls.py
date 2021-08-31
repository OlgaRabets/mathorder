from django.urls import path

from .views import show_persons, create_person, show_person_visits, create_visit

urlpatterns = [
    path('', show_persons),
    path('create-person/<str:name>/<slug:privilege>', create_person),
    path('show-person-visits/<int:person_id>/', show_person_visits),
    path('create-visit/<int:person_id>/<date_of_visit>/<fill>', create_visit),
]