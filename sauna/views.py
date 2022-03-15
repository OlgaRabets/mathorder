from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Sum, Count
from django.contrib import auth
from django.views.generic import ListView, CreateView

from .models import Person, Visit, Price, Payment
from .forms import VisitForm, LoginUserForm


def base(request: HttpRequest):
    request.session['fontSize'] = 40
    # request.session.get('fontSize', 20)
    return render(request, "sauna/base.html", {'fontSize': request.session['fontSize']})


class PriceListView(ListView):
    # template_name = 'sauna/price_list.html'
    model = Price
    queryset = Price.objects.all().order_by('number', 'privilege')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Прайс'
        return context


class PersonListView(ListView):
    # template_name = 'sauna/person_list.html'
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
    person_rests = Decimal('0.00')  # сумма персональных остатков
    for person in Person.objects.all():
        person_rests += person.get_rest_of_last_visit()

    current_date = Visit.objects.order_by('-date').first().date  # дата последнего посещения сауны

    used_payments = Decimal('0.00')  # использованные оплаты посещений сауны
    for payment in Payment.objects.all():
        if payment.date <= current_date:
            used_payments += payment.cost

    unused_payments = Decimal('0.00')  # неиспользованные оплаты посещений сауны
    for payment in Payment.objects.all():
        if payment.date > current_date:
            unused_payments += payment.cost

    person_costs = Decimal('0.00')  # сумма, заплаченная посетителями за посещения сауны
    for visit in Visit.objects.all():
        person_costs += visit.cost

    unperson_rests = person_costs - used_payments  # общие остатки
    cash = person_rests + unperson_rests - unused_payments  # наличные у меня

    visits_group_by_date = Visit.objects.values('date') \
        .annotate(Count('date'), Sum('fill'), cost=Sum('cost')) \
        .order_by('-date')
    context = {'visits_group_by_date': visits_group_by_date,
               'person_rests': person_rests, 'person_costs': person_costs,
               'used_payments': used_payments, 'unused_payments': unused_payments,
               'unperson_rests': unperson_rests, 'cash': cash}
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


class VisitByPersonListView(LoginRequiredMixin, ListView):
    template_name = 'sauna/show_person_visits.html'

    def get_queryset(self):
        return Visit.objects.filter(person=self.kwargs['person']).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_person'] = Person.objects.get(pk=self.kwargs['person'])
        visits = self.get_queryset()
        paginator = Paginator(visits, 5)
        if 'page' in self.request.GET:
            page_num = self.request.GET['page']
        else:
            page_num = 1
        page = paginator.get_page(page_num)
        context['page'] = page
        context['visits'] = page.object_list
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


def date_last_friday():
    # номер сегодняшнего дня недели
    day_of_week_today = date.today().weekday()
    # сколько дней дазад была пятница
    if day_of_week_today < 4:
        days_ago = day_of_week_today + 3
    else:
        days_ago = day_of_week_today - 4
    # дата последней пятницы
    return date.today() - timedelta(days=days_ago)


class VisitCreateView(CreateView):
    template_name = 'sauna/create_visit.html'
    form_class = VisitForm

    # success_url = 'show-persons/{pk}'

    def get(self, request, person):
        p = Person.objects.get(pk=person)
        form = VisitForm(initial={'date': date_last_friday(),
                                  'fill': Decimal('0.00'),
                                  'person': p})
        return render(request, 'sauna/create_visit.html', {'form': form, 'person': person})

    def post(self, request, person):
        form = VisitForm(request.POST)
        if form.is_valid():
            # form.instance.person = Person.objects.get(pk=person)
            form.instance.cost = form.instance.get_cost_of_current_visit()
            form.instance.rest = form.instance.person.get_rest_of_last_visit() + form.instance.fill - form.instance.cost
            form.save()
            # return show_person_visits(request, person)
            return redirect('show_person_visits', person=person)
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


# def logout_user(request: HttpRequest):
#    if request.user.is_authenticated:
#        auth.logout(request)
#    return render(request, "sauna/base.html", {})

# @ login_required()
# def login_user(request: HttpRequest):
#    err = ''
#    if request.method == 'GET':
#        form = LoginUserForm()
#    elif request.method == 'POST':
#        form = LoginUserForm(request.POST)
#        if form.is_valid():
#            user = auth.authenticate(request, **form.cleaned_data)
#            if user is not None:
#                auth.login(request, user)
#                return render(request, "sauna/base.html", {})
#            elif request.POST['user_has_login_and_password'] == 'no':
#                if auth.models.User.objects.filter(username=request.POST['username']).exists():
#                    err = "Пользователь с таким именем уже существует. Выберите другое имя."
#                    return render(request, "sauna/login_user.html", {'form': form, 'err': err})
#                user == auth.models.User.objects.create_user(request.POST['username'],
#                                                             password=request.POST['password'])
#                auth.login(request, user)
#                return render(request, "sauna/base.html", {})
#            else:
#                from django.utils.translation import gettext
#                err = gettext("Ошибка при вводе логина или пароля!")
#    return render(request, "sauna/login_user.html", {'form': form, 'err': err})

class SaunaLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return '/show-person-visits/'+str(self.request.user.person.id)+'/'

