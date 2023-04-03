from django import forms
from .models import *
        
class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        exclude = ['id', 'treatment', 'patient', 'createdAt', 'updatedAt', 'deletedAt', 
                   'patientName', 'doctorName', 'medicine', 'total']
        