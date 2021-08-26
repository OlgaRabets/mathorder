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
