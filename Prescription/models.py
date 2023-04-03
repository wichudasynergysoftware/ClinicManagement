from django.db import models
from MedicineStock.models import *
from Patient.models import Patient, TreatmentHistory
from MedicineStock.models import Medicine
from Unit.models import MedicineUnit

MEDICINE_UNIT_CHOICE = (
    ('เม็ด','เม็ด'),
    ('ขวด','ขวด'),
    ('ตลับ','ตลับ'),
    ('ซอง','ซอง'),
    ('กระปุก','กระปุก'),
    ('หลอด','หลอด'),
)

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=False)
    treatment = models.ForeignKey(TreatmentHistory, on_delete=models.CASCADE, null=True, blank=False)
    patientName = models.CharField(max_length=50, blank=True, null=True, verbose_name='ชื่อคนไข้')
    doctorName = models.CharField(max_length=50, blank=True, null=True, verbose_name='ชื่อหมอ')
    medicine = models.ForeignKey(Medicine, on_delete=models.SET_NULL, verbose_name='ชื่อยา', null=True)
    medicineAmount = models.IntegerField(verbose_name='จำนวน')
    medicineUnit = models.ForeignKey(MedicineUnit, verbose_name='หน่วยบรรจุ', on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, blank=False)
    updatedAt = models.DateTimeField(auto_now=True, blank=False)
    deletedAt = models.DateTimeField(auto_now=True, blank=False)
