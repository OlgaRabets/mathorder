from datetime import date
from decimal import Decimal
from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name='Имя')
    privilege = models.BooleanField(verbose_name='Льготный тариф')

    class Meta:
        verbose_name_plural = 'Посетители'
        verbose_name = 'Посетителя'
        ordering = ['name']

    def get_rest_of_last_visit(self):
        """
        Получение для человека остатка из его последнего посещения.
        Если у человека нет посещений, то возвращается 0.
        :param self:
        :return:
        """
        rest = Decimal('0.00')
        try:
            rest = Visit.objects.filter(person=self.pk).order_by('-date')[0].rest
        finally:
            return rest


class Visit(models.Model):
    date = models.DateField(verbose_name='Дата')
    person = models.ForeignKey('Person', null=True, on_delete=models.CASCADE, verbose_name='Посетитель')
    fill = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Пополнение')
    cost = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Стоимость')
    rest = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Остаток')

    class Meta:
        verbose_name_plural = 'Посещения'
        verbose_name = 'Посещение'
        ordering = ['-date', 'person']

    def person_name(self):
        return self.person.name

    def get_number_of_visits_in_current_month(self):
        current_month = self.date.month
        number_of_visits = 0
        visits = Visit.objects.filter(person=self.person)
        for visit in visits:
            if visit.date.month == current_month:
                number_of_visits += 1
        return number_of_visits + 1

    def get_cost_of_current_visit(self):
        privilege = self.person.privilege
        number_of_visits_in_current_month = self.get_number_of_visits_in_current_month()
        price = Price.objects.filter(privilege=privilege).get(number=number_of_visits_in_current_month)
        return price.cost


class Price(models.Model):
    privilege = models.BooleanField(verbose_name='Льготный тариф')
    number = models.IntegerField(verbose_name='Номер посещения в месяце')
    cost = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Стоимость')

    class Meta:
        verbose_name_plural = 'Тарифы'
        verbose_name = 'Тариф'
        ordering = ['privilege', 'number']
