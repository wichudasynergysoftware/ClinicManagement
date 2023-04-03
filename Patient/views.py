from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from ClinicManagement.models import MyUser
from xhtml2pdf import pisa
from Prescription.models import Prescription
from .models import *
from .forms import *
from django.utils.text import slugify
from unidecode import unidecode
from django.template import defaultfilters
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime, pytz
from django.db.models import Sum
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4, letter
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date
from django.utils.safestring import mark_safe
from Appointment.forms import EventAppointmentForm
from Prescription.forms import PrescriptionForm
from django.utils import timezone
from Appointment.models import EventAppointment
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from MedicineStock.models import Medicine
from Unit.models import MedicineUnit
from django.contrib.auth.decorators import user_passes_test
import csv
import pdfkit
from django.template.loader import get_template
from io import BytesIO
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet

def check_staff(user: MyUser):
    return user.is_staff or user.is_superuser

def check_nurse(user: MyUser):
    return user.is_staff or user.is_superuser or user.is_nurse

def check_doctor(user: MyUser):
    return user.is_staff or user.is_superuser or user.is_doctor

# pdfmetrics.registerFont(TTFont('F1', 'angsana.ttc'))
pdfmetrics.registerFont(TTFont('THSarabunNew', 'Patient/static/font/THSarabunNew.ttf'))
pdfmetrics.registerFont(TTFont('THSarabunNew-Bold', 'Patient/static/font/THSarabunNew Bold.ttf'))
    
# real export patient data PDF
def export_patient_record(request, id):
    tz = pytz.timezone('Asia/Bangkok')
    now1 = datetime.now(tz)
    month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[now1.month]
    thai_year = now1.year + 543
    time_str = now1.strftime('%H:%M:%S')
    d = "%d %s %d %s"%(now1.day, month_name, thai_year, time_str)
    
    patient = get_object_or_404(Patient, id=id)
    logo = ImageReader('Patient/static/icon/logo-color.png')
    
    # if patient.img:
    #     img = ImageReader('ClinicManagement/static'+patient.img.url)
    # else :
    #     img = ImageReader('Patient/static/icon/default-user.png')

    response = HttpResponse(content_type='application/pdf')
    # d = date.today()
    response['Content-Disposition'] = f'inline; filename="{d}.pdf"'
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    # Width, Height = letter
    
    # x = datetime.strptime(patient.dob, '%Y-%m-%d').strftime('%d %B %Y')
    # print(type(x))
    # show thai datetime format in pdf 
    dob = patient.dob
    dobSplit = dob.split("-")
    dobYear = dobSplit[0]
    dobDay = dobSplit[2]
    dobMonth = dobSplit[1]

    mo = int(dobMonth)
    month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[mo]
    thai_year = int(dobYear) + 543
    x = ("%d %s %d"%(int(dobDay), month_name, thai_year))
    
    # data = {
    #     "": [{"เลขประจำตัวผู้ป่วย": patient.hn},
    #         {"คำนำหน้าชื่อ/ยศ/ตำแหน่ง": str(patient.title)},
    #         {"ชื่อและนามสกุล": patient.name},
    #         {"หมู่เลือด": patient.bloodType},
    #         {"โรคประจำตัว": patient.underlyingDisease},
    #         {"เลขบัตรประจำตัวประชาชน": patient.idCard},
    #         {"เพศ": patient.gender},
    #         {"อายุ": patient.age + "  " + "ปี"},
    #         {"วันเกิด": x},
    #         {"เบอร์โทรศัพท์": patient.phone},
    #         {"ที่อยู่อาศัย": patient.address},
    #         {"อีเมล": patient.email},
    #     ],
    # }
  
    p.drawImage(logo, 120, 750, mask='auto')
    # p.drawImage(img, 50, Height/2.8, width=Width/3, preserveAspectRatio=True, mask='auto')
    p.setFont("THSarabunNew-Bold", 18, leading=None)
    # p.setFillColorRGB(0.29296875, 0.453125, 0.609375)
    p.drawString(245, 755, "ระเบียนประวัติผู้ป่วย")
    p.drawString(490, 800, "*"+patient.hn+"*")
    p.drawString(170, 725, "ออกประวัติผู้ป่วยเมื่อ")
    p.drawString(280, 725, str(d))
    p.drawString(72, 677, "ข้อมูลผู้ป่วย")
    p.drawString(72, 287, "รายการแพ้")
    
    if not patient == None:
        p.setFont("THSarabunNew-Bold", 14, leading=None)
        p.drawString(50, 640, "เลขที่บัตรประจำตัวประชาชน")
        p.drawString(50, 605, "คำนำหน้าชื่อ/ยศ/ตำแหน่ง")
        p.drawString(340, 605, "ชื่อ")
        p.drawString(50, 570, "วันเดือนปีเกิด")
        p.drawString(340, 570, "อายุ")
        p.drawString(50, 535, "เพศ")
        p.drawString(50, 500, "ที่อยู่ปัจจุบัน")
        p.drawString(50, 465, "โทรศัพท์(มือถือ)")
        p.drawString(50, 430, "อีเมลที่ติดต่อได้")
        p.drawString(50, 395, "โรคประจำตัว")
        p.drawString(50, 360, "หมู่เลือด")
        p.drawString(50, 325, "วันที่ลงทะเบียน")
    
    if not patient == None:
        p.setFont("THSarabunNew", 14, leading=None)
        p.drawString(200, 640, patient.idCard)
        p.drawString(200, 605, str(patient.title))
        p.drawString(390, 605, patient.name)
        p.drawString(200, 570, x)
        p.drawString(390, 570, str(patient.age) + " " + " ปี")
        p.drawString(200, 535, patient.gender)
        p.drawString(200, 500, patient.address)
        p.drawString(200, 465, patient.phone)
        p.drawString(200, 430, patient.email)
        if patient.underlyingDisease == None:
            p.drawString(200, 395, 'ไม่มีโรคประจำตัว')
        else:
            p.drawString(200, 395, str(patient.underlyingDisease))
        p.drawString(200, 360, patient.bloodType)
        p.drawString(200, 325, str(patient.createdAt))
    
    # กรอบนอก
    p.line(25, 680, 60, 680)
    p.line(140, 680, 570, 680)
    p.line(25, 680, 25, 120)
    p.line(570, 680, 570, 120)
    
    # กรอบอาการแพ้ยา
    p.line(25, 290, 60, 290)
    p.line(140, 290, 570, 290)
    p.line(25, 120, 570, 120)
    
    if not Allergic.objects.filter(patient_id=patient.id).values().count() == 0:
        allergic = Allergic.objects.all().filter(patient_id=patient.id).values()
        p.setFont("THSarabunNew-Bold", 14, leading=None)
        p.drawString(50, 260, 'รายการ')
        for i in range(1, len(allergic)+1): 
            p.setFont("THSarabunNew", 14, leading=None)
            if i == 1:
                p.drawString(200, 260, str(allergic[i-i]['allergicMedicineName'])) 
            else: 
                p.drawString(200, (290-(i*30)), str(allergic[i-1]['allergicMedicineName'])) 
    else: 
        p.setFont("THSarabunNew-Bold", 14, leading=None)
        p.drawString(50, 260, 'รายการ') 
        if not patient == None:
            p.setFont("THSarabunNew", 14, leading=None)
            p.drawString(200, 260, 'ไม่มีรายการแพ้') 
    
    # for k,v in data.items():
    #     p.setFont("THSarabunNew", 16, leading=None)
    #     p.drawString(177, 720, "ออกประวัติผู้ป่วยเมื่อ")
    #     p.drawString(280, 720, str(d))
    #     p.drawString(x1, y1-10, f'{k}')
        
    #     for value in v:
    #         for key, val in value.items():
    #             p.setFont("THSarabunNew", 14, leading=None)
    #             p.drawString(x1+40, y1-40, f'{key} : {val}')
    #             y1 = y1-30
            
    p.drawString(25, 90, "ผู้ออกใบระเบียนผู้ป่วย ")
    p.drawString(135, 90, str(request.user.title + request.user.first_name + ' ' + request.user.last_name))
    p.setTitle(f'Report on {d}')
    p.showPage()
    p.save()
    
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response

# real export prescription PDF
def export_patient_prescriptions(request, id):
    try:
        tz = pytz.timezone('Asia/Bangkok')
        now1 = datetime.now(tz)
        month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[now1.month]
        thai_year = now1.year + 543
        time_str = now1.strftime('%H:%M:%S')
        d = "%d %s %d %s"%(now1.day, month_name, thai_year, time_str)
        
        pres = Prescription.objects.all().filter(treatment_id=id).values()

        if len(pres) <= 0:
            messages.error(request, 'ขออภัย ผู้ป่วยท่านนี้ไม่มีใบจ่ายยา')
            return HttpResponseRedirect(reverse('Patient:show-successful-treatment', kwargs={}))
        logo = ImageReader('Patient/static/icon/logo-color.png')

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{d}.pdf"'
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        p.drawImage(logo, 120, 750, mask='auto')
        p.setFont("THSarabunNew-Bold", 18, leading=None)
        p.drawString(260, 750, "ใบสั่งจ่ายยา")
        p.drawString(30, 555, "ลำดับ")
        p.drawString(190, 555, "ชื่อยา / รายการยา")
        p.drawString(415, 555, "จำนวน")
        p.drawString(500, 555, "หน่วยยา")
                
        # for i in pres:
        #     p.drawString(20, 700*i, str(i)) 
        for i in range(1, len(pres)+1):
            p.setFont("THSarabunNew", 16, leading=None)
            if i == 1:
                med = get_object_or_404(Medicine, id=int(pres[i-i]['medicine_id']))
                unit = get_object_or_404(MedicineUnit, id=int(pres[i-i]['medicineUnit_id']))
                # p.drawString(20, 700, str(pres[i-i]['id'])) 
                p.drawString(40, 510, str(i)) 
                p.drawString(100, 510, str(med)) 
                p.drawString(422, 510, str(pres[i-i]['medicineAmount'])) 
                p.drawString(500, 510, str(unit)) 
            else: 
                med = get_object_or_404(Medicine, id=int(pres[i-1]['medicine_id']))
                unit = get_object_or_404(MedicineUnit, id=int(pres[i-1]['medicineUnit_id']))
                # p.drawString(20, (700*(i/2)-50), str(pres[i-1]))
                p.drawString(40, (535-(i*30)), str(i)) 
                p.drawString(100, (535-(i*30)), str(med))  
                p.drawString(422, (535-(i*30)), str(pres[i-1]['medicineAmount'])) 
                p.drawString(500, (535-(i*30)), str(unit)) 
        
        if not Allergic.objects.filter(patient_id=pres[0]['patient_id']).values().count() == 0:
            allergic = Allergic.objects.all().filter(patient_id=pres[0]['patient_id']).values()
            p.setFont("THSarabunNew-Bold", 12, leading=None)
            p.drawString(460, 810, '*รายการแพ้ยา*')
            for i in range(1, len(allergic)+1): 
                p.setFont("THSarabunNew", 12, leading=None)
                if i == 1:
                    p.drawString(480, 790, str(allergic[i-i]['allergicMedicineName'])) 
                else: 
                    p.drawString(480, (835-(i*30)), str(allergic[i-1]['allergicMedicineName'])) 
        else: 
            p.setFont("THSarabunNew-Bold", 12, leading=None)
            p.drawString(460, 810, '*รายการแพ้ยา*') 
            p.drawString(480, 790, 'ไม่มีรายการแพ้ยา') 
     
        treatment = TreatmentHistory.objects.get(id=id)
        patient = get_object_or_404(Patient, id=treatment.patient_id)
        dob = patient.dob
        dobSplit = dob.split("-")
        dobYear = dobSplit[0]
        dobDay = dobSplit[2]
        dobMonth = dobSplit[1]

        mo = int(dobMonth)
        month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[mo]
        thai_year = int(dobYear) + 543
        x = ("%d %s %d"%(int(dobDay), month_name, thai_year))
        
        data = {
            "": [{"เลขประจำตัวผู้ป่วย": patient.hn},
                {"ชื่อและนามสกุล": str(patient.title) + patient.name},
                {"เลขบัตรประจำตัวประชาชน": patient.idCard},
            ],
        }
        
        data1 = {
            "": [
                {"เพศ": patient.gender},
                {"อายุ": patient.age + "  " + "ปี"},
                {"วันเกิด": x},
            ],
        }
        
        x1 = 10
        y1 = 710
        
        for k,v in data.items():
            p.setFont("THSarabunNew", 16, leading=None)
            p.drawString(195, 720, "ออกใบสั่งยาเมื่อ")
            p.drawString(270, 720, str(d))
            p.drawString(x1, y1-10, f'{k}')
            
            for value in v:
                for key, val in value.items():
                    p.setFont("THSarabunNew", 14, leading=None)
                    p.drawString(x1+40, y1-40, f'{key}    {val}')
                    y1 = y1-30
        
        for k,v in data1.items():
            for value in v:
                for key, val in value.items():
                    p.setFont("THSarabunNew", 14, leading=None)
                    p.drawString(x1+380, y1+55, f'{key}    {val}')
                    y1 = y1-30

        p.line(20, 580, 580, 580)
        p.line(20, 540, 580, 540)
        p.line(20, 580, 20, 280)
        p.line(580, 580, 580, 280)
        
        p.line(70, 580, 70, 280)
        p.line(400, 580, 400, 280)
        p.line(460, 580, 460, 280)
        p.line(20, 280, 580, 280)
        
        p.drawString(20, 230, "ผู้ออกใบจ่ายยา ")
        p.drawString(110, 230, str(pres[0]['doctorName']))
        
        p.drawString(20, 200, "วันที่ออกใบจ่ายยา ")
        p.drawString(110, 200, str(d))
    
        p.setTitle(f'Report on {d}')
        p.showPage()
        p.save()
        
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        
        return response
    except:
        messages.error(request, 'ขออภัย ผู้ป่วยท่านนี้ไม่มีใบจ่ายยา')
        return HttpResponseRedirect(reverse('Patient:show-successful-treatment', kwargs={}))
 
# export prescription in patient present data page
def export_patient_prescriptions_present(request, id):
    try:
        tz = pytz.timezone('Asia/Bangkok')
        now1 = datetime.now(tz)
        month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[now1.month]
        thai_year = now1.year + 543
        time_str = now1.strftime('%H:%M:%S')
        d = "%d %s %d %s"%(now1.day, month_name, thai_year, time_str)
        
        pres = Prescription.objects.all().filter(treatment_id=id).values()
        
        if len(pres) <= 0:
            messages.error(request, 'ขออภัย ผู้ป่วยท่านนี้ไม่มีใบจ่ายยา')
            return HttpResponseRedirect(reverse('Patient:patient-present-data', kwargs={}))
        
        logo = ImageReader('Patient/static/icon/logo-color.png')

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="prescriptions.pdf"'
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        p.drawImage(logo, 120, 750, mask='auto')
        p.setFont("THSarabunNew-Bold", 18, leading=None)
        p.drawString(260, 750, "ใบสั่งจ่ายยา")
        p.drawString(30, 555, "ลำดับ")
        p.drawString(190, 555, "ชื่อยา / รายการยา")
        p.drawString(415, 555, "จำนวน")
        p.drawString(500, 555, "หน่วยยา")
                
        # for i in pres:
        #     p.drawString(20, 700*i, str(i)) 
        for i in range(1, len(pres)+1):
            p.setFont("THSarabunNew", 16, leading=None)
            if i == 1:
                med = get_object_or_404(Medicine, id=int(pres[i-i]['medicine_id']))
                unit = get_object_or_404(MedicineUnit, id=int(pres[i-i]['medicineUnit_id']))
                # p.drawString(20, 700, str(pres[i-i]['id'])) 
                p.drawString(40, 510, str(i)) 
                p.drawString(100, 510, str(med)) 
                p.drawString(422, 510, str(pres[i-i]['medicineAmount'])) 
                p.drawString(500, 510, str(unit)) 
            else: 
                med = get_object_or_404(Medicine, id=int(pres[i-1]['medicine_id']))
                unit = get_object_or_404(MedicineUnit, id=int(pres[i-1]['medicineUnit_id']))
                # p.drawString(20, (700*(i/2)-50), str(pres[i-1]))
                p.drawString(40, (535-(i*30)), str(i)) 
                p.drawString(100, (535-(i*30)), str(med))  
                p.drawString(422, (535-(i*30)), str(pres[i-1]['medicineAmount'])) 
                p.drawString(500, (535-(i*30)), str(unit)) 
                
        if not Allergic.objects.filter(patient_id=pres[0]['patient_id']).values().count() == 0:
            allergic = Allergic.objects.all().filter(patient_id=pres[0]['patient_id']).values()
            p.setFont("THSarabunNew-Bold", 12, leading=None)
            p.drawString(460, 810, '*รายการแพ้ยา*')
            for i in range(1, len(allergic)+1): 
                p.setFont("THSarabunNew", 12, leading=None)
                if i == 1:
                    p.drawString(480, 790, str(allergic[i-i]['allergicMedicineName'])) 
                else: 
                    p.drawString(480, (835-(i*30)), str(allergic[i-1]['allergicMedicineName'])) 
        else: 
            p.setFont("THSarabunNew-Bold", 12, leading=None)
            p.drawString(460, 810, '*รายการแพ้ยา*') 
            p.drawString(480, 790, 'ไม่มีรายการแพ้ยา') 
                
        treatment = TreatmentHistory.objects.get(id=id)
        patient = get_object_or_404(Patient, id=treatment.patient_id)
        dob = patient.dob
        dobSplit = dob.split("-")
        dobYear = dobSplit[0]
        dobDay = dobSplit[2]
        dobMonth = dobSplit[1]

        mo = int(dobMonth)
        month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[mo]
        thai_year = int(dobYear) + 543
        x = ("%d %s %d"%(int(dobDay), month_name, thai_year))
        
        data = {
            "": [{"เลขประจำตัวผู้ป่วย": patient.hn},
                {"ชื่อและนามสกุล": str(patient.title) + patient.name},
                {"เลขบัตรประจำตัวประชาชน": patient.idCard},
            ],
        }
        
        data1 = {
            "": [
                {"เพศ": patient.gender},
                {"อายุ": patient.age + "  " + "ปี"},
                {"วันเกิด": x},
            ],
        }
        
        x1 = 10
        y1 = 710
        
        for k,v in data.items():
            p.setFont("THSarabunNew", 16, leading=None)
            p.drawString(195, 720, "ออกใบสั่งยาเมื่อ")
            p.drawString(270, 720, str(d))
            p.drawString(x1, y1-10, f'{k}')
            
            for value in v:
                for key, val in value.items():
                    p.setFont("THSarabunNew", 14, leading=None)
                    p.drawString(x1+40, y1-40, f'{key}    {val}')
                    y1 = y1-30
        
        for k,v in data1.items():
            for value in v:
                for key, val in value.items():
                    p.setFont("THSarabunNew", 14, leading=None)
                    p.drawString(x1+380, y1+55, f'{key}    {val}')
                    y1 = y1-30

        p.line(20, 580, 580, 580)
        p.line(20, 540, 580, 540)
        p.line(20, 580, 20, 280)
        p.line(580, 580, 580, 280)
        
        p.line(70, 580, 70, 280)
        p.line(400, 580, 400, 280)
        p.line(460, 580, 460, 280)
        p.line(20, 280, 580, 280)
        
        p.drawString(20, 230, "ผู้ออกใบจ่ายยา ")
        p.drawString(110, 230, str(pres[0]['doctorName']))
        
        p.drawString(20, 200, "วันที่ออกใบจ่ายยา ")
        p.drawString(110, 200, str(d))
    
        p.setTitle(f'Report on {d}')
        p.showPage()
        p.save()
        
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        
        return response
    except:
        messages.error(request, 'ขออภัย ผู้ป่วยท่านนี้ไม่มีใบจ่ายยา')
        return HttpResponseRedirect(reverse('Patient:patient-present-data', kwargs={}))

# export prescription in patient treatment history page
def export_patient_prescriptions_treatment(request, id):
    try:
        tz = pytz.timezone('Asia/Bangkok')
        now1 = datetime.now(tz)
        month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[now1.month]
        thai_year = now1.year + 543
        time_str = now1.strftime('%H:%M:%S')
        d = "%d %s %d %s"%(now1.day, month_name, thai_year, time_str)
        
        pres = Prescription.objects.all().filter(treatment_id=id).values()
        
        if len(pres) <= 0:
            messages.error(request, 'ขออภัย ผู้ป่วยท่านนี้ไม่มีใบจ่ายยา')
            return HttpResponseRedirect(reverse('Patient:patient-present-data', kwargs={}))
        
        logo = ImageReader('Patient/static/icon/logo-color.png')

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="prescriptions.pdf"'
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        p.drawImage(logo, 120, 750, mask='auto')
        p.setFont("THSarabunNew-Bold", 18, leading=None)
        p.drawString(260, 750, "ใบสั่งจ่ายยา")
        p.drawString(30, 555, "ลำดับ")
        p.drawString(190, 555, "ชื่อยา / รายการยา")
        p.drawString(415, 555, "จำนวน")
        p.drawString(500, 555, "หน่วยยา")
                
        # for i in pres:
        #     p.drawString(20, 700*i, str(i)) 
        for i in range(1, len(pres)+1):
            p.setFont("THSarabunNew", 16, leading=None)
            if i == 1:
                med = get_object_or_404(Medicine, id=int(pres[i-i]['medicine_id']))
                unit = get_object_or_404(MedicineUnit, id=int(pres[i-i]['medicineUnit_id']))
                # p.drawString(20, 700, str(pres[i-i]['id'])) 
                p.drawString(40, 510, str(i)) 
                p.drawString(100, 510, str(med)) 
                p.drawString(422, 510, str(pres[i-i]['medicineAmount'])) 
                p.drawString(500, 510, str(unit)) 
            else: 
                med = get_object_or_404(Medicine, id=int(pres[i-1]['medicine_id']))
                unit = get_object_or_404(MedicineUnit, id=int(pres[i-1]['medicineUnit_id']))
                # p.drawString(20, (700*(i/2)-50), str(pres[i-1]))
                p.drawString(40, (535-(i*30)), str(i)) 
                p.drawString(100, (535-(i*30)), str(med))  
                p.drawString(422, (535-(i*30)), str(pres[i-1]['medicineAmount'])) 
                p.drawString(500, (535-(i*30)), str(unit)) 
                
        if not Allergic.objects.filter(patient_id=pres[0]['patient_id']).values().count() == 0:
            allergic = Allergic.objects.all().filter(patient_id=pres[0]['patient_id']).values()
            p.setFont("THSarabunNew-Bold", 12, leading=None)
            p.drawString(460, 810, '*รายการแพ้ยา*')
            for i in range(1, len(allergic)+1): 
                p.setFont("THSarabunNew", 12, leading=None)
                if i == 1:
                    p.drawString(480, 790, str(allergic[i-i]['allergicMedicineName'])) 
                else: 
                    p.drawString(480, (835-(i*30)), str(allergic[i-1]['allergicMedicineName'])) 
        else: 
            p.setFont("THSarabunNew-Bold", 12, leading=None)
            p.drawString(460, 810, '*รายการแพ้ยา*') 
            p.drawString(480, 790, 'ไม่มีรายการแพ้ยา') 
                
        treatment = TreatmentHistory.objects.get(id=id)
        patient = get_object_or_404(Patient, id=treatment.patient_id)
        dob = patient.dob
        dobSplit = dob.split("-")
        dobYear = dobSplit[0]
        dobDay = dobSplit[2]
        dobMonth = dobSplit[1]

        mo = int(dobMonth)
        month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[mo]
        thai_year = int(dobYear) + 543
        x = ("%d %s %d"%(int(dobDay), month_name, thai_year))
        
        data = {
            "": [{"เลขประจำตัวผู้ป่วย": patient.hn},
                {"ชื่อและนามสกุล": str(patient.title) + patient.name},
                {"เลขบัตรประจำตัวประชาชน": patient.idCard},
            ],
        }
        
        data1 = {
            "": [
                {"เพศ": patient.gender},
                {"อายุ": patient.age + "  " + "ปี"},
                {"วันเกิด": x},
            ],
        }
        
        x1 = 10
        y1 = 710
        
        for k,v in data.items():
            p.setFont("THSarabunNew", 16, leading=None)
            p.drawString(195, 720, "ออกใบสั่งยาเมื่อ")
            p.drawString(270, 720, str(d))
            p.drawString(x1, y1-10, f'{k}')
            
            for value in v:
                for key, val in value.items():
                    p.setFont("THSarabunNew", 14, leading=None)
                    p.drawString(x1+40, y1-40, f'{key}    {val}')
                    y1 = y1-30
        
        for k,v in data1.items():
            for value in v:
                for key, val in value.items():
                    p.setFont("THSarabunNew", 14, leading=None)
                    p.drawString(x1+380, y1+55, f'{key}    {val}')
                    y1 = y1-30

        p.line(20, 580, 580, 580)
        p.line(20, 540, 580, 540)
        p.line(20, 580, 20, 280)
        p.line(580, 580, 580, 280)
        
        p.line(70, 580, 70, 280)
        p.line(400, 580, 400, 280)
        p.line(460, 580, 460, 280)
        p.line(20, 280, 580, 280)
        
        p.drawString(20, 230, "ผู้ออกใบจ่ายยา ")
        p.drawString(110, 230, str(pres[0]['doctorName']))
        
        p.drawString(20, 200, "วันที่ออกใบจ่ายยา ")
        p.drawString(110, 200, str(d))
    
        p.setTitle(f'Report on {d}')
        p.showPage()
        p.save()
        
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        
        return response
    except:
        messages.error(request, 'ขออภัย ผู้ป่วยท่านนี้ไม่มีใบจ่ายยา')
        return HttpResponseRedirect(request.headers.get("referer"))
    
# real export patient appointment PDF
def export_patient_appointment(request, id):
    try:
        tz = pytz.timezone('Asia/Bangkok')
        now1 = datetime.now(tz)
        month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[now1.month]
        thai_year = now1.year + 543
        time_str = now1.strftime('%H:%M:%S')
        d = "%d %s %d %s"%(now1.day, month_name, thai_year, time_str)
        
        treatment = TreatmentHistory.objects.get(id=id)
        patient = Patient.objects.get(id=treatment.patient_id)
        app = EventAppointment.objects.filter(patient_id=patient.id).latest('createdAt')
        logo = ImageReader('Patient/static/icon/logo-color.png')

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{d}.pdf"'
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        dob = patient.dob
        dobSplit = dob.split("-")
        dobYear = dobSplit[0]
        dobDay = dobSplit[2]
        dobMonth = dobSplit[1]

        mo = int(dobMonth)
        month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[mo]
        thai_year = int(dobYear) + 543
        x = ("%d %s %d"%(int(dobDay), month_name, thai_year))
        
        data = {
            "": [{"เลขประจำตัวผู้ป่วย": patient.hn},
                {"ชื่อและนามสกุล": str(patient.title) + patient.name},
                {"อายุ": patient.age + "  " + "ปี"},
                {"วันเกิด": x},
                {"เบอร์โทรศัพท์": patient.phone},
            ],
        }
        
        appDate = str(app.date)
        appDateSplit = appDate.split("-")
        appDateYear = appDateSplit[0]
        appDateMonth = appDateSplit[1]
        appDateDay = appDateSplit[2]
        
        appMonth = int(appDateMonth)
        month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[appMonth]
        thai_year = int(appDateYear) + 543
        appointmentDate = ("%d %s %d"%(int(appDateDay), month_name, thai_year))
        
        app_data = {
            "ข้อมูลการนัด" : [{"วันที่นัด": str(appointmentDate)},
                {"แพทย์": app.doctorName},
                {"สาเหตุการนัดหมาย": app.name},
                {"หมายเหตุ / ข้อควรปฏิบัติ": app.description},
                ],
        }
        
        remark = {
            "หมายเหตุ / remarks": [
                {"": "- หากท่านมีอาการผิดปกติก่อนวันนัด กรุณามาพบแพทย์ได้ทันที"},
                {"": "- กรุณามาตรงตามเวลานัด หากไม่ตรงเวลา ต้องรอตามเวลานัดหรือนัดใหม่"},
                {"": "- กรุณาติดต่อที่แผนกเวชระเบียน ก่อนเวลานัด 30 นาที"},
                {"": "- หากท่านมีอาการผิดปกติก่อนวันนัด กรุณามาพบแพทย์ได้ทันที"},
            ]
        }
    
        p.drawImage(logo, 120, 750, mask='auto')
        p.setFont("THSarabunNew-Bold", 18, leading=None)
        p.drawString(250, 750, "บัตรนัดหมายผู้ป่วย")

        x1 = 340
        y1 = 720
        
        for k,v in data.items():
            p.setFont("THSarabunNew", 14, leading=None)
            p.drawString(490, 800, "*" + patient.idCard + "*")
            p.drawString(120, 730, "(กรุณามาก่อนเวลานัด 30 นาที : Please contact us 30 minutes before the appointment.)")
            p.drawString(x1, y1-10, f'{k}')
            
            for value in v:
                for key, val in value.items():
                    p.setFont("THSarabunNew", 14, leading=None)
                    p.drawString(x1+40, y1-40, f'{key}  {val}')
                    y1 = y1-20
        
        for k,v in app_data.items():
            p.setFont("THSarabunNew-Bold", 14, leading=None)
            p.drawString(x1-285, y1+60, f'{k}')
            
            for value in v:
                for key, val in value.items():
                    p.setFont("THSarabunNew", 14, leading=None)
                    p.drawString(x1-265, y1+30, f'{key} {val}')
                    y1 = y1-30
                    
        for k,v in remark.items():
            p.setFont("THSarabunNew-Bold", 14, leading=None)
            p.drawString(x1-285, y1-30, f'{k}')
            
            for value in v:
                for key, val in value.items():
                    p.setFont("THSarabunNew", 14, leading=None)
                    p.drawString(x1-265, y1-60, f'{key}  {val}')
                    y1 = y1-20
        
        p.drawString(360, 250, "ผู้ออกบัตรนัด ")
        p.drawString(440, 250, str(app.doctorName))
        
        p.drawString(360, 225, "วันที่ออกบัตรนัด ")
        p.drawString(440, 225, str(d))
                
        p.setTitle(f'Report on {d}')
        p.showPage()
        p.save()
        
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        
        return response
    except:
        messages.error(request, 'ขออภัย ผู้ป่วยท่านนี้ไม่มีการนัดหมาย')
        return HttpResponseRedirect(reverse('Patient:show-successful-treatment', kwargs={}))
    
# real export patient appointment PDF
def export_patient_appointment_treatment(request, id):
    try:
        tz = pytz.timezone('Asia/Bangkok')
        now1 = datetime.now(tz)
        month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[now1.month]
        thai_year = now1.year + 543
        time_str = now1.strftime('%H:%M:%S')
        d = "%d %s %d %s"%(now1.day, month_name, thai_year, time_str)
        
        treatment = TreatmentHistory.objects.get(id=id)
        patient = Patient.objects.get(id=treatment.patient_id)
        app = EventAppointment.objects.filter(patient_id=patient.id).latest('createdAt')
        logo = ImageReader('Patient/static/icon/logo-color.png')

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{d}.pdf"'
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        dob = patient.dob
        dobSplit = dob.split("-")
        dobYear = dobSplit[0]
        dobDay = dobSplit[2]
        dobMonth = dobSplit[1]

        mo = int(dobMonth)
        month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[mo]
        thai_year = int(dobYear) + 543
        x = ("%d %s %d"%(int(dobDay), month_name, thai_year))
        
        data = {
            "": [{"เลขประจำตัวผู้ป่วย": patient.hn},
                {"ชื่อและนามสกุล": str(patient.title) + patient.name},
                {"อายุ": patient.age + "  " + "ปี"},
                {"วันเกิด": x},
                {"เบอร์โทรศัพท์": patient.phone},
            ],
        }
        
        appDate = str(app.date)
        appDateSplit = appDate.split("-")
        appDateYear = appDateSplit[0]
        appDateMonth = appDateSplit[1]
        appDateDay = appDateSplit[2]
        
        appMonth = int(appDateMonth)
        month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[appMonth]
        thai_year = int(appDateYear) + 543
        appointmentDate = ("%d %s %d"%(int(appDateDay), month_name, thai_year))
        
        app_data = {
            "ข้อมูลการนัด" : [{"วันที่นัด": str(appointmentDate)},
                {"แพทย์": app.doctorName},
                {"สาเหตุการนัดหมาย": app.name},
                {"หมายเหตุ / ข้อควรปฏิบัติ": app.description},
                ],
        }
        
        remark = {
            "หมายเหตุ / remarks": [
                {"": "- หากท่านมีอาการผิดปกติก่อนวันนัด กรุณามาพบแพทย์ได้ทันที"},
                {"": "- กรุณามาตรงตามเวลานัด หากไม่ตรงเวลา ต้องรอตามเวลานัดหรือนัดใหม่"},
                {"": "- กรุณาติดต่อที่แผนกเวชระเบียน ก่อนเวลานัด 30 นาที"},
                {"": "- หากท่านมีอาการผิดปกติก่อนวันนัด กรุณามาพบแพทย์ได้ทันที"},
            ]
        }
    
        p.drawImage(logo, 120, 750, mask='auto')
        p.setFont("THSarabunNew-Bold", 18, leading=None)
        p.drawString(250, 750, "บัตรนัดหมายผู้ป่วย")

        x1 = 340
        y1 = 720
        
        for k,v in data.items():
            p.setFont("THSarabunNew", 14, leading=None)
            p.drawString(490, 800, "*" + patient.idCard + "*")
            p.drawString(120, 730, "(กรุณามาก่อนเวลานัด 30 นาที : Please contact us 30 minutes before the appointment.)")
            p.drawString(x1, y1-10, f'{k}')
            
            for value in v:
                for key, val in value.items():
                    p.setFont("THSarabunNew", 14, leading=None)
                    p.drawString(x1+40, y1-40, f'{key}  {val}')
                    y1 = y1-20
        
        for k,v in app_data.items():
            p.setFont("THSarabunNew-Bold", 14, leading=None)
            p.drawString(x1-285, y1+60, f'{k}')
            
            for value in v:
                for key, val in value.items():
                    p.setFont("THSarabunNew", 14, leading=None)
                    p.drawString(x1-265, y1+30, f'{key} {val}')
                    y1 = y1-30
                    
        for k,v in remark.items():
            p.setFont("THSarabunNew-Bold", 14, leading=None)
            p.drawString(x1-285, y1-30, f'{k}')
            
            for value in v:
                for key, val in value.items():
                    p.setFont("THSarabunNew", 14, leading=None)
                    p.drawString(x1-265, y1-60, f'{key}  {val}')
                    y1 = y1-20
        
        p.drawString(360, 250, "ผู้ออกบัตรนัด ")
        p.drawString(440, 250, str(app.doctorName))
        
        p.drawString(360, 225, "วันที่ออกบัตรนัด ")
        p.drawString(440, 225, str(d))
                
        p.setTitle(f'Report on {d}')
        p.showPage()
        p.save()
        
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        
        return response
    except:
        messages.error(request, 'ขออภัย ไม่มีการนัดหมายในการรักษาครั้งนี้')
        return HttpResponseRedirect(request.headers.get("referer"))
        # return HttpResponseRedirect(reverse('Patient:show-patient-treatment-history', kwargs={}))

def patient_render_pdf_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    patient = get_object_or_404(Patient, pk=pk)

    template_path = 'patient/patient-data.html'
    context = {
        'patient': mark_safe(patient),
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="patient-data.pdf"'
    response.write(u'\ufeff'.encode('utf8'))
    
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, response)
    
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response

def render_pdf_view(request):
    template_path = 'patient/patient-data.html'
    context = {
        'patient': 'this is your patient pdf detail'
    }
    response = HttpResponse(content_type='application/pdf')
    
    #download
    # response['Content-Disposition'] = 'attachment; filename="patient-data.pdf"'
    
    #display
    response['Content-Disposition'] = 'filename="patient-data.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    #create a pdf file
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response

@login_required(login_url='ClinicManagement:login')  
def export_csv_patient(request):
    patient = Patient.objects.all()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="patient-data-list.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    
    writer = csv.writer(response)
    writer.writerow(['เลขประจำตัวผู้ป่วย', 'คำนำหน้าชื่อ', 'ชื่อและนามสกุล', 'เพศ', 'วันเกิด', 'อายุ', 
                    'เบอร์โทรศัพท์มือถือ', 'เลขบัตรประจำตัวประชาชน', 'ที่อยู่อาศัย', 'อีเมล์', 'โรคประจำตัว', 'หมู่เลือด',
                    'ลงทะเบียนผู้ป่วยเมื่อ', 'วันที่มีการแก้ไขล่าสุด'])

    for patient in patient:
        writer.writerow([patient.hn, str(patient.title), patient.name, patient.gender, 
                str(patient.dob), patient.age, patient.phone, patient.idCard, 
                patient.address, patient.email, patient.underlyingDisease, patient.bloodType, 
                patient.createdAt, patient.updatedAt])
        
    return response

@login_required(login_url='ClinicManagement:login')  
def generate_pdf(request, id):
    patient = get_object_or_404(Patient, id=id) 
    
    response = HttpResponse(content_type = 'application/pdf')
    d = date.today()
    response['Content-Disposition'] = f'inline; filename="{d}.pdf"'
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont('F1', 15, leading=None)
    
    p.line(20, 710, 580, 710)
    p.line(20, 480, 580, 480)
    p.line(20, 710, 20, 480)
    p.line(580, 710, 580, 480)
    
    p.drawString(270, 780, "ข้อมูลผู้ป่วย")
    p.drawString(130, 750, "(กรุณามาก่อนเวลานัด 30 นาที : Please contact us 30 minutes before the appointment.)")

    p.drawString(50, 670, "ข้อมูลเบื้องต้น")
    p.drawString(390, 630, "HN (Hospital Number) :")
    p.drawString(500, 630, patient.hn)
    
    p.drawString(50, 630, "ชื่อ-นามสกุล (Name and Surname) :")
    p.drawString(200, 630, str(patient.title) + patient.name)
    
    p.drawString(50, 600, "อายุ (Age) :")
    p.drawString(110, 600, patient.age + "      ปี")
    
    p.drawString(280, 600, "วันเดือนปีเกิด (Date of Birth) :")
    p.drawString(450, 600, patient.dob)
    
    p.drawString(50, 570, "เลขบัตรประจำตัวประชาชน (Personal id card number) :")
    p.drawString(300, 570, patient.idCard)
    
    p.drawString(50, 540, "ที่อยู่ (Address) :")
    p.drawString(150, 540, patient.address)
    
    p.drawString(50, 510, "เบอร์โทรศัพท์มือถือ (Phone Number) :")
    p.drawString(230, 510, patient.phone)
    
    p.drawString(50, 440, "ข้อมูลประวัติการแพ้ยา")
    
    try:
        allergic = Allergic.objects.get(patient_id=id)
        p.drawString(100, 410, "ชื่อยาที่แพ้ :")
        p.drawString(150, 410, allergic.allergicMedicineName)
        
        p.drawString(300, 410, "อาการที่แพ้ :")
        p.drawString(360, 410, allergic.allergicSymptom)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        pass
    
    p.drawString(370, 150, "ผู้ออกบัตรนัด :")
    p.drawString(440, 150, str(request.user.title + request.user.first_name + " " + request.user.last_name))
    
    p.drawString(370, 120, "วันที่ออกบัตรนัด :")
    p.drawString(450, 120, str(d))
    
    p.setTitle(f'Report on {d}')
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

@login_required(login_url='ClinicManagement:login')   
def export_appointment(request, id):
     
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont('F1', 15, leading=None)
    d = date.today()
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = f'inline; filename="{d}.pdf"'
    
    try:
        app = EventAppointment.objects.filter(patient_id=id).latest('createdAt')
        patient = Patient.objects.get(id=id)
        
        p.drawString(260, 780, "บัตรนัดหมายผู้ป่วย")
        p.drawString(130, 750, "(กรุณามาก่อนเวลานัด 30 นาที : Please contact us 30 minutes before the appointment.)")
        
        p.drawString(50, 700, "ชื่อ-นามสกุล (Name and Surname) :")
        p.drawString(200, 700, str(app.patientTitle) + app.patientName)
        
        p.drawString(390, 700, "HN (Hospital Number) :")
        p.drawString(500, 700, patient.hn)
        
        p.drawString(50, 655, "วันที่นัด (Date) :")
        p.drawString(130, 655, str(app.date.day))
        
        p.drawString(150, 655, "เดือน")
        p.drawString(180, 655, str(app.date.month))
        
        p.drawString(200, 655, "ปี ค.ศ.")
        p.drawString(230, 655, str(app.date.year))
        p.drawString(340, 655, "เบอร์ติดต่อ (Phone Number) : 093 390 6787")
        
        p.drawString(50, 620, "พบแพทย์ (Appointment Doctor) :")
        p.drawString(200, 620, str(app.doctorName))
        
        p.drawString(50, 570, "นัดมาเพื่อ (Appointment To) :")
        p.drawString(190, 570, app.name)
        
        p.drawString(50, 540, "ข้อปฏิบัติก่อนเข้าพบแพทย์ (Preparation) :")
        p.drawString(240, 540, app.description)
        
        p.drawString(50, 400, "หมายเหตุ (Remark) :")
        p.drawString(80, 370, "- หากท่านมีอาการผิดปกติก่อนวันนัด กรุณามาพบแพทย์ได้ทันที")
        p.drawString(80, 340, "- กรุณามาตรงตามเวลานัด หากไม่ตรงเวลา ต้องรอตามเวลานัดหรือนัดใหม่")
        p.drawString(80, 310, "- กรุณาติดต่อที่แผนกเวชระเบียน ก่อนเวลานัด 30 นาที")
        p.drawString(80, 280, "- กรณีต้องตรวจ แล็ป หรือเอ็กซเรย์ให้มาก่อนเวลานัด")
        
        p.drawString(370, 150, "ผู้ออกบัตรนัด :")
        p.drawString(440, 150, str(app.doctorName))
        
        p.drawString(370, 120, "วันที่ออกบัตรนัด :")
        p.drawString(450, 120, str(d))

        p.line(20, 680, 580, 680)
        p.line(20, 600, 580, 600)
        p.line(20, 680, 20, 600)
        p.line(580, 680, 580, 600)
    
        p.setTitle(f'Report on {d}')
        
    except:
        pass
        
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

@login_required(login_url='ClinicManagement:login')   
def show_prescription(request, id):
    print('xxxxxx')
    pres = Prescription.objects.filter(treatment_id=id)
    print('xxxxxx1')
    return render(request, "../templates/patient/successful-treatment.html", {'pres': pres})

# new appointment here
@login_required(login_url='ClinicManagement:login')   
def export_appointment_treatment(request, id):
     
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont('F1', 15, leading=None)
    d = date.today()
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = f'inline; filename="{d}.pdf"'
    
    try:
        treatment = TreatmentHistory.objects.get(id=id)
        patient = Patient.objects.get(id=treatment.patient_id)
        app = EventAppointment.objects.filter(patient_id=patient.id).latest('createdAt')
        
        p.drawString(260, 780, "บัตรนัดหมายผู้ป่วย")
        p.drawString(130, 750, "(กรุณามาก่อนเวลานัด 30 นาที : Please contact us 30 minutes before the appointment.)")
        
        p.drawString(50, 700, "ชื่อ-นามสกุล (Name and Surname) :")
        p.drawString(200, 700, str(app.patientTitle) + app.patientName)
        
        p.drawString(390, 700, "HN (Hospital Number) :")
        p.drawString(500, 700, patient.hn)
        
        p.drawString(50, 655, "วันที่นัด (Date) :")
        p.drawString(130, 655, str(app.date.day))
        
        p.drawString(150, 655, "เดือน")
        p.drawString(180, 655, str(app.date.month))
        
        p.drawString(200, 655, "ปี ค.ศ.")
        p.drawString(230, 655, str(app.date.year))
        p.drawString(340, 655, "เบอร์ติดต่อ (Phone Number) : 093 390 6787")
        
        p.drawString(50, 620, "พบแพทย์ (Appointment Doctor) :")
        p.drawString(200, 620, str(app.doctorName))
        
        p.drawString(50, 570, "นัดมาเพื่อ (Appointment To) :")
        p.drawString(190, 570, app.name)
        
        p.drawString(50, 540, "ข้อปฏิบัติก่อนเข้าพบแพทย์ (Preparation) :")
        p.drawString(240, 540, app.description)
        
        p.drawString(50, 400, "หมายเหตุ (Remark) :")
        p.drawString(80, 370, "- หากท่านมีอาการผิดปกติก่อนวันนัด กรุณามาพบแพทย์ได้ทันที")
        p.drawString(80, 340, "- กรุณามาตรงตามเวลานัด หากไม่ตรงเวลา ต้องรอตามเวลานัดหรือนัดใหม่")
        p.drawString(80, 310, "- กรุณาติดต่อที่แผนกเวชระเบียน ก่อนเวลานัด 30 นาที")
        p.drawString(80, 280, "- กรณีต้องตรวจ แล็ป หรือเอ็กซเรย์ให้มาก่อนเวลานัด")
        
        p.drawString(370, 150, "ผู้ออกบัตรนัด :")
        p.drawString(440, 150, str(app.doctorName))
        
        p.drawString(370, 120, "วันที่ออกบัตรนัด :")
        p.drawString(450, 120, str(d))

        p.line(20, 680, 580, 680)
        p.line(20, 600, 580, 600)
        p.line(20, 680, 20, 600)
        p.line(580, 680, 580, 600)
    
        p.setTitle(f'Report on {d}')
        
    except:
        p.setTitle(f'Report on {d}')
        pass
        # p.drawString(260, 780, "ไม่มีรายการนัด")
        # p.setTitle(f'Report on {d}')
        
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

@login_required(login_url='ClinicManagement:login')   
def patient_list(request):
    patient = Patient.objects.all().order_by('-createdAt')
    form = InitialSymptomsForm()
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    
    page = request.GET.get('page', 1)
    paginator = Paginator(patient, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = patient.count()
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return render(request, '../templates/patient/patient-list.html', {
        'page_obj': page_obj,
        'count': count,
        'form': form,
        'empty': empty,
    })

@login_required(login_url='ClinicManagement:login')    
def patient_medicine(request, id):
    form = AppointmentForm()
    patient = get_object_or_404(Patient, id=id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.patient_id = patient.id
            app.patientName = patient.name
            app.patientTitle = patient.title
            app.save()
            form.save_m2m()
            messages.success(request, 'บันทึกอาการแพ้สำเร็จ')
            return HttpResponseRedirect(reverse('Patient:patient-present-data', kwargs={}))
    return render(request, '../templates/patient/patient-present.html')
    
@login_required(login_url='ClinicManagement:login')    
def add_patient_allergic_history(request, id):
    patient = Patient.objects.get(id=id)
    form = AllergicHistoryForm()
    if request.method == 'POST':
        form = AllergicHistoryForm(request.POST, request.FILES)
        if form.is_valid():
            allergic = form.save(commit=False)
            allergic.patient_id = patient.id
            allergic.patientName = patient.name
            allergic.patientTitle = patient.title
            allergic.allergicMedicineName = request.POST['allergicMedicineName']
            allergic.allergicSymptom = request.POST['allergicSymptom']
            allergic.sequence = 1
            allergic.save()
            form.save_m2m()
            messages.success(request, 'บันทึกอาการแพ้สำเร็จ')
            return HttpResponseRedirect(reverse('Patient:patient-present-data', kwargs={}))
    return render(request, '../templates/patient/patient-present.html')

@login_required(login_url='ClinicManagement:login')    
@user_passes_test(check_nurse, login_url='ClinicManagement:error-page') 
def add_patient_queue(request, id):
    patient = get_object_or_404(Patient, id=id) 
    
    form = PatientQueueForm()
    if request.method == 'POST':
        form = PatientQueueForm(request.POST, request.FILES)
        if form.is_valid():
            try: 
                q = get_object_or_404(PatientQueue, patient_id=id) 
                q.delete()
                queue = form.save(commit=False)
                queue.patient_id = patient.id
                queue.patientTitle = patient.title
                queue.patientName = patient.name
                queue.status = 'รอเข้าพบแพทย์'
                queue.save()
                messages.success(request, 'เพิ่มคนไข้เข้าคิวสำเร็จ')
            except:
                queue = form.save(commit=False)
                queue.patient_id = patient.id
                queue.patientTitle = patient.title
                queue.patientName = patient.name
                queue.status = 'รอเข้าพบแพทย์'
                queue.save()
                form.save_m2m()
                messages.success(request, 'เพิ่มคนไข้เข้าคิวสำเร็จ')
            return HttpResponseRedirect(reverse('Patient:patient-list', kwargs={}))
    return render(request, '../templates/patient/patient-queue.html')

# @login_required(login_url='ClinicManagement:login')    
# def add_patient_queue(request, id):
#     patient = get_object_or_404(Patient, id=id) 
    
#     form = PatientQueueForm()
#     if request.method == 'POST':
#         form = PatientQueueForm(request.POST, request.FILES)
#         if form.is_valid():
#             try: 
#                 q = get_object_or_404(PatientQueue, patient_id=id) 
#                 q.delete()
#                 queue = form.save(commit=False)
#                 queue.patient_id = patient.id
#                 queue.patientTitle = patient.title
#                 queue.patientName = patient.name
#                 queue.save()
#                 messages.success(request, 'เพิ่มคนไข้เข้าคิวสำเร็จ')
#             except:
#                 queue = form.save(commit=False)
#                 queue.patient_id = patient.id
#                 queue.patientTitle = patient.title
#                 queue.patientName = patient.name
#                 queue.save()
#                 form.save_m2m()
#                 messages.success(request, 'เพิ่มคนไข้เข้าคิวสำเร็จ')
#             return HttpResponseRedirect(reverse('Patient:patient-list', kwargs={}))
#     return render(request, '../templates/patient/patient-queue.html')

@login_required(login_url='ClinicManagement:login')
def patient_queue_list(request):
    today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
    today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)

    queue = PatientQueue.objects.filter(createdAt__range=(today_min, today_max)) and (PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์') | PatientQueue.objects.filter(status='รอเข้าพบแพทย์'))
    waiting = PatientQueue.objects.filter(createdAt__range=(today_min, today_max), status='รอเข้าพบแพทย์').count()
    treatment = TreatmentHistory.objects.filter(createdAt__range=(today_min, today_max), number=None).count()
    treatment1 = TreatmentHistory.objects.filter(createdAt__range=(today_min, today_max), number=1).count()
    
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'

    page = request.GET.get('page', 1)
    paginator = Paginator(queue, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = queue.count()
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    context = {
        'page_obj': page_obj,
        'count': count,
        'waiting': waiting,
        'treatment': treatment,
        'treatment1': treatment1,
        'empty': empty,
    }
    
    return render(request, '../templates/patient/patient-queue.html', context)

@login_required(login_url='ClinicManagement:login')    
@user_passes_test(check_nurse, login_url='ClinicManagement:error-page')   
def patient_delete_queue(request, id):
    data = get_object_or_404(PatientQueue, id=id) 
    data.delete()
    messages.success(request, 'ลบคิวสำเร็จ')
    return HttpResponseRedirect(reverse('Patient:patient-queue-list', kwargs={}))

@login_required(login_url='ClinicManagement:login')    
@user_passes_test(check_nurse, login_url='ClinicManagement:error-page') 
def add_present_patient(request, id):
    try:
        if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
            messages.error(request, 'ขออภัย ขณะนี้มีผู้ป่วยกำลังเข้ารับการรักษา')
            return HttpResponseRedirect(reverse('Patient:patient-queue-list', kwargs={}))
        else:
            patient = get_object_or_404(Patient, id=id) 
            form = TreatmentHistoryForm()
            if request.method == 'POST':
                form = TreatmentHistoryForm(request.POST, request.FILES)
                if form.is_valid():
                    treatment = form.save(commit=False)
                    treatment.patient_id = patient.id
                    treatment.patientTitle = patient.title
                    treatment.patientName = patient.name
                    treatment.number = 1 
                    treatment.save()
                    form.save_m2m()

                    queue = PatientQueue.objects.filter(patient_id=id).latest('createdAt')
                    q = PatientQueueForm(request.POST or None, instance = queue)
                    q1 = q.save(commit=False) 
                    q1.status = 'กำลังเข้าพบแพทย์'
                    q1.save()
                    # queue.delete()
                    messages.success(request, 'เพิ่มคนไข้เข้าตรวจสำเร็จ')
                    return HttpResponseRedirect(reverse('Patient:patient-queue-list', kwargs={}))
    except:
        messages.error(request, 'เพิ่มคนไข้เข้าตรวจไม่สำเร็จ')
        return HttpResponseRedirect(reverse('Patient:patient-queue-list', kwargs={}))
    return render(request, '../templates/patient/patient-present.html')

@login_required(login_url='ClinicManagement:login')  
@user_passes_test(check_doctor, login_url='ClinicManagement:error-page')   
def successful_treatment(request, id):
    try:
        form = SuccessfulTreatmentForm()
        if request.method == 'POST':
            form = SuccessfulTreatmentForm(request.POST)
            if form.is_valid():
                try:
                    s = SuccessfulTreatment.objects.filter(patient_id=id) 
                    s.delete()
                    
                    queue = PatientQueue.objects.filter(patient_id=id).latest('createdAt')
                    patient = get_object_or_404(Patient, id=id)
                    treatment = TreatmentHistory.objects.filter(patient_id=id).latest('createdAt')
                    treatment_form = TreatmentHistoryForm(instance = treatment)
                    
                    success = form.save(commit=False)
                    success.treatment_id = request.POST['treatment1']
                    success.treatmentName = treatment.initialSymptoms
                    success.patientName = str(patient.title) + patient.name
                    success.queueStatus = 'ตรวจสำเร็จ'
                    success.patient_id = patient.id
                    success.queue_id = queue.id
                    success.status1 = 'กำลังรอ'
 
                    try:
                        app = EventAppointment.objects.filter(patient_id=id, treatment_id=treatment.id).latest('createdAt')
                        success.appointment = app.id
                    except:
                        success.appointment = None
                    
                    try:
                        pres = Prescription.objects.filter(patient_id=id, treatment_id=treatment.id).latest('createdAt')
                        success.prescription = pres.id
                    except:
                        success.prescription = None
                        
                    success.save()
                    form.save_m2m()
                    
                    history = treatment_form.save(commit=False)
                    
                    try:
                        app1 = EventAppointment.objects.filter(patient_id=id, treatment_id=treatment.id).latest('createdAt')
                        history.app = app1.id
                    except:
                        history.app = None
                    
                    try:
                        pres1 = Prescription.objects.filter(patient_id=id, treatment_id=treatment.id).latest('createdAt')
                        history.pres = pres1.id
                    except:
                        history.pres = None
                    
                    history.save()
                    
                    q = PatientQueueForm(request.POST or None, instance = queue)
                    q1 = q.save(commit=False) 
                    q1.status = 'ตรวจสำเร็จ'
                    q1.save()
                    
                    messages.success(request, 'รักษาเสร็จสิ้น')
                    return HttpResponseRedirect(reverse('Patient:patient-present-data', kwargs={}))
                except:
                    queue = PatientQueue.objects.filter(patient_id=id).latest('createdAt')
                    patient = get_object_or_404(Patient, id=id)
                    treatment = TreatmentHistory.objects.filter(patient_id=id).latest('createdAt')
                    treatment_form = TreatmentHistoryForm(instance = treatment)

                    success = form.save(commit=False)
                    success.treatment_id = request.POST['treatment1']
                    success.treatmentName = treatment.initialSymptoms
                    success.patientName = str(patient.title) + patient.name
                    success.queueStatus = 'ตรวจสำเร็จ'
                    success.patient_id = patient.id
                    success.status1 = 'กำลังรอ'
                    
                    try:
                        app = EventAppointment.objects.filter(patient_id=id, treatment_id=treatment.id).latest('createdAt')
                        success.appointment = app.id
                    except:
                        success.appointment = None
                    
                    try:
                        pres = Prescription.objects.filter(patient_id=id, treatment_id=treatment.id).latest('createdAt')
                        success.prescription = pres.id
                    except:
                        success.prescription = None
                    
                    success.save()
                    form.save_m2m()
                    
                    history = treatment_form.save(commit=False)
                    
                    try:
                        app1 = EventAppointment.objects.filter(patient_id=id, treatment_id=treatment.id).latest('createdAt')
                        history.app = app1.id
                        print('here4')
                    except:
                        history.app = None
                        print('here5')
                    
                    try:
                        pres1 = Prescription.objects.filter(patient_id=id, treatment_id=treatment.id).latest('createdAt')
                        history.pres = pres1.id
                        print('here6')
                    except:
                        history.pres = None
                        print('here7')
                    
                    history.save()
                    
                    q = PatientQueueForm(request.POST or None, instance = queue)
                    q1 = q.save(commit=False) 
                    q1.status = 'ตรวจสำเร็จ'
                    q1.save()
                    
                    messages.success(request, 'รักษาเสร็จสิ้น')
                    return HttpResponseRedirect(reverse('Patient:patient-present-data', kwargs={}))
            messages.error(request, 'รักษาไม่เสร็จสิ้น')
    except:
        messages.error(request, 'รักษาไม่เสร็จสิ้น')
    return render(request, '../templates/patient/patient-present.html')

@login_required(login_url='ClinicManagement:login')    
def show_successful_treatment(request):
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
        
    today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
    today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)

    success = SuccessfulTreatment.objects.filter(status1='กำลังรอ')
    app = EventAppointment.objects.filter(createdAt__range=(today_min, today_max)).count()
    pres = Prescription.objects.filter(createdAt__range=(today_min, today_max)).count()
            
    form = SuccessfulTreatmentForm()
    
    page = request.GET.get('page', 1)
    paginator = Paginator(success, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = success.count()
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return render(request, '../templates/patient/successful-treatment.html', {
        'page_obj': page_obj,
        'count': count,
        'form': form,
        'app': app,
        'pres': pres,
        'empty': empty,
    })
    
@login_required(login_url='ClinicManagement:login')    
def delete_successful_treatment(request, id):
    # data = get_object_or_404(SuccessfulTreatment, id=id) 
    # data.delete()
    # messages.success(request, 'เข้ารับการรักษาเสร็จเรียบร้อย')
    # return HttpResponseRedirect(reverse('Patient:show-successful-treatment', kwargs={}))
    data = get_object_or_404(SuccessfulTreatment, id = id)
    form = SuccessfulTreatmentForm(request.POST or None, instance = data)
    finish = form.save(commit=False)
    finish.status1 = 'สำเร็จ'
    finish.save()
    messages.success(request, 'จบการรักษาผู้ป่วย')
    return HttpResponseRedirect(reverse('Patient:show-successful-treatment', kwargs={}))
    
# เพิ่มการรักษา โยนไปที่ present patient data page
# @login_required(login_url='ClinicManagement:login')    
# def add_present_patient(request, id):
#     try:
#         patient = get_object_or_404(Patient, id=id) 
#         form = TreatmentHistoryForm()
#         if request.method == 'POST':
#             form = TreatmentHistoryForm(request.POST, request.FILES)
#             if form.is_valid():
#                 treatment = form.save(commit=False)
#                 treatment.patient_id = patient.id
#                 treatment.patientTitle = patient.title
#                 treatment.patientName = patient.name
#                 treatment.number = 1 
#                 treatment.save()
#                 form.save_m2m()
#                 queue = PatientQueue.objects.filter(patient_id=id)
#                 queue.delete()
#                 messages.success(request, 'เพิ่มคนไข้เข้าตรวจสำเร็จ')
#                 return HttpResponseRedirect(reverse('Patient:patient-queue-list', kwargs={}))
#     except:
#         messages.error(request, 'ไม่พบข้อมูลคนไข้ท่านนี้ในระบบ')
#         return HttpResponseRedirect(reverse('Patient:patient-queue-list', kwargs={}))

#     return render(request, '../templates/patient/patient-present.html')

#เพิ่มการวินิจฉัย หมอ
@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_doctor, login_url='ClinicManagement:error-page')  
def add_treatment_history(request, id):
    data = TreatmentHistory.objects.filter(patient_id=id).latest('createdAt')
    form = TreatmentHistoryForm(instance = data)

    if request.method == 'POST':
        form = TreatmentHistoryForm(request.POST, request.FILES, instance = data)
        if form.is_valid(): 
            patient = form.save(commit=False)
            patient.initialSymptoms = request.POST['initialSymptoms']
            patient.initial_id = request.POST['initialId']
            patient.doctorName = request.user.title + request.user.first_name + " " + request.user.last_name
            patient.save()
            messages.success(request, 'เพิ่มการวินิจฉัยสำเร็จ')
            return HttpResponseRedirect(reverse('Patient:patient-present-data', kwargs={}))
        messages.error(request, 'เพิ่มการวินิจฉัยไม่สำเร็จ')     
    return render(request, "../templates/patient/patient-present.html")

@login_required(login_url='ClinicManagement:login')
def show_treatment_history(request, id):
    treatment_history = TreatmentHistory.objects.filter(patient_id=id).order_by('-createdAt')
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    
    page = request.GET.get('page', 1)
    paginator = Paginator(treatment_history, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = treatment_history.count()
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return render(request, '../templates/patient/patient-treatment-history.html', {
        'page_obj': page_obj,
        'count': count,
        'empty': empty,
    })

@login_required(login_url='ClinicManagement:login')
def patient_present_data(request):
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
        
    form = AllergicHistoryForm()
    appointmentForm = EventAppointmentForm()
    treatmentForm = TreatmentHistoryForm()
    pres = PrescriptionForm()
    medicine = Medicine.objects.all()
    medicineUnit = MedicineUnit.objects.all()
    today = date.today()
    today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
    today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
    latest_prescript = 'ไม่มีรายการยา'
    latest_appointment1 = 'ไม่มีการนัดหมาย'
    
    try:
        queue = PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์')
        if queue.count() > 0:
            queueStatus = 1
        else:
            queueStatus = 0
    except:
        queueStatus = 0
 
    if TreatmentHistory.objects.count() == 0:
        object = 0
        empty = 'ว่าง'
        return render(request, '../templates/patient/patient-present.html', {'object': object, 'empty': empty})
    else:
        object = 1
        present = TreatmentHistory.objects.latest('createdAt')
        patient = Patient.objects.get(id=present.patient_id)
        treatment = TreatmentHistory.objects.filter(patient_id=patient.id).latest('createdAt')
        prescript = Prescription.objects.filter(treatment_id=treatment.id)
        allergic = Allergic.objects.filter(patient_id=present.patient_id)
        
        try:
            latest_treatment = TreatmentHistory.objects.filter(patient_id=patient.id).order_by('-createdAt')[1]
            try:
                latest_prescript = Prescription.objects.filter(treatment_id=latest_treatment.id)
            except:
                latest_prescript = 'ไม่มีรายการยา'
            try:
                latest_appointment1 = EventAppointment.objects.filter(treatment_id=latest_treatment.id)
            except:
                latest_appointment1 = 'ไม่มีการนัดหมาย'
        except:
            latest_treatment = 'ไม่พบประวัติการรักษาครั้งล่าสุด'
        
        dob = patient.dob
        dobSplit = dob.split("-")
        dobYear = dobSplit[0]
        dobDay = dobSplit[2]
        dobMonth = dobSplit[1]
        
        mo = int(dobMonth)
        month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[mo]
        thai_year = int(dobYear) + 543
        x = ("%d %s %d"%(int(dobDay), month_name, thai_year))
    
    try:
        initialObj = 0
        initial = InitialSymptoms.objects.filter(patient_id=present.patient_id, createdAt__range=(today_min, today_max)).latest('createdAt')
    except:
        initialObj = 1
        initial = 'พยาบาลไม่ได้ระบุอาการเบื้องต้น'
        
    allergic = Allergic.objects.filter(patient_id=present.patient_id)
    
    context = {
        'data': patient,
        'present': present,
        'object': object,
        'form': form,
        'initial': initial,
        'initialObj': initialObj,
        'allergic': allergic,
        'appointmentForm': appointmentForm,
        'treatmentForm': treatmentForm,
        'pres': pres,
        'medicine': medicine,
        'medicineUnit': medicineUnit,
        'treatment': treatment,
        'prescript': prescript,
        'd': today,
        'queueStatus': queueStatus,
        'empty': empty,
        'x': x,
        'latest_treatment': latest_treatment,
        'latest_prescript': latest_prescript,
        'latest_appointment1': latest_appointment1
    }
    
    return render(request, '../templates/patient/patient-present.html', context)

@login_required(login_url='ClinicManagement:login')    
def add_patient_initial_symptoms(request, id):
    patient = get_object_or_404(Patient, id=id) 
    form = InitialSymptomsForm()
    if request.method == 'POST':
        form = InitialSymptomsForm(request.POST, request.FILES)
        if form.is_valid():
            initial = form.save(commit=False)
            initial.initialSymptoms = request.POST['initialSymptoms']
            initial.patient_id = patient.id
            initial.nurseId = request.user.id
            initial.save()
            form.save_m2m()
            messages.success(request, 'บันทึกอาการเบื้องต้นสำเร็จ')
            return HttpResponseRedirect(reverse('Patient:patient-list', kwargs={}))
    return render(request, '../templates/patient/patient-present.html')

@login_required(login_url='ClinicManagement:login')    
def patient_initial_symptoms(request, id): 
    today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
    today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
    
    if InitialSymptoms.objects.count() == 0:
        object = 0
        return render(request, '../templates/patient/patient-present.html', {'object': object})
    else:
        object = 1
        present = InitialSymptoms.objects.filter(createdAt__range=(today_min, today_max)).latest('createdAt')
        patient = Patient.objects.get(id=present.patient_id)
    return render(request, '../templates/patient/patient-present.html', {
        'data': patient,
        'initial': present,
        'object': object,
    })

@login_required(login_url='ClinicManagement:login')       
@user_passes_test(check_nurse, login_url='ClinicManagement:error-page')                
def patient_add(request):
    form = PatientForm()
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        today = date.today()
        year = today.year
        if form.is_valid():
            patient = form.save(commit=False)
            dob = patient.dob
            dobSplit = dob.split("-")
            dobYear = dobSplit[0]
            age = int(year) - int(dobYear)
            
            patient.slug = defaultfilters.slugify(unidecode(patient.name))
            patient.age = age
            patient.save()
            form.save_m2m()
            messages.success(request, 'บันทึกข้อมูลสำเร็จ')
            return HttpResponseRedirect(reverse('Patient:patient-list', kwargs={}))
        messages.error(request, 'กรุณากรอกข้อมูลให้ครบถ้วน')
    return render(request, '../templates/patient/patient-add.html', {
        'form': form,
        'empty': empty,
    })

@login_required(login_url='ClinicManagement:login')   
@user_passes_test(check_nurse, login_url='ClinicManagement:error-page')      
def patient_delete(request, id):
    data = get_object_or_404(Patient, id=id) 

    data.delete()
    messages.success(request, 'ลบข้อมูลสำเร็จ')
    return HttpResponseRedirect(reverse('Patient:patient-list', kwargs={}))

@login_required(login_url='ClinicManagement:login')
def patient_detail(request, id, slug):
    patient = get_object_or_404(Patient, id=id, slug=slug)
    allergic = Allergic.objects.filter(patient_id=id)
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    
    dob = patient.dob
    dobSplit = dob.split("-")
    dobYear = dobSplit[0]
    dobDay = dobSplit[2]
    dobMonth = dobSplit[1]
    
    mo = int(dobMonth)
    month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[mo]
    thai_year = int(dobYear) + 543
    x = ("%d %s %d"%(int(dobDay), month_name, thai_year))
    
    return render(request, '../templates/patient/patient-detail.html', {
        'data': patient,
        'allergic': allergic,
        'x': x,
        'empty': empty
    })

@login_required(login_url='ClinicManagement:login')    
@user_passes_test(check_nurse, login_url='ClinicManagement:error-page')     
def patient_update(request, id, slug):
    data = get_object_or_404(Patient, id = id, slug = slug)
    form = PatientForm(request.POST or None, instance = data)
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'

    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES, instance = data)
        today = date.today()
        year = today.year
        if form.is_valid():
            patient = form.save(commit=False)
            dob = patient.dob
            dobSplit = dob.split("-")
            dobYear = dobSplit[0]
            age = int(year) - int(dobYear)
            patient.age = age
            patient.slug = defaultfilters.slugify(unidecode(patient.name))
            patient.save()
            messages.success(request, 'แก้ไขข้อมูลสำเร็จ')
            return HttpResponseRedirect(reverse('Patient:patient-list', kwargs={}))
        messages.error(request, 'แก้ไขข้อมูลไม่สำเร็จ')
    return render(request, "../templates/patient/patient-update.html", {
        'form': form,
        'empty': empty
    })

@login_required(login_url='ClinicManagement:login')
def patient_search(request):
    form = InitialSymptomsForm()
    search = request.GET.get('q')
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    if search:
        result = Patient.objects.filter(Q(name__icontains=search)|Q(hn__icontains=search)|Q(idCard__icontains=search))
        count = result.count()
        
        page = request.GET.get('page', 1)
        paginator = Paginator(result, 10)
        
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return render(request, '../templates/patient/patient-search.html', {
            'page_obj': page_obj, 
            'count': count,
            'form': form,
            'empty': empty
        })
        
    return render(request, '../templates/patient/patient-search.html')

@login_required(login_url='ClinicManagement:login')
def success_search(request):
    search = request.GET.get('q')
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    if search:
        result = SuccessfulTreatment.objects.filter(Q(patientName__icontains=search))
        count = result.count()
        
        page = request.GET.get('page', 1)
        paginator = Paginator(result, 10)
        
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return render(request, '../templates/patient//successful-treatment-search.html', {
            'page_obj': page_obj, 
            'count': count,
            'empty': empty
        })
        
    return render(request, '../templates/patient/successful-treatment-search.html')

@login_required(login_url='ClinicManagement:login')
def show_present_prescription(request, id):
    prescript = Prescription.objects.filter(treatment_id=id)
    print(prescript)
    count = prescript.count()
    
    context = {
        'prescript': prescript,
        'count': count,
    }
    
    return render(request, '../templates/patient/successful-treatment.html', context)