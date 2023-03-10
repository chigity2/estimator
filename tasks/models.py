from django.db import models
from django.forms import CharField, DateTimeField, IntegerField

class Tasks(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    complete = models.BooleanField(default=False)
    created = models.DateTimeField('task created')

    def _str_(self):
        return self.title
    
