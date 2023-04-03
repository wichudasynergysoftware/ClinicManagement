from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from ClinicManagement.models import MyUser
from Patient.models import Patient, PatientQueue
from .models import *
from .forms import *
from django.utils.text import slugify
from unidecode import unidecode
import datetime
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date
from django.utils.safestring import mark_safe
import calendar
from django.views import generic
from .utils import Calendar
from django.contrib.auth.decorators import user_passes_test

def check_staff(user: MyUser):
    return user.is_staff or user.is_superuser

def check_nurse(user: MyUser):
    return user.is_staff or user.is_superuser or user.is_nurse

def check_doctor(user: MyUser):
    return user.is_staff or user.is_superuser or user.is_doctor

class CalendarView(generic.ListView):
    # เรียกโมเดลนี้มาใช้ เพื่อเอาไปแสดงผลที่หน้าเว็บ
    model = EventAppointment
    template_name = '../templates/appointment/calendar.html'

    # กำหนดข้อมูลในเทมเพลต โดยเรียกฟังก์ชันอื่นมาใช้ แล้วรีเทิร์นค่าออกไปเป็นดิก
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['empty'] = empty()
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        # รับพารามิเตอร์ req mont มา จากนั้นจะแยกเดือนและปีออกจากกันด้วย - และแปลงให้เป็นตัวเลข
        return date(year, month, day=1)
        # จะสร้าง obj date โดยใส่ค่า year, month และใส่วันที่เป็นันที่ 1 เสมอ หากไม่ได้ระบุวันที่
    return datetime.today()
    # return datetime.today ของวันที่เริ่มต้นของเดือนที่กำหนดใน req month หรือวันปัจจุบัน หากไม่ได้กำหนดไว้

# เดือนก่อนหน้า
def prev_month(d):
    first = d.replace(day=1) # ให้ตัวแปรนี้เท่ากับวันที่ที่ส่งเข้ามา (d) เท่ากับวันแรกของเดือนที่รับมา
    prev_month = first - timedelta(days=1) # ลบจำนวนวันที่ 1 จากวันแรกของเดือนนั้นด้วย timedelta(days=1) เพื่อให้ได้วันก่อนหน้าเดือนนั้น
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    # เอาปีและเดือนของวันก่อนหน้า ทำให้เป็นสตริง แล้วรีเทิร์นออกไปด้วยจ้า
    return month

# เดือนถัดไป
def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def empty():
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    return empty

@login_required(login_url='ClinicManagement:login')  
@user_passes_test(check_doctor, login_url='ClinicManagement:error-page') 
def event(request, event_id):
    # instance คือ พารามิเตอร์ตัวหนึ่งที่ใช้ในการสร้างฟอร๋ม เมื่อมีการแก้ไขข้อมูล เป็น obj ของโมเดลที่มีอยู่แล้วใน DB สามารถนำมาใช้เป็นฟอร์มเริ่มต้นได้จ้า
    instance = EventAppointment()
    patient = get_object_or_404(Patient, id=event_id)
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'

    form = EventAppointmentForm(request.POST or None, instance=instance)
    if request.method == 'POST': # ตรวจสอบว่าเมธอดเป็น POST หรือไม่จ้า
        form = EventAppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            # ตรวจสอบความถูกต้องของข้อมูล
            app = form.save(commit=False)
            app.patient_id = patient.id
            app.patientName = patient.name
            app.patientTitle = patient.title
            app.treatment_id = request.POST['treatment']
            app.doctorName = request.user.title + request.user.first_name + " " + request.user.last_name
            app.save()
            form.save_m2m()
            messages.success(request, 'บันทึกนัดหมายสำเร็จ')
            if patient.email :
                t = app.date
                x = t.strftime("%d %B %Y")
                try :
                    subject = 'คลินิกแห่งหนึ่ง'
                    # body = {
                    # 'สวัสดี คุณ': f'{patient.name} คุณได้รับข้อความแจ้งเตือนการนัดหมายจากระบบจัดการคลินิก',
                    # 'หัวข้อการนัดหมาย': app.name,
                    # 'คำอธิบายเพิ่มเติม/ข้อปฏิบัติ': app.description,
                    # 'กำหนดนัดหมาย': app.date,
                    # 'แพทย์เจ้าของไข้': app.doctorName,
                    # 'หมายเหตุ': '\n- หากท่านมีอาการผิดปกติก่อนวันนัด กรุณามาพบแพทย์ได้ทันที \n- กรุณามาตรงตามเวลานัด หากไม่ตรงเวลา ต้องรอตามเวลานัดหรือนัดใหม่ \n- กรุณาติดต่อที่แผนกเวชระเบียน ก่อนเวลานัด 30 นาที \n- กรณีต้องตรวจ แล็ป หรือเอ็กซเรย์ให้มาก่อนเวลานัด'
                    # }
                    # message = '\n'.join('{}  {}'.format(key, value) for key, value in body.items())
                    # เอาไอเทมใน body มา join key, value จะฟอร์แมตสตริงด้วย {}  {}'.format(key, value)
                    
                    message = ''
                    
                    html_message = '''
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
                        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
                        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous" />
                        <link rel="canonical" href="https://getbootstrap.com/docs/5.2/examples/dashboard/">
                        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Kanit">
                        <script src="https://kit.fontawesome.com/9918a0d039.js" crossorigin="anonymous"></script>
                    </head>
                    <body style="font-family: 'Kanit'; font-size: 14px; color: black;">
                        <div class="container">
                            <div class="card mt-5" style='box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); border: solid 2px grey; border-radius:10px;'>
                                <div class="card-body">
                                    <h2 style='text-align:center;'>แจ้งเตือนการนัดหมาย</h2>
                                    <p style='text-align:center;'>ระบบจัดการคลินิก - Clinic Management System</p> 
                                    <div class="text-center mt-5" style='margin-left: 60px;'>
                                        <i class="fa-regular fa-envelope fa-5x"></i>
                                        <br>
                                        <h3>สวัสดี คุณ{}</h3>
                                        <p>คุณมีกำหนดนัดหมายในวันที่ : {} </p>
                                        <p>หัวข้อการนัดหมาย : {} </p>
                                        <p>คำอธิบายเพิ่มเติม/ข้อปฏิบัติ : {} </p> 
                                        <p>แพทย์เจ้าของไข้ : {} </p> 
                                        <br>
                                        <p>หมายเหตุ</p> 
                                        <p>- หากท่านมีอาการผิดปกติก่อนวันนัด กรุณามาพบแพทย์ได้ทันที</p> 
                                        <p>- กรุณามาตรงตามเวลานัด หากไม่ตรงเวลา ต้องรอตามเวลานัดหรือนัดใหม่</p> 
                                        <p>- กรุณาติดต่อที่แผนกเวชระเบียน ก่อนเวลานัด 30 นาที</p> 
                                        <p>- กรณีต้องตรวจ แล็ป หรือเอ็กซเรย์ให้มาก่อนเวลานัด</p> 
                                        <br>
                                        <p>ขอบคุณที่ไว้วางใจคลินิกของเรา</p> 
                                        <br>
                                    </div>
                                    <p class="mt-5 mb-3 text-muted" style='text-align:center;'>&copy; Clinic Management System</p>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    '''.format(patient.name, x, app.name, app.description, app.doctorName)
                    
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [patient.email, ]
                    send_mail( subject, message, email_from, recipient_list, html_message=html_message)
                except:
                    messages.error(request, f'ส่งการแจ้งเตือนนัดหมายไม่สำเร็จ')   
            else:
                pass
            
        return HttpResponseRedirect(reverse('Patient:patient-present-data'))
    return render(request, '../templates/appointment/appointment.html', {'form': form, 'empty': empty})

@login_required(login_url='ClinicManagement:login')  
def event_edit(request, event_id=None):
    instance = EventAppointment()
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
        
    if event_id:
        instance = get_object_or_404(EventAppointment, pk=event_id)
    else:
        instance = EventAppointment()
    form = EventAppointmentForm(request.POST or None, instance=instance)
    
    if request.POST and form.is_valid():
        patient = get_object_or_404(Patient, id=instance.patient_id)
        print(patient.id)
        form.save()
        messages.success(request, 'แก้ไขนัดหมายสำเร็จ')
        if patient.email :
            t = instance.date
            x = t.strftime("%d %B %Y")
            try :
                subject = 'คลินิกแห่งหนึ่ง'
                message = ''
                
                html_message = '''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
                    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous" />
                    <link rel="canonical" href="https://getbootstrap.com/docs/5.2/examples/dashboard/">
                    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Kanit">
                    <script src="https://kit.fontawesome.com/9918a0d039.js" crossorigin="anonymous"></script>
                </head>
                <body style="font-family: 'Kanit'; font-size: 14px; color: black;">
                    <div class="container">
                        <div class="card mt-5" style='box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); border: solid 2px grey; border-radius:10px;'>
                            <div class="card-body">
                                <h2 style='text-align:center;'>แจ้งเตือนการนัดหมาย</h2>
                                <p style='text-align:center;'>ระบบจัดการคลินิก - Clinic Management System</p> 
                                <div class="text-center mt-5" style='margin-left: 60px;'>
                                    <i class="fa-regular fa-envelope fa-5x"></i>
                                    <br>
                                    <h3>สวัสดี คุณ{}</h3>
                                    <p>คุณมีกำหนดนัดหมายในวันที่ : {} </p>
                                    <p>หัวข้อการนัดหมาย : {} </p>
                                    <p>คำอธิบายเพิ่มเติม/ข้อปฏิบัติ : {} </p> 
                                    <p>แพทย์เจ้าของไข้ : {} </p> 
                                    <br>
                                    <p>หมายเหตุ</p> 
                                    <p>- หากท่านมีอาการผิดปกติก่อนวันนัด กรุณามาพบแพทย์ได้ทันที</p> 
                                    <p>- กรุณามาตรงตามเวลานัด หากไม่ตรงเวลา ต้องรอตามเวลานัดหรือนัดใหม่</p> 
                                    <p>- กรุณาติดต่อที่แผนกเวชระเบียน ก่อนเวลานัด 30 นาที</p> 
                                    <p>- กรณีต้องตรวจ แล็ป หรือเอ็กซเรย์ให้มาก่อนเวลานัด</p> 
                                    <br>
                                    <p>ขอบคุณที่ไว้วางใจคลินิกของเรา</p> 
                                    <br>
                                </div>
                                <p class="mt-5 mb-3 text-muted" style='text-align:center;'>&copy; Clinic Management System</p>
                            </div>
                        </div>
                    </div>
                </body>
                </html>
                '''.format(patient.name, x, instance.name, instance.description, instance.doctorName)
                
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [patient.email, ]
                send_mail( subject, message, email_from, recipient_list, html_message=html_message)
            except:
                messages.error(request, f'ส่งการแจ้งเตือนนัดหมายไม่สำเร็จ')   
        else:
            pass
        return HttpResponseRedirect(reverse('Appointment:calendar'))
        
    return render(request, '../templates/appointment/appointment.html', {'form': form, 'empty': empty})
