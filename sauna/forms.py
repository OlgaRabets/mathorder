from django.forms import ModelForm, Form, CharField, PasswordInput
from .models import Person, Visit


class VisitForm(ModelForm):
    class Meta:
        model = Visit
        exclude = []


class LoginUserForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)
