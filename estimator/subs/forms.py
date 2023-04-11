from django import forms
from .models import Employees, Subcontractors


class AddEmployeeForm(forms.ModelForm):

    class Meta:
        model = Employees
        fields = ('first_name', 'last_name', 'email', 'phone')

class AddSubcontractorForm(forms.ModelForm):
    class Meta:
        model = Subcontractors
        fields = ('name', 'address1', 'address2', 'city', 'state', 'zip', 'phone', 'fax', 'union', 'pw')