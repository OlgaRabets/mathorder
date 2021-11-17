from django.http import HttpRequest
from django.shortcuts import render
from .models import Task
from .forms import TaskForm


# Create your views here.
def base(request: HttpRequest):
    tasks = Task.objects.all()
    return render(request, 'todo/base.html', {'tasks': tasks})


def create_task(request: HttpRequest):
    if request.method == 'GET':
        form = TaskForm()
    elif request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'todo/create_task.html', {'form': form})
