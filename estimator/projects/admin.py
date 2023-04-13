from django.contrib import admin
from .models import Bids, Projects, Architects, Owners, Notes, ProjectNotes, ArchitectsContacts, OwnersContacts, SubPackages
# Register your models here.

admin.site.register(Bids)
admin.site.register(Projects)
admin.site.register(Architects)
admin.site.register(Owners)
admin.site.register(OwnersContacts)
admin.site.register(ArchitectsContacts)
admin.site.register(Notes)
admin.site.register(ProjectNotes)
admin.site.register(SubPackages)