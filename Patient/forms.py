from django import forms
from .models import *
import datetime
from django.contrib.auth.forms import UserCreationForm
        
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient 
        widgets = {
            'dob': forms.DateInput(format=('%d-%m-%Y'), attrs={'pattern=': '\d{4}-\d{2}-\d{2}', 'lang': 'TH', 'format': 'yyyy-mm-dd', 'type': 'date'}),
            'address': forms.Textarea(attrs={'rows':3}),
        }
        exclude = ['id', 'age', 'slug', 'createdAt', 'updatedAt', 'deletedAt', 'number']
        
class PatientQueueForm(forms.ModelForm):
    class Meta:
        model = PatientQueue
        exclude = ['id', 'createdAt', 'updatedAt', 'patient']
        
class TreatmentHistoryForm(forms.ModelForm):
    class Meta:
        model = TreatmentHistory
        exclude = ['id', 'createdAt', 'updatedAt', 'patient', 'patientName', 'initial'
                   , 'patientTitle', 'doctorName']
        
class PatientQueueForm(forms.ModelForm):
    class Meta:
        model = PatientQueue
        exclude = ['id', 'createdAt', 'updatedAt', 'patient', 'patientName', 'patientTitle']
        
class AllergicHistoryForm(forms.ModelForm):
    class Meta:
        model = Allergic
        exclude = ['id', 'createdAt', 'updatedAt', 'patient', 'patientName', 'patientTitle', 
                   'sequence', 'deletedAt', 'doctorName']
        
class InitialSymptomsForm(forms.ModelForm):
    class Meta:
        model = InitialSymptoms
        exclude = ['id', 'createdAt', 'updatedAt', 'nurseId', 'patient']
        
class SuccessfulTreatmentForm(forms.ModelForm):
    class Meta:
        model = SuccessfulTreatment
        exclude = ['id', 'createdAt', 'updatedAt', 'patient', 'treatment', 'queue', 'patientName', 'treatmentName', 'queueStatus',
                   'appointment', 'prescription', 'status1']
        
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        widgets = {
            'date': forms.DateInput(format=('%d-%m-%Y'), attrs={'pattern=': '\d{4}-\d{2}-\d{2}', 'lang': 'TH', 'format': 'yyyy-mm-dd', 'type': 'date'}),
            'description': forms.Textarea(attrs={'rows':3}),
        }
        exclude = ['id', 'createdAt', 'updatedAt', 'patient', 'patientName', 'patientTitle'
                   , 'doctorName', 'slug']