from django import forms
from .models import *
        
class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine 
        exclude = ['id', 'slug', 'createdAt', 'updatedAt', 'deletedAt']
        