from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from .forms import TaskForm, TaskUpdateForm
from .models import Task

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'main/task_list.html', {'tasks': tasks})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'main/task_detail.html', {'task': task})


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('main:task_list')
    else:
        form = TaskForm()
    return render(request, 'main/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('main:task_list')
    else:
        form = TaskUpdateForm(instance=task)
    return render(request, 'main/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('main:task_list')
    return render(request, 'main/task_delete.html', {'task': task})


@login_required
def mark_task_done(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        task.status = 'done'
        task.save()
    return redirect('main:task_list')
