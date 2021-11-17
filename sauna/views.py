from datetime import date
from decimal import Decimal

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.db.models import Sum, Count
from django.contrib import auth
from django.views.generic import ListView, CreateView

from .models import Person, Visit, Price
from .forms import VisitForm, LoginUserForm


def base(request: HttpRequest):
    request.session['fontSize'] = 40
        #request.session.get('fontSize', 20)
    return render(request, "sauna/base.html", {'fontSize': request.session['fontSize']})


class PriceListView(ListView):
    #template_name = 'sauna/price_list.html'
    model = Price
    queryset = Price.objects.all().order_by('number', 'privilege')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Прайс'
        return context


class PersonListView(ListView):
    #template_name = 'sauna/person_list.html'
    model = Person

    def get_context_data(self, **kwargs):
        person_rests_sum = Decimal('0.00')  # сумма персональных остатков
        for person in Person.objects.all():
            person_rest = person.get_rest_of_last_visit()  # персональный остаток
            person_rests_sum += person_rest
        context = super().get_context_data(**kwargs)
        context['person_rests_sum'] = person_rests_sum
        context['title'] = 'Посетители'
        return context


def show_persons(request: HttpRequest):
    """
    Формирование списка остатков денег по каждому человеку
    :param request:
    :return:
    """
    persons = Person.objects.all().order_by('name')
    id_and_name_and_rest_of_persons = {}
    person_rests_sum = Decimal('0.00')  # сумма персональных остатков
    for person in persons:
        person_rest = person.get_rest_of_last_visit()  # персональный остаток
        id_and_name_and_rest_of_persons[person.pk] = [person.name, person_rest]
        person_rests_sum += person_rest
    context = {'id_and_name_and_rest_of_persons': id_and_name_and_rest_of_persons,
               'person_rests_sum': person_rests_sum}
    return render(request, 'sauna/show_persons.html', context)


def show_persons_001(request: HttpRequest):
    visits_all = Visit.objects.order_by('person', '-date')
    visits = []
    pk = -1
    for visit in visits_all:
        if visit.person != pk:
            visits.append(visit)
            pk = visit.person
    return render(request, 'sauna/show_persons.html', {'visits': visits})


class PersonCreateView(CreateView):
    template_name = 'sauna/person_create.html'
    model = Person
    fields = ['name', 'privilege']
    success_url = 'show-persons'


def show_visits(request: HttpRequest):
    """
    Формирование списка
    :param request:
    :return:
    """
    visits_group_by_date = Visit.objects.values('date') \
        .annotate(Count('date'), Sum('fill'), cost=Sum('cost')) \
        .order_by('-date')
    context = {'visits_group_by_date': visits_group_by_date}
    return render(request, 'sauna/show_visits.html', context)

    date_and_persons_number_and_fills_sum = []
    visits = Visit.objects.order_by('-date')
    current_date = visits.first().date
    persons_number = 0
    fills_sum = Decimal('0.00')
    costs_sum = Decimal('0.00')
    for visit in visits:
        if visit.date == current_date:
            persons_number += 1
            fills_sum += visit.fill
            costs_sum += visit.cost
        else:
            date_and_persons_number_and_fills_sum.append([current_date, persons_number, fills_sum, costs_sum])
            current_date = visit.date
            persons_number = 1
            fills_sum = visit.fill
            costs_sum = visit.cost
    date_and_persons_number_and_fills_sum.append([current_date, persons_number, fills_sum, costs_sum])
    context = {'date_and_persons_number_and_fills_sum': date_and_persons_number_and_fills_sum}
    return render(request, 'sauna/show_visits.html', context)


def show_visits_001(request: HttpRequest):
    """
    Формирование списка
    :param request:
    :return:
    """
    if not Visit.objects.exists():
        context = {'date_and_persons_number_and_fills_sum': []}
        return render(request, 'sauna/show_visits.html', context)

    date_and_persons_number_and_fills_sum = []
    visits = Visit.objects.order_by('-date')
    current_date = visits.first().date
    persons_number = 0
    fills_sum = Decimal('0.00')
    costs_sum = Decimal('0.00')
    for visit in visits:
        if visit.date == current_date:
            persons_number += 1
            fills_sum += visit.fill
            costs_sum += visit.cost
        else:
            date_and_persons_number_and_fills_sum.append([current_date, persons_number, fills_sum, costs_sum])
            current_date = visit.date
            persons_number = 1
            fills_sum = visit.fill
            costs_sum = visit.cost
    date_and_persons_number_and_fills_sum.append([current_date, persons_number, fills_sum, costs_sum])
    context = {'date_and_persons_number_and_fills_sum': date_and_persons_number_and_fills_sum}
    return render(request, 'sauna/show_visits.html', context)


def create_person(request: HttpRequest, name: str, privilege):
    if privilege not in {'True', 'False'}:
        return HttpResponse('Oh, No!')
    person = Person(name=name)
    if privilege == 'True':
        person.privilege = True
    else:
        person.privilege = False
    person.save()
    return HttpResponse('Yes!')


class VisitByPersonListView(ListView):
    template_name = 'sauna/show_person_visits.html'

    def get_queryset(self):
        return Visit.objects.filter(person=self.kwargs['person']).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_person'] = Person.objects.get(pk=self.kwargs['person'])
        context['visits'] = Visit.objects.filter(person=self.kwargs['person']).order_by('-date')
        return context

def show_person_visits(request: HttpRequest, person):
    current_person = Person.objects.get(pk=person)
    visits = Visit.objects.filter(person=person).order_by('-date')
    context = {'current_person': current_person,
               'visits': visits}
    return render(request, 'sauna/show_person_visits.html', context)


def create_visit_old(request: HttpRequest, person: int, date_of_visit: date, fill):
    visit = Visit()
    d = date_of_visit[0:2]
    m = date_of_visit[3:5]
    y = date_of_visit[6:]
    date_of_visit = date(year=int(y), month=int(m), day=int(d))
    visit.date = date_of_visit
    person = Person.objects.get(pk=person)
    visit.person = person
    fill = Decimal(fill)
    visit.fill = fill
    cost = visit.get_cost_of_current_visit()
    visit.cost = cost
    rest = person.get_rest_of_last_visit() + fill - cost
    visit.rest = rest
    visit.save()
    return HttpResponse(cost)


class VisitCreateView(CreateView):
    template_name = 'sauna/create_visit.html'
    form_class = VisitForm
    #success_url = 'show-persons/{pk}'

    def get(self, request, person):
        p = Person.objects.get(pk=person)
        form = VisitForm(initial={'date': date.today(),
                                  'person': p})
        return render(request, 'sauna/create_visit.html', {'form': form, 'person': person})

    def post(self, request, person):
        form = VisitForm(request.POST)
        if form.is_valid():
            form.save()
            return show_person_visits(request, person)
        return render(request, 'sauna/create_visit.html', {'form': form, 'person': person})


def create_visit(request: HttpRequest, person: int):
    if request.method == 'GET':
        p = Person.objects.get(pk=person)
        form = VisitForm(initial={'date': date.today(),
                                  'person': p})
    elif request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            form.save()
            return show_person_visits(request, person)
    return render(request, 'sauna/create_visit.html', {'form': form, 'person': person})


def logout_user(request: HttpRequest):
    if request.user.is_authenticated:
        auth.logout(request)
    return render(request, "sauna/base.html", {})


def login_user(request: HttpRequest):
    err = ''
    if request.method == 'GET':
        form = LoginUserForm()
    elif request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return render(request, "sauna/base.html", {})
            elif request.POST['user_has_login_and_password'] == 'no':
                if auth.models.User.objects.filter(username=request.POST['username']).exists():
                    err = "Пользователь с таким именем уже существует. Выберите другое имя."
                    return render(request, "sauna/login_user.html", {'form': form, 'err': err})
                user == auth.models.User.objects.create_user(request.POST['username'],
                                                             password=request.POST['password'])
                auth.login(request, user)
                return render(request, "sauna/base.html", {})
            else:
                err = "Ошибка при вводе логина или пароля!"
    return render(request, "sauna/login_user.html", {'form': form, 'err': err})
