from django.urls import path

from .views import PersonCreateView, VisitCreateView
from .views import base, PriceListView, PersonListView, show_visits, create_person, VisitByPersonListView
from .views import logout_user, login_user

urlpatterns = [
    path('', base, name='base'),
    path('show-price', PriceListView.as_view(), name='show_price'),
    path('show-persons', PersonListView.as_view(), name='show_persons'),
    path('show-visits', show_visits, name='show_visits'),
    path('create-person1', PersonCreateView.as_view()),
    path('create-person/<str:name>/<slug:privilege>', create_person),
    path('show-person-visits/<int:person>/', VisitByPersonListView.as_view()),
    path('create-visit/<int:person>', VisitCreateView.as_view(), name='create_visit'),
    path('logout-user', logout_user, name='logout_user'),
    path('login-user', login_user, name='login_user'),
]