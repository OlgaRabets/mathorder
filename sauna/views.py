from decimal import Decimal

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Person, Visit


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
    return render(request, 'show_persons.html', context)

def show_persons_old(request: HttpRequest):
    visits_all = Visit.objects.order_by('person_id', '-date')
    visits = []
    pk = -1
    for visit in visits_all:
        if visit.person_id != pk:
            visits.append(visit)
            pk = visit.person_id
    return render(request, 'show_persons.html', {'visits': visits})

def create_person(request: HttpRequest, name: str, privilege):
    if privilege not in {'True', 'False'}:
        return HttpResponse('Oh, No!')
    person = Person(name = name)
    if privilege == 'True':
        person.privilege = True
    else:
        person.privilege = False
    person.save()
    return HttpResponse('Yes!')

def show_person_visits(request: HttpRequest, person_id):
    current_person = Person.objects.get(pk=person_id)
    visits = Visit.objects.filter(person_id=person_id).order_by('-date')
    context = {'current_person': current_person,
               'visits': visits}
    return render(request, 'show_person_visits.html', context)