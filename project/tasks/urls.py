from django.urls import path
from .views import Tasklist, TaskDetails

urlpatterns = [
    path('', Tasklist.as_view(),name='tasks'),
    path('task/<int:pk>/', TaskDetails.as_view(),name='tasks')
    
    ]
