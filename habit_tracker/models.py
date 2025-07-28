from django.db import models
from django.contrib.auth.models import User


class BaseMode(models.Model):
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_habits', null=True)
    habit = models.CharField(max_length=250)
    created_date = models.DateField(db_index=True, auto_now_add=True)
    target_goal = models.IntegerField(null=True)
    unit_of_measure = models.CharField(max_length=250)

    def __str__(self) -> str:
        return f'{self.habit}'
    

class DailyRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='habit_dailyrecords', null=True)
    date_completed = models.DateField(db_index=True, auto_now_add=True)
    goal_status = models.IntegerField(null=True)
