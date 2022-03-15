from rest_framework.serializers import ModelSerializer
from .models import Task, Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'description', 'done']
