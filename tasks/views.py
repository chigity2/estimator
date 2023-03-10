from django.shortcuts import render
from .serializers import TasksSerializer
from rest_framework import viewsets
from .models import Tasks


class TasksView(viewsets.ModelViewSet):
    serializer_class = TasksSerializer
    queryset = Tasks.objects.all()




