from django.urls import path
from . import views

app_name = 'habit_tracker'

urlpatterns = [
    path('daily_habits/', views.daily_habits, name='daily_habits'),
    path('habit/<int:pk>', views.habit_detail, name='habit_detail'),
    path('habit/new/', views.habit_new, name='habit_new'),
    path('habit/<int:pk>/edit/', views.habit_edit, name='habit_edit'),
    path('habit/<pk>/delete/', views.habit_delete, name='habit_delete'),
    path('daily_record/<int:pk>', views.daily_record, name='daily_record'),
    path('daily_record/<int:pk>/edit/', views.edit_daily_record, name='edit_daily_record'),
]

