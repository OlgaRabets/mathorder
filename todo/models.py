from django.db import models


# Create your models here.
class Task(models.Model):
    description = models.CharField(max_length=50)
    done = models.BooleanField(default=False)
