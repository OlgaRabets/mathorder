from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse

from .views import PersonCreateView, VisitCreateView, SaunaLoginView
from .views import base, PriceListView, PersonListView, show_visits, create_person, VisitByPersonListView
#from .views import logout_user
#from .views import login_user

urlpatterns = [
    path('', base, name='base'),
    path('show-price', PriceListView.as_view(), name='show_price'),
    path('show-persons', PersonListView.as_view(), name='show_persons'),
    path('show-visits', show_visits, name='show_visits'),
    path('create-person1', PersonCreateView.as_view()),
    path('create-person/<str:name>/<slug:privilege>', create_person),
    path('show-person-visits/<int:person>/', VisitByPersonListView.as_view(), name='show_person_visits'),
    path('create-visit/<int:person>', VisitCreateView.as_view(), name='create_visit'),
    #path('logout-user', logout_user, name='logout_user'),
    #path('login-user', login_user, name='login_user'),
#    path('accounts/login/', LoginView.as_view(template_name='registration/login.html',
#                                              redirect_field_name='next',
#                                              extra_context={'next': '/show-person-visits/1/'}), name='login'),
    path('accounts/login/', SaunaLoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
]
