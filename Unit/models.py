from django.db import models

class MedicineUnit(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='ชื่อหน่วยยา', default='เม็ด', unique=True)
    createdAt = models.DateTimeField(auto_now_add=True, blank=False)
    updatedAt = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        return self.name
    
class MedicineType(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='ชื่อประเภทยา', default='ยาน้ำ', unique=True)
    createdAt = models.DateTimeField(auto_now_add=True, blank=False)
    updatedAt = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        return self.name
    
class ThailandNationalListOfEssentialMedicines(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='บัญชียาหลักแห่งชาติ', default='บัญชี ก.', unique=True)
    createdAt = models.DateTimeField(auto_now_add=True, blank=False)
    updatedAt = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        return self.name
    
class NameTitle(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='คำนำหน้าชื่อ', unique=True)
    createdAt = models.DateTimeField(auto_now_add=True, blank=False)
    updatedAt = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        return self.name
    
class WorkingTime(models.Model):
    time = models.TimeField(max_length=100, blank=True, null=True, verbose_name='ช่วงเวลา', unique=True)
    createdAt = models.DateTimeField(auto_now_add=True, blank=False)
    updatedAt = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        return self.time