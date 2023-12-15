from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class Login(LoginView):
    template_name = 'tasks/login.html'
    fields = ['title','description','complete','priority','due']
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    
class Register(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(Register, self).get(*args, **kwargs)

    
class Tasklist(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'
    
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context

    
class TaskDetails(DetailView):
    model = Task
    context_object_name = 'task'
    
class TaskCreate(CreateView):
    model = Task
    fields = ['title','description','complete','priority','due']
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
    
class TaskUpdate(UpdateView):
    model = Task
    fields = ['title','description','complete','priority','due']
    success_url = reverse_lazy('tasks')
    
    
class TaskDelete(DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    def get_priority(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)