from django.db import models

class Subcontractor(models.Model):
    sub_name = models.CharField(max_length=100)
    sub_address = models.CharField(max_length=50)
    sub_city = models.CharField(max_length=50)
    sub_state = models.CharField(max_length=2)
    sub_zip = models.IntegerField(default=95747)
    sub_date_added = models.DateTimeField('sub added')

    


