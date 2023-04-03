from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import format_html
from django.urls import reverse

ROLE_CHOICES = (
    ('1','ผู้ดูแลระบบ'),
    ('2','หมอ'),
    ('3','พยาบาล'),  
)

GENDER_CHOICE = (
    ('ชาย','ชาย'),
    ('หญิง','หญิง'),
    ('ไม่ระบุ','ไม่ระบุ'),
    )

NAME_TITLE_CHOICE = (
    ('นาย','นาย'),
    ('นางสาว','นางสาว'),
    ('นาง','นาง'),
    ('นายแพทย์','นายแพทย์'),
    ('แพทย์หญิง','แพทย์หญิง'),
    ('ดอกเตอร์','ดอกเตอร์'),
    ('รองศาสตราจารย์','รองศาสตราจารย์'),
    ('ศาสตราจารย์','ศาสตราจารย์'),
)
  
class MyUser(AbstractUser):
    email = models.EmailField(max_length=255, verbose_name="อีเมล", unique=True)
    is_doctor = models.BooleanField(default=False, verbose_name='หมอ', blank=True, null=True)
    is_nurse = models.BooleanField(default=False, verbose_name='พยาบาล' , blank=True, null=True)
    is_admin = models.BooleanField(default=False, verbose_name='ผู้ดูแลระบบ' , blank=True, null=True)
    title = models.CharField(max_length=30, choices=NAME_TITLE_CHOICE, default="นาย", verbose_name='คำนำหน้าชื่อ')
    slug = models.SlugField(max_length=200)
    
class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    age = models.CharField(max_length=10, verbose_name='อายุ')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, default="ชาย", verbose_name='เพศ')
    dob = models.CharField(max_length=10, verbose_name='วันเกิด')
    phone = models.CharField(max_length=10, verbose_name='เบอร์โทรศัพท์มือถือ')
    idCard = models.CharField(max_length=13, verbose_name='เลขบัตรประจำตัวประชาชน')
    address = models.TextField(max_length=500, verbose_name='ที่อยู่')
    img = models.ImageField(upload_to='Image', default='', verbose_name='รูปภาพ')
    medicalLicense = models.ImageField(upload_to='MedicalLicense', default='', verbose_name='รูปภาพใบประกอบวิชาชีพ')
    updatedAt = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        return str(self.user) + self.age + str(self.gender) + self.dob + self.phone + self.idCard + self.address + self.img.url + self.medicalLicense.url

    def image(self):
        if self.img:
            return format_html('<img src="' + self.img.url + '" height="40px">')
        return ''
    image.allow_tags = True
    image.short_description = "รูปภาพ"
    
    def image2(self):
        if self.img:
            return format_html('<img src="' + self.medicalLicense.url + '" height="40px">')
        return ''
    image2.allow_tags = True
    image2.short_description = "ใบประกอบวิชาชีพ"

    