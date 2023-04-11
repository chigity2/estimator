from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    task_name = models.TextField()
    assigned_to = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.task_name


class Logs(models.Model):
    task_date = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=5)
    task = models.CharField(max_length=500)
    completed_date = models.DateTimeField(blank=True, null=True)
    active_task = models.BooleanField(default=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="task_by_user")

    def __str__(self):
        return str(self.user.first_name) + ' ' + str(self.user.last_name) + ': ' + str(self.task)

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'