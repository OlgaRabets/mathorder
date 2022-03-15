from datetime import date
from decimal import Decimal
from logging import getLogger

from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User
from django.db import models
# from django.db.models.signals import pre_save
# from django.dispatch import receiver
from django.dispatch import receiver


class Person(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name='Имя')
    privilege = models.BooleanField(verbose_name='Льготный тариф')
    user = models.OneToOneField(User, null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Посетители'
        verbose_name = 'Посетителя'
        ordering = ['name']

    def __str__(self):
        return self.name

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


#    @receiver(pre_save)
#    def pre_save_visit(sender, **kwargs):
#        visit = kwargs['instance']
#        visit.cost = visit.get_cost_of_current_visit()
#        visit.rest = visit.person.get_rest_of_last_visit() + visit.fill - visit.cost


class Price(models.Model):
    privilege = models.BooleanField(verbose_name='Льгота')
    number = models.IntegerField(verbose_name='Номер посещения в месяце')
    cost = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Стоимость')

    class Meta:
        verbose_name_plural = 'Цены'
        verbose_name = 'Цена'
        ordering = ['privilege', 'number']


class Payment(models.Model):
    date = models.DateField(verbose_name='Дата')
    cost = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Стоимость')

    class Meta:
        verbose_name_plural = 'Платежи'
        verbose_name = 'Платеж'
        ordering = ['-date']


@receiver(user_logged_in)
def write_logging(sender, **kwargs):
    logger = getLogger(__name__)
    logger.info('пользователь с логином %s успешно выполнил вход на сайт', kwargs['user'].username)
