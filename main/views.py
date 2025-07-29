from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import TaskForm, TaskUpdateForm
from .models import Task
from django.contrib import messages


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user, is_deleted=False).order_by('deadline')
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
            messages.success(request, 'Задача успешно добавлена!')
            return redirect('main:task_list')
    else:
        form = TaskUpdateForm(instance=task)
    return render(request, 'main/task_form.html', {'form': form})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        task.is_deleted = True
        task.save()
        return redirect('main:task_list')
    return render(request, 'main/task_delete.html', {'task': task})


@login_required
def mark_task_done(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        task.status = 'done'
        task.save()
    return redirect('main:task_list')


@login_required
def calendar(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача успешно добавлена!')
            return redirect('main:calendar')
    else:
        form = TaskForm()
    return render(request, 'main/calendar.html', {'form': form})
