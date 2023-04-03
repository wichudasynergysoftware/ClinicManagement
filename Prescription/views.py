from io import BytesIO
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect

from ClinicManagement.models import MyUser
from .models import *
from .forms import *
from django.db.models import Sum
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from django.contrib.auth.decorators import login_required
from Patient.models import Patient
from MedicineStock.models import Medicine
from datetime import datetime, timedelta, date
from django.contrib.auth.decorators import user_passes_test

def check_staff(user: MyUser):
    return user.is_staff or user.is_superuser

def check_nurse(user: MyUser):
    return user.is_staff or user.is_superuser or user.is_nurse

def check_doctor(user: MyUser):
    return user.is_staff or user.is_superuser or user.is_doctor

@login_required(login_url='ClinicManagement:login')
def prescriptions(request):
    return render(request, '../templates/prescription/prescription.html')

@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_doctor, login_url='ClinicManagement:error-page') 
def add_prescription(request, id):
    patient = get_object_or_404(Patient, id=id)
    form = PrescriptionForm(request.POST or None)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.patient_id = patient.id
            prescription.patientName = str(patient.title) + patient.name
            prescription.treatment_id = request.POST['treatment']
            prescription.medicine_id = request.POST['medicine']
            prescription.medicineAmount = request.POST['medicineAmount']
            prescription.medicineUnit_id = request.POST['medicineUnit']
            prescription.doctorName = request.user.title + request.user.first_name + " " + request.user.last_name
            prescription.save()
            messages.success(request, 'เพิ่มยาในใบสั่งยาสำเร็จ')
            return HttpResponseRedirect(reverse('Patient:patient-present-data', kwargs={}))
        messages.error(request, 'เพิ่มยาในใบสั่งยาไม่สำเร็จ')     
    return render(request, "../templates/prescription/prescription.html", {'form': form})

@login_required(login_url='ClinicManagement:login')   
def export_prescription(request, id):
     
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont('F1', 15, leading=None)
    d = date.today()
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = f'inline; filename="{d}.pdf"'
    
    try:
        pres = Prescription.objects.get(treatment_id=id)
        patient = Patient.objects.get(id=pres.patient_id)
        
        p.drawString(260, 780, "ใบสั่งยา")
        p.drawString(130, 750, "(กรุณามาก่อนเวลานัด 30 นาที : Please contact us 30 minutes before the appointment.)")
        
        p.drawString(50, 700, "ชื่อ-นามสกุล (Name and Surname) :")
        p.drawString(200, 700, pres.patientName)
        
        p.drawString(390, 700, "HN (Hospital Number) :")
        p.drawString(500, 700, patient.hn)
        
        p.drawString(50, 655, "รายการยา :")
        p.drawString(130, 655, str(pres.medicineId))
        
        p.drawString(150, 655, "จำนวน")
        p.drawString(180, 655, str(pres.medicineAmount))
        
        p.drawString(200, 655, "หน่วยยา")
        p.drawString(230, 655, pres.medicineUnit)
        
        # p.drawString(50, 620, "รายการยา :")
        # p.drawString(200, 620, str(pres.medicineAmount))
        
        # p.drawString(50, 570, "นัดมาเพื่อ (Appointment To) :")
        # p.drawString(190, 570, app.name)
        
        # p.drawString(50, 540, "ข้อปฏิบัติก่อนเข้าพบแพทย์ (Preparation) :")
        # p.drawString(240, 540, app.description)
        
        p.drawString(50, 400, "หมายเหตุ (Remark) :")
        p.drawString(80, 370, "- หากท่านมีอาการผิดปกติก่อนวันนัด กรุณามาพบแพทย์ได้ทันที")
        p.drawString(80, 340, "- กรุณามาตรงตามเวลานัด หากไม่ตรงเวลา ต้องรอตามเวลานัดหรือนัดใหม่")
        p.drawString(80, 310, "- กรุณาติดต่อที่แผนกเวชระเบียน ก่อนเวลานัด 30 นาที")
        p.drawString(80, 280, "- กรณีต้องตรวจ แล็ป หรือเอ็กซเรย์ให้มาก่อนเวลานัด")
        
        p.drawString(370, 150, "ผู้ออกใบสั่งยา :")
        p.drawString(440, 150, pres.doctorName)
        
        p.drawString(370, 120, "วันที่ออกบัตรนัด :")
        p.drawString(450, 120, str(d))

        p.line(20, 680, 580, 680)
        p.line(20, 600, 580, 600)
        p.line(20, 680, 20, 600)
        p.line(580, 680, 580, 600)
    
        p.setTitle(f'Report on {d} {patient.title + patient.name}')
        
    except:
        p.drawString(260, 780, "ไม่มีใบสั่งยา")
        p.setTitle(f'Report on {d}')
        
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

@login_required(login_url='ClinicManagement:login')   
def show_prescription(request, id):
    pres = Prescription.objects.get(treatment_id=id)
    return render(request, "../templates/patient/successful-treatment.html", {'pres': pres})

@login_required(login_url='ClinicManagement:login')    
@user_passes_test(check_doctor, login_url='ClinicManagement:error-page') 
def prescription_delete(request, id):
    data = get_object_or_404(Prescription, id=id) 

    data.delete()
    messages.success(request, 'ลบรายการยาสำเร็จ')
    return HttpResponseRedirect(reverse('Patient:patient-present-data', kwargs={}))

@login_required(login_url='ClinicManagement:login')  
@user_passes_test(check_doctor, login_url='ClinicManagement:error-page')   
def prescription_update(request, id):
    data = get_object_or_404(Prescription, id = id)
    form = PrescriptionForm(request.POST or None, instance = data)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST, request.FILES, instance = data)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.treatment_id = request.POST['treatment']
            prescription.medicine_id = request.POST['medicine']
            prescription.medicineAmount = request.POST['medicineAmount']
            prescription.medicineUnit_id = request.POST['medicineUnit']
            prescription.doctorName = request.user.title + request.user.first_name + " " + request.user.last_name
            prescription.save()
            messages.success(request, 'แก้ไขข้อมูลสำเร็จ')
            return HttpResponseRedirect(reverse('Patient:patient-present-data', kwargs={}))
        messages.error(request, 'แก้ไขข้อมูลไม่สำเร็จ')
    return render(request, "../templates/patient/patient-present.html", {
        'pres': form,
    })