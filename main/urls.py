from django.urls import path
from . import views
from .api import create_task_api, get_tasks_for_date

app_name = 'main'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
    path('create/', views.task_create, name='task_create'),
    path('task/<int:pk>/done/', views.mark_task_done, name='task_mark_done'),
    path('<int:pk>/update/', views.task_update, name='task_update'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('calendar/', views.calendar, name='calendar'),
    path('api/tasks/', get_tasks_for_date, name='get_tasks_for_date'),
    path('api/tasks/create/', create_task_api, name='create_task_api'),
]

