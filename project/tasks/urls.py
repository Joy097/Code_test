from django.urls import path
from .views import Tasklist, TaskDetails, TaskCreate, TaskUpdate

urlpatterns = [
    path('', Tasklist.as_view(),name='tasks'),
    path('task/<int:pk>/', TaskDetails.as_view(),name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update')
    ]
