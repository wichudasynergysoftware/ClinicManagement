from django import forms
from .models import *
        
class EventAppointmentForm(forms.ModelForm):
  class Meta:
    model = EventAppointment
    widgets = {
        # 'date': forms.DateInput(format='%Y-%m-%dT%H:%M', attrs={'pattern=': '\d{4}-\d{2}-\d{2}', 'lang': 'TH', 'format': 'yyyy-mm-dd', 'type': 'date'}),
        'date': forms.DateInput(attrs={'type': 'datetime-local', 'pattern=': '\d{4}-\d{2}-\d{2}'}, format='%Y-%m-%dT%H:%M'),
        'description': forms.Textarea(attrs={'rows':3}),
    }
    exclude = ['id', 'createdAt', 'updatedAt', 'patient', 'patientName', 'patientTitle'
                   , 'doctorName', 'doctorId', 'treatment']

  def __init__(self, *args, **kwargs):
    super(EventAppointmentForm, self).__init__(*args, **kwargs)
    self.fields['date'].input_formats = ('%Y-%m-%dT%H:%M',)
    # self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
