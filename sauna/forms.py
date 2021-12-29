from django.forms import ModelForm, Form, CharField, PasswordInput, TextInput, DateInput
from .models import Person, Visit


class VisitForm(ModelForm):
    class Meta:
        model = Visit
        exclude = ['cost', 'rest']
#        widgets = {
#            'cost': TextInput(attrs={'readonly': True})
#        }


class LoginUserForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)
