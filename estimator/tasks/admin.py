from django.contrib import admin
from tasks.models import Task, Logs
from subs.models import Trades, Subcontractors, Employees, SubNotes
# Register your models here.
admin.site.register(Task)
admin.site.register(Logs)
admin.site.register(Trades)
admin.site.register(Subcontractors)
admin.site.register(Employees)
admin.site.register(SubNotes)