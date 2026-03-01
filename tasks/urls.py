from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task-list'),
    path('<int:pk>/', views.task_detail, name='task-detail'),
    path('create/', views.task_create, name='task-create'),
    path('my-tasks/', views.my_tasks, name='my-tasks'),
    path('<int:pk>/status/', views.task_update_status, name='task-status'),
]