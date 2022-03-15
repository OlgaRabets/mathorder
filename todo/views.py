from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task, Category
from .forms import TaskForm
from .serializers import CategorySerializer


# Create your views here.
@api_view(['GET'])
def api_categories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


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
