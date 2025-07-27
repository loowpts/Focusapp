from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    STATUS_CHOICES = (
        ('todo', 'Ожидает'),
        ('in_progress', 'В процессе'),
        ('done', 'Выполнено'),
    )
    STATUS_PRIORITY = (
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField(null=True, blank=True)
    deadline = models.DateField(default=timezone.now)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=50, choices=STATUS_PRIORITY, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_priority_color(self):
        return {
            'low': 'info',
            'medium': 'warning',
            'high': 'danger',
        }.get(self.priority, 'secondary')
    
    def get_status_color(self):
        return {
            'todo': 'secondary',
            'in_progress': 'primary',
            'done': 'success',
        }.get(self.status, 'light')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self) -> str:
        return f'{self.title} ({self.user.username})'


