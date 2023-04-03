from django.db import models
from Unit.models import *

MEDICINE_TYPE_CHOICE = (
    ('ยากิน', (
        ('ยาน้ำ', 'ยาน้ำ'), 
        ('ยาเม็ด', 'ยาเม็ด'), 
        ('ยาผง (ละลายน้ำ)', 'ยาผง (ละลายน้ำ)')
        )),
    ('ยาทา', (
        ('ยาทาประเภทครีม', 'ยาทาประเภทครีม'),
        ('ยาทาประเภทน้ำ', 'ยาทาประเภทน้ำ'),
        )),
    ('ยาฉีด','ยาฉีด'),
    ('ยาอื่น ๆ','ยาอื่น ๆ'),
    )

MEDICINE_UNIT_CHOICE = (
    ('เม็ด','เม็ด'),
    ('ขวด','ขวด'),
    ('ตลับ','ตลับ'),
    ('ซอง','ซอง'),
    ('กระปุก','กระปุก'),
    ('หลอด','หลอด'),
)
    
# ยาในคลังยาของคลินิก
class Medicine(models.Model):
    medCode = models.CharField(max_length=50, verbose_name='รหัสยา', unique=True)
    type = models.ForeignKey(MedicineType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='ประเภทของยา')
    packingUnit = models.ForeignKey(MedicineUnit, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='หน่วยบรรจุ')
    nlem = models.ForeignKey(ThailandNationalListOfEssentialMedicines, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='บัญชียาหลักแห่งชาติ')
    name = models.CharField(max_length=100, verbose_name='ชื่อยา', unique=True)
    slug = models.SlugField(max_length=200)
    tradeName = models.CharField(max_length=100, verbose_name='ชื่อทางการค้า') # ชื่อทางการค้า
    genericName = models.CharField(max_length=100, verbose_name='ชื่อสามัญทางยา') # ชื่อยาสามัญ
    initial = models.CharField(max_length=20, verbose_name='ชื่อย่อ') # อักษรย่อ ตัวย่อของยา
    countingUnit = models.FloatField(max_length=10, verbose_name='หน่วยนับ')
    costPrice = models.FloatField(verbose_name='ราคาซื้อ')
    sellingPrice = models.FloatField(verbose_name='ราคาขาย')
    medicineStrength = models.CharField(max_length=500, verbose_name='ความแรงของยา') # ความแรงของยา
    indication = models.CharField(max_length=500, verbose_name='สรรพคุณของยา') # สรรพคุณของยา
    direction = models.CharField(max_length=500, verbose_name='คำเตือนการใช้ยา') # คำเตือนการใช้ยา
    createdAt = models.DateTimeField(auto_now_add=True, blank=False)
    updatedAt = models.DateTimeField(auto_now=True, blank=False)
    deletedAt = models.DateTimeField(auto_now=True, blank=False)
    
    def __str__(self):
        return self.name

# ยาในห้องจ่ายยา ซึ่งจะรับยาจากคลังยา
class MedicineFrontStock(models.Model):
    code = models.CharField(max_length=100)

    