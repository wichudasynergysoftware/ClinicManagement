from django.db import models
from django.utils.html import format_html
from django.urls import reverse
from Patient.models import Patient, TreatmentHistory

class EventAppointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=False)
    treatment = models.ForeignKey(TreatmentHistory, on_delete=models.CASCADE, null=True, blank=False)
    doctorId = models.PositiveIntegerField(blank=True, null=True)
    patientName = models.CharField(max_length=50, blank=True, null=True,)
    patientTitle = models.CharField(max_length=50, blank=True, null=True, verbose_name='คำนำหน้าชื่อ')
    doctorName = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=200, verbose_name='ชื่อการนัด')
    description = models.TextField(max_length=1000, blank=True, null=True, verbose_name='คำอธิบายเพิ่มเติม')
    date = models.DateField(verbose_name='วันที่นัดคนไข้')
    createdAt = models.DateTimeField(auto_now_add=True, blank=False)
    updatedAt = models.DateTimeField(auto_now=True, blank=False)

    @property 
    def get_html_url(self):
        url = reverse('Appointment:event_edit', args=(self.id,))
        return f'<a class="appointment-name" href="{url}"><ul class="day-ul"><li class="li li-test">{self.patientTitle}{self.patientName}</li></ul></a>'
