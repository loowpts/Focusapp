from django.shortcuts import render, redirect, get_object_or_404
from .models import Habit, BaseMode, DailyRecord
from .forms import HabitForm, DailyRecordForm
from django.contrib.auth.decorators import login_required


@login_required
def daily_habits(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, 'habit_tracker/daily_habits.html', {'habits': habits})


@login_required
def habit_detail(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    return render(request, 'habit_tracker/habit_detail.html', {'habit': habit})


@login_required
def habit_new(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('habit_tracker:habit_detail', pk=habit.pk)
    else:
        form = HabitForm()
    return render(request, 'habit_tracker/habit_edit.html', {'form': form})


@login_required
def habit_edit(request, pk):
    post = get_object_or_404(Habit, pk=pk)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('habit_tracker:habit_detail', pk=pk)
    else:
        form = HabitForm(instance=post)
    return render(request, 'habit_tracker/habit_edit.html', {'form': form})


@login_required
def habit_delete(request, pk):
    post = get_object_or_404(Habit, pk=pk)
    post.delete()
    return redirect('habit_tracker:daily_habits.html')


@login_required
def daily_record(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    daily_record = habit.dailyrecord.all()
    return render(request, 'habit_tracker/habit_detail.html', {'daily_record': daily_record})


@login_required
def edit_daily_record(request, pk):
    post = get_object_or_404(Habit, pk=pk)
    if request.method == 'POST':
        form = DailyRecordForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('habit_tracker/habit_detail', pk.post.pk)
    else:
        form = DailyRecordForm(instance=post)
    return render(request, 'habit_tracker/habit_detail.html', {'form': form})


