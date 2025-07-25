from django import forms
from django.utils.html import strip_tags
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'status', 'deadline', 'priority')


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'status', 'priority')
