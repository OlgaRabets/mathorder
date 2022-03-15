from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)


class Priority(models.Model):
    name = models.CharField(max_length=50)


class Task(models.Model):
    description = models.CharField(max_length=500)
    done = models.BooleanField(default=False)
    deadline = models.DateField(null=True)
    category = models.ForeignKey('Category', null=True, on_delete=models.PROTECT)
    priority = models.ForeignKey('Priority', null=True, on_delete=models.PROTECT)
