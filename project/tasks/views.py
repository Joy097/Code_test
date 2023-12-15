from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Task
from django.urls import reverse_lazy


class Tasklist(ListView):
    model = Task
    context_object_name = 'tasks'
    
class TaskDetails(DetailView):
    model = Task
    context_object_name = 'task'
    
class TaskCreate(CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')
    
class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')