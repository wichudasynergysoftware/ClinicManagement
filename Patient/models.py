from django.db import models
from django.utils.html import format_html
from django.urls import reverse
from Unit.models import *

GENDER_CHOICE = (
    ('ชาย','ชาย'),
    ('หญิง','หญิง'),
    ('ไม่ระบุ','ไม่ระบุ'),
    )

NAME_TITLE_CHOICE = (
    ('นาย','นาย'),
    ('นาง','นาง'),
    ('นางสาว','นางสาว'),
    ('เด็กหญิง','เด็กหญิง'),
    ('เด็กชาย','เด็กชาย'),
)

BLOOD_TYPE_CHOICES =(
    ('A','A'),
    ('B','B'),
    ('AB','AB'),
    ('O','O'),
)

STATUS_CHOICES =(
    ('รอเข้าพบแพทย์','รอเข้าพบแพทย์'),
    ('กำลังเข้าพบแพทย์','กำลังเข้าพบแพทย์'),
    ('ตรวจสำเร็จ','ตรวจสำเร็จ'),
    ('เสร็จสิ้น','เสร็จสิ้น'),
)

class Patient(models.Model):
    hn = models.CharField(max_length=50, verbose_name='เลขประจำตัวคนไข้', unique=True)
    name = models.CharField(max_length=50, verbose_name='ชื่อ-นามสกุล')
    slug = models.SlugField(max_length=200)
    age = models.CharField(max_length=10)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, default="ชาย", verbose_name='เพศ')
    title = models.ForeignKey(NameTitle, on_delete=models.CASCADE, verbose_name='คำนำหน้าชื่อ', blank=True, null=True)
    # title = models.CharField(max_length=10, choices=NAME_TITLE_CHOICE, default="นาย", verbose_name='คำนำหน้าชื่อ')
    dob = models.CharField(max_length=10, verbose_name='วันเกิด')
    phone = models.CharField(max_length=10, verbose_name='เบอร์โทรศัพท์')
    idCard = models.CharField(max_length=13, verbose_name='เลขบัตรประจำตัวประชาชน', unique=True)
    address = models.TextField(max_length=500, verbose_name='ที่อยู่')
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='ที่อยู่อีเมล์')
    img = models.ImageField(upload_to='Image', default='', blank=True, null=True, verbose_name='รูปภาพ')
    bloodType = models.CharField(max_length=10, verbose_name='หมู่เลือด', choices=BLOOD_TYPE_CHOICES)
    underlyingDisease = models.CharField(max_length=500, verbose_name='โรคประจำตัว', null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, blank=False)
    updatedAt = models.DateTimeField(auto_now=True, blank=False)
    deletedAt = models.DateTimeField(auto_now=True, blank=False)
    number = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.hn + str(self.title) + self.name + self.age + str(self.gender) + self.dob + self.phone + self.idCard + self.address + self.email + f'{self.createdAt}' + f'{self.updatedAt}'

    def image(self):
        if self.img:
            return format_html('<img src="' + self.img.url + '" height="40px">')
        return ''
    image.allow_tags = True
    image.short_description = "Image"
    
# รายการแพ้ยาของคนไข้
class Allergic(models.Model):
    hn = models.CharField(max_length=50, blank=True, null=True, verbose_name='เลขประจำตัวคนไข้')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=False)
    patientTitle = models.CharField(max_length=50, blank=True, null=True, verbose_name='คำนำหน้าชื่อ')
    patientName = models.CharField(max_length=50, blank=True, null=True, verbose_name='ชื่อคนไข้')
    doctorName = models.CharField(max_length=50, blank=True, null=True, verbose_name='ชื่อหมอ')
    sequence = models.IntegerField(blank=True, null=True, verbose_name='ลำดับการแพ้ยา')
    allergicMedicineName = models.CharField(max_length=100, blank=True, null=True, verbose_name='ชื่อยาที่แพ้') # ชื่อยาที่แพ้ กรณีที่ไม่มียานั้นในคลินิก
    allergicSymptom = models.CharField(max_length=500, blank=True, verbose_name='อาการแพ้ยา') # อาการของการแพ้
    createdAt = models.DateTimeField(auto_now_add=True, blank=False)
    updatedAt = models.DateTimeField(auto_now=True, blank=False)
    deletedAt = models.DateTimeField(auto_now=True, blank=False)
    
    def __str__(self):
        return self.patientName
    
class InitialSymptoms(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=False)
    weight = models.IntegerField(blank=True, null=True, verbose_name='น้ำหนัก')
    height = models.FloatField(max_length=10, blank=True, null=True, verbose_name='ส่วนสูง')
    temp = models.FloatField(max_length=10, blank=True, null=True, verbose_name='อุณหภูมิ')
    pressure = models.CharField(max_length=10, blank=True, null=True, verbose_name='ความดันโลหิต')
    pulse = models.CharField(max_length=10, blank=True, null=True, verbose_name='ชีพจร')
    initialSymptoms = models.CharField(max_length=1000, blank=True, null=True, verbose_name='อาการ')
    nurseId = models.CharField(max_length=100, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, blank=False)
    updatedAt = models.DateTimeField(auto_now=True, blank=False)
    
    def __str__(self):
        return str(self.patient)
    
class PatientQueue(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=False)
    patientTitle = models.CharField(max_length=50)
    patientName = models.CharField(max_length=50)
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, blank=False)
    updatedAt = models.DateTimeField(auto_now=True, blank=False)
    
    def __str__(self):
        return str(self.patient)
    
class TreatmentHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=False)
    initial = models.ForeignKey(InitialSymptoms, on_delete=models.CASCADE, null=True, blank=False)
    patientTitle = models.CharField(max_length=50)
    patientName = models.CharField(max_length=50)
    doctorName = models.CharField(max_length=50, blank=True, null=True, verbose_name='ชื่อหมอ')
    initialSymptoms = models.CharField(max_length=1000, blank=True, null=True, verbose_name='อาการ')
    initialSymptoms1 = models.CharField(max_length=1000, blank=True, null=True, verbose_name='ผลการวินิจฉัย')
    number = models.IntegerField(null=True, blank=True)
    app = models.CharField(max_length=50, null=True, blank=True)
    pres = models.CharField(max_length=50, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, blank=False)
    updatedAt = models.DateTimeField(auto_now=True, blank=False)
    
    def __str__(self):
        return str(self.patient)
    
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=False)
    doctorId = models.PositiveIntegerField(blank=True, null=True,)
    patientName = models.CharField(max_length=40, blank=True, null=True,)
    patientTitle = models.CharField(max_length=100, blank=True, null=True, verbose_name='คำนำหน้าชื่อ')
    doctorName = models.CharField(max_length=40, blank=True, null=True,)
    name = models.CharField(max_length=200, verbose_name='ชื่อการนัด')
    description = models.TextField(max_length=1000, blank=True, null=True, verbose_name='คำอธิบายเพิ่มเติม')
    date = models.DateField(max_length=100, verbose_name='วันที่นัดคนไข้') # วันที่นัดคนไข้
    createdAt = models.DateTimeField(auto_now_add=True, blank=False)
    updatedAt = models.DateTimeField(auto_now=True, blank=False)
    
    def __str__(self):
        return str(self.patient)

class SuccessfulTreatment(models.Model):
    patientName = models.CharField(max_length=50, null=True, blank=True)
    treatmentName = models.CharField(max_length=500, null=True, blank=True)
    queueStatus = models.CharField(max_length=50, null=True, blank=True)
    appointment = models.CharField(max_length=50, null=True, blank=True)
    prescription = models.CharField(max_length=50, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=False)
    treatment = models.ForeignKey(TreatmentHistory, on_delete=models.CASCADE, null=True, blank=False)
    queue = models.ForeignKey(PatientQueue, on_delete=models.CASCADE, null=True, blank=False)
    status1 = models.CharField(max_length=50, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, blank=False)
    updatedAt = models.DateTimeField(auto_now=True, blank=False)
    
    def __str__(self):
        return str(self.patient) + str(self.treatment)