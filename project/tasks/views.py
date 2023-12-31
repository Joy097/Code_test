from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from .models import Task
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from rest_framework.renderers import TemplateHTMLRenderer
from .serializers import ItemSerializer
from django.db.models import Case, When, Value, CharField

class Login(LoginView):
    template_name = 'tasks/login.html'
    fields = ['title','description','complete','priority','due']
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    
class Register(FormView):
    template_name = 'tasks/register.html'
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
            
        selected_priority = self.request.GET.get('priority')
        if selected_priority:
            context['tasks'] = context['tasks'].filter(priority=selected_priority)
            
        selected_cmp = self.request.GET.get('cmp')
        if selected_cmp:
            context['tasks'] = context['tasks'].filter(complete=selected_cmp)
            
        selected_DD = self.request.GET.get('due-date')
        if selected_DD:
            context['tasks'] = context['tasks'].filter(due=selected_DD)
            
        selected_CD = self.request.GET.get('cr-date')
        if selected_CD:
            context['tasks'] = context['tasks'].filter(created=selected_CD)

        context['tasks'] = context['tasks'].order_by(
            Case(
                When(priority='Low', then=Value(3)),
                When(priority='Medium', then=Value(2)),
                When(priority='High', then=Value(1)),
                default=Value(4),
                output_field=CharField(),
            )
        )
        context['search_input'] = search_input

        return context
    
class TaskCreate(CreateView):
    model = Task
    fields = ['title','description','complete','photos','priority','due']
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
    
class TaskUpdate(UpdateView):
    model = Task
    fields = ['title','description','complete','photos','priority','due']
    success_url = reverse_lazy('tasks')
    
    
class TaskDelete(DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    def get_priority(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)
  
# Example of api_view
  
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def task(request, pk):
    instance = Task.objects.get(pk=pk)
    serialized = ItemSerializer(instance)
    return Response({'data':serialized.data}, template_name='task_detail.html')