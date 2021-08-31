from datetime import date
from decimal import Decimal

from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    privilege = models.BooleanField()

    def get_rest_of_last_visit(self):
        """
        Получение для человека остатка из его последнего посещения.
        Если у человека нет посещений, то возвращается 0.
        :param self:
        :return:
        """
        rest = Decimal('0.00')
        try:
            rest = Visit.objects.filter(person_id=self.pk).order_by('-date')[0].rest
        finally:
            return rest


class Visit(models.Model):
    date = models.DateField()
    person_id = models.ForeignKey('Person', null=True, on_delete=models.CASCADE)
    fill = models.DecimalField(max_digits=5, decimal_places=2)
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    rest = models.DecimalField(max_digits=5, decimal_places=2)

    def get_number_of_visits_in_current_month(self):
        current_month = self.date.month
        number_of_visits = 0
        visits = Visit.objects.filter(person_id=self.person_id)
        for visit in visits:
            if visit.date.month == current_month:
                number_of_visits += 1
        return number_of_visits + 1

    def get_cost_of_current_visit(self):
        privilege = self.person_id.privilege
        number_of_visits_in_current_month = self.get_number_of_visits_in_current_month()
        price = Price.objects.filter(privilege=privilege).get(number=number_of_visits_in_current_month)
        return price.cost



class Price(models.Model):
    privilege = models.BooleanField()
    number = models.IntegerField()
    cost = models.DecimalField(max_digits=5, decimal_places=2)
