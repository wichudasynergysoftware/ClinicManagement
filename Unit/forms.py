from django import forms
from .models import *
import datetime as dt
HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]

class MedicineUnitForm(forms.ModelForm):
    class Meta:
        model = MedicineUnit
        exclude = ['id', 'createdAt', 'updatedAt']
        
class MedicineTypeForm(forms.ModelForm):
    class Meta:
        model = MedicineType
        exclude = ['id', 'createdAt', 'updatedAt']
        
class ThailandNationalListOfEssentialMedicinesForm(forms.ModelForm):
    class Meta:
        model = ThailandNationalListOfEssentialMedicines
        exclude = ['id', 'createdAt', 'updatedAt']
        
class NameTitleForm(forms.ModelForm):
    class Meta:
        model = NameTitle
        exclude = ['id', 'createdAt', 'updatedAt']
        
class WorkingTimeForm(forms.ModelForm):
    class Meta:
        model = WorkingTime
        widgets = {
            'time': forms.DateInput(format=('%H-%i-%A'), attrs={'pattern=': '\d{2}-\d{2}-\d{2}', 'lang': 'TH', 'format': 'HH-ii-a', 'type': 'time'}),
        }
        exclude = ['id', 'createdAt', 'updatedAt']