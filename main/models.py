from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'In progress'),
        ('done', 'Done'),
    )
    STATUS_PRIORITY = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='done')
    priority = models.CharField(max_length=10, choices=STATUS_PRIORITY, default='low')
    created_at = models.DateTimeField(auto_now_add=True)
    
        


