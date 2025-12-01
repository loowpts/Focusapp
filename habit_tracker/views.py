from django.shortcuts import render, redirect, get_object_or_404
from .models import Habit, DailyRecord
from .forms import HabitForm, DailyRecordForm
from django.contrib.auth.decorators import login_required


@login_required
def daily_habits(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, 'habit_tracker/daily_habits.html', {'habits': habits})

@login_required
def habit_detail(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
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
    return render(request, 'habit_tracker/habit_form.html', {'form': form})

@login_required
def habit_edit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect('habit_tracker:habit_detail', pk=pk)
    else:
        form = HabitForm(instance=habit)
    return render(request, 'habit_tracker/habit_edit.html', {'form': form, 'habit': habit})

@login_required
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    habit.delete()
    return redirect('habit_tracker:daily_habits')

@login_required
def daily_record(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        form = DailyRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.habit = habit
            record.save()
            return redirect('habit_tracker:habit_detail', pk=pk)
    else:
        form = DailyRecordForm()
    daily_records = habit.habit_dailyrecords.all()
    return render(request, 'habit_tracker/daily_record.html', {'form': form, 'habit': habit, 'daily_records': daily_records})

@login_required
def edit_daily_record(request, pk):
    record = get_object_or_404(DailyRecord, pk=pk, habit__user=request.user)
    if request.method == 'POST':
        form = DailyRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('habit_tracker:habit_detail', pk=record.habit.pk)
    else:
        form = DailyRecordForm(instance=record)
    return render(request, 'habit_tracker/edit_daily_record.html', {'form': form, 'record': record})
