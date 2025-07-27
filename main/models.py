from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'In progress'),
        ('done', 'Done'),
    )
    STATUS_PRIORITY = (
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField(default=timezone.now)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='done')
    priority = models.CharField(max_length=50, choices=STATUS_PRIORITY, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_priority_color(self):
        return {
            'low': 'info',
            'medium': 'warning',
            'high': 'danger',
        }.get(self.priority, 'secondary')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self) -> str:
        return f'{self.title} ({self.user.username})'


