from django.db import models
from subs.models import Trades, Subcontractors, SubTrades
from django.contrib.auth.models import User

# Create your models here.


class Notes(models.Model):
    note = models.CharField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)
    note_person = models.CharField(max_length=300)

    def __str__(self):
        return str(self.date_added) + ' ' + (self.note_person)

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"


class Owners(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Owner"
        verbose_name_plural = "Owners"


class OwnersContacts(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    direct = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)

    class Meta:
        verbose_name = "Owner Contact"
        verbose_name_plural = "Owner Contacts"

class Architects(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Architect"
        verbose_name_plural = "Architects"


class ArchitectsContacts(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    direct = models.CharField(max_length=200)

    def __str__(self):
        return str(first_name) + ' ' + str(self.last_name)

    class Meta:
        verbose_name = "Architect Contact"
        verbose_name_plural = "Architect Contacts"


class Projects(models.Model):
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=4)
    zip = models.CharField(max_length=200)
    state_pw = models.BooleanField(default=False)
    davis_bacon = models.BooleanField(default=False)
    units = models.IntegerField(default=0, blank=True, null=True)
    description = models.CharField(max_length=200)
    owner = models.ForeignKey(Owners, blank=True, null=True, on_delete=models.SET_NULL)
    architect = models.ForeignKey(Architects, blank=True, null=True, on_delete=models.SET_NULL)
    owner_contact = models.ForeignKey(OwnersContacts, blank=True, null=True, on_delete=models.SET_NULL)
    architect_contact = models.ForeignKey(ArchitectsContacts, blank=True, null=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)


    def __str__(self):
        return str(self.name) + ' ' + str(self.city) + ', ' + str(self.state)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class ProjectNotes(models.Model):
    note = models.CharField(max_length=500)
    employee = models.CharField(max_length=4)
    date_added = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.note)

    class Meta:
        verbose_name = "Project Note"
        verbose_name_plural = "Project Notes"


class Bids(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.SET_NULL, null=True, blank=True, related_name="proj_bid")
    bid_number = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_due = models.DateTimeField(blank=True, null=True)
    plans = models.CharField(max_length=200)
    status = models.CharField(max_length=200, blank=True, null=True)
    sub_bids_due = models.DateTimeField(blank=True,null=True)


    def __str__(self):
        return str(self.project.name) + ' ' + str(self.bid_number)

    class Meta:
        verbose_name = "Bid"
        verbose_name_plural = "Bids"


class Packages(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.SET_NULL, null=True, blank=True, related_name="proj_package")
    bid = models.ForeignKey(Bids, on_delete=models.SET_NULL, null=True, blank=True, related_name='bid_package')
    trade = models.ForeignKey(Trades, on_delete=models.SET_NULL, null=True, blank=True, related_name='trade_package')
    estimator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='package_estimator')
    value = models.IntegerField(default=0)


    def __str__(self):
        return str(self.project.name) + ' ' + str(self.bid.bid_number) + ' ' + str(self.trade.code) + ' - ' + str(self.trade.name)

    class Meta:
        verbose_name = "Package"
        verbose_name_plural = "Packages"


class SubPackages(models.Model):
    bid_package = models.ForeignKey(Packages, on_delete=models.SET_NULL, null=True, blank=True, related_name="sub_bid_package")
    sub = models.ForeignKey(Subcontractors, on_delete=models.SET_NULL, null=True, blank=True, related_name='sub_pack_sub')
    bidding = models.BooleanField(default=False)
    received = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.bid_package.project.name) + ' ' + str(self.bid_package.bid.bid_number) + ': ' + str(self.sub.name)

    class Meta:
        verbose_name = "Sub Package"
        verbose_name_plural = "Sub Packages"

