from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.list import DetailView
from .models import Task

class Tasklist(ListView):
    model = Task
    context_object_name = 'tasks'
    
class TaskDetails(DetailView):
    model = Task
     