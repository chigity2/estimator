from django.db import models

# Create your models here.


class Subcontractors(models.Model):
    name = models.CharField(max_length=50)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50,null=True, blank=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=12)
    phone = models.CharField(max_length=20)
    primary_contact = models.IntegerField(null=True, blank=True, default=None)
    fax = models.CharField(max_length=14, null=True, blank=True, default=None)
    union = models.BooleanField(default=False)
    pw = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


class Employees(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20)
    sub = models.ForeignKey(Subcontractors, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)


class PrimaryContact(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    sub = models.ForeignKey(Subcontractors, on_delete=models.CASCADE)


class Trades(models.Model):
    code = models.CharField(max_length=12)
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.code) + ' ' + str(self.name)


class SubTrades(models.Model):
    sub = models.ForeignKey(Subcontractors, on_delete=models.CASCADE)
    trade = models.ForeignKey(Trades, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.sub.name) + ': ' + str(self.trade.name)


class SubNotes(models.Model):
    note = models.TextField()
    employee = models.CharField(max_length=4)
    sub = models.ForeignKey(Subcontractors, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.employee) + ': ' + str(self.time_created)
