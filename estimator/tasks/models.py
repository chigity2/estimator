from django.db import models

class Task(models.Model):
    task = models.TextField()
    assigned_to = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    