from django.contrib import admin
from .models import Habit
from django.contrib.auth.admin import UserAdmin

admin.site.register(Habit)
