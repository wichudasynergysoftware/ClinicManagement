from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from django.utils.text import slugify
from unidecode import unidecode
from django.template import defaultfilters
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from django.db.models import Sum
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from io import BytesIO
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date
from django.utils.safestring import mark_safe
import calendar
from django.views import generic
from Patient.models import *
from ReceiveAndPaymentTransaction.models import *
import matplotlib.pyplot as plt
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.db.models.functions import ExtractMonth
from django.db.models.functions import TruncMonth

def check_staff(user: MyUser):
    return user.is_staff or user.is_superuser

def check_doctor(user: MyUser):
    return user.is_doctor

def check_nurse(user: MyUser):
    return user.is_nurse

def check_nurse_doctor(user: MyUser):
    return user.is_nurse and user.is_doctor

@login_required(login_url='ClinicManagement:login')
def profile(request: HttpRequest):
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    user = request.user
    is_new_profile = False
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        
        try:
            extended_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        except:
            extended_form = ProfileForm(request.POST, request.FILES)
            is_new_profile = True
            
        if form.is_valid() and extended_form.is_valid(): 
            form.save()
            today = date.today()
            year = today.year
            if is_new_profile:
                profile = extended_form.save(commit=False)
                dob = profile.dob
                dobSplit = dob.split("-")
                dobYear = dobSplit[0]
                age = int(year) - int(dobYear)
                profile.user = user 
                profile.age = age
                profile.save()
                messages.success(request, 'แก้ไขข้อมูลผู้ใช้สำเร็จ')
            else:
                profile = extended_form.save(commit=False)
                dob = profile.dob
                dobSplit = dob.split("-")
                dobYear = dobSplit[0]
                age = int(year) - int(dobYear)
                profile.user = user 
                profile.age = age
                profile.save()
                messages.success(request, 'แก้ไขข้อมูลผู้ใช้สำเร็จ')
            
            return HttpResponseRedirect(reverse('ClinicManagement:edit-user-profile'))
    else:
        form = UserProfileForm(instance=user)
        try:
            extended_form = ProfileForm(instance=user.profile)
        except:
            extended_form = ProfileForm(request.POST, request.FILES)
        
    context = {
        'form': form, 
        'extended_form': extended_form,
        'empty': empty,
    }
    
    return render(request, '../templates/doctor/edit-profile.html', context)
    
@login_required(login_url='ClinicManagement:login')
def get_user_profile(request, username):
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    try:
        obj = 1
        user = MyUser.objects.get(username = username)
        profile = Profile.objects.get(user_id=user.id)
        dob = profile.dob
        dobSplit = dob.split("-")
        dobYear = dobSplit[0]
        dobDay = dobSplit[2]
        dobMonth = dobSplit[1]
        
        mo = int(dobMonth)
        month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[mo]
        thai_year = int(dobYear) + 543
        x = ("%d %s %d"%(int(dobDay), month_name, thai_year))
    except:
        x = 1
        obj = 2
        profile = 'คุณยังไม่ได้เพิ่มข้อมูลโปรไฟล์'
        
    context = {
        'user': user, 
        'profile': profile,
        'obj': obj,
        'x': x,
        'empty': empty,
    }
    
    return render(request, '../templates/doctor/profile.html', context)

@login_required(login_url='ClinicManagement:login')
def doctor_index(request):
    user = request.user
    today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
    today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
    today = timezone.now()
    one_year_ago = today - timedelta(days=365)
    
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'

    if (user.is_authenticated == True) and (user.is_staff == True | user.is_superuser == True):
        patient = Patient.objects.count()
        patientMale = Patient.objects.filter(gender='ชาย').count()
        patientFemale = Patient.objects.filter(gender='หญิง').count()
        patientNone = Patient.objects.filter(gender='ไม่ระบุ').count()
        
        data1 = [0] * 12  
        data2 = [0] * 12  
        labels1 = []

        for i in range(1, 13):
            start_date = date(date.today().year, i, 1)
            end_date = start_date.replace(day=28) + timedelta(days=4) 
            end_date -= timedelta(days=end_date.day)  

            income_data = ReceivePaymentTransaction.objects.filter(type='รายรับ', updatedAt__gte=start_date, updatedAt__lte=end_date).aggregate(total_income=Sum('amount'))['total_income']
            expense_data = ReceivePaymentTransaction.objects.filter(type='รายจ่าย', updatedAt__gte=start_date, updatedAt__lte=end_date).aggregate(total_expense=Sum('amount'))['total_expense']
            if income_data is None:
                income_data = 0
            data1[i-1] = income_data
            labels1.append(start_date.strftime('%B %Y'))
            
            if expense_data is None:
                expense_data = 0
            data2[i-1] = expense_data

        # print("incomes_per_month :", data1)
        # print("expense_per_month :", data2)
        
        doctor = MyUser.objects.filter(is_doctor=True).count()
        nurse = MyUser.objects.filter(is_nurse=True).count()
        
        receiveToday = ReceivePaymentTransaction.objects.filter(type='รายรับ', updatedAt__range=(today_min, today_max)).aggregate(Sum('amount'))
        receiveTodayVal = receiveToday['amount__sum']
        
        paymentToday = ReceivePaymentTransaction.objects.filter(type='รายจ่าย', updatedAt__range=(today_min, today_max)).aggregate(Sum('amount'))
        paymentTodayVal = paymentToday['amount__sum']
  
        total = ReceivePaymentTransaction.objects.filter(type='รายรับ').aggregate(Sum('amount'))
        totalReceive = total['amount__sum']
        
        totalPayment = ReceivePaymentTransaction.objects.filter(type='รายจ่าย').aggregate(Sum('amount'))
        payment = totalPayment['amount__sum']
        
        if receiveTodayVal is None:
            receiveTodayVal = 0
            
        if paymentTodayVal is None:
            paymentTodayVal = 0
            
        if payment is None:
            payment = 0
            
        if totalReceive is None:
            totalReceive = 0
        
        if (totalReceive is None) and (payment is None):
            totalReceive = 0
            payment = 0
            
        else:
            remaining = int(totalReceive) - int(payment)
        
        remaining = int(totalReceive) - int(payment)
        
        labels = ['ไม่ระบุ', 'หญิง', 'ชาย']
        data = []
        data.append(patientNone)
        data.append(patientFemale)
        data.append(patientMale)
        
        largest_number = data[0]
        for number in data:
            if number > largest_number:
                largest_number = number
        
        users = []
        users.append(doctor)
        users.append(nurse)
        largest_number1 = users[0]
        for number in data:
            if number > largest_number:
                largest_number = number
        
        receive = []
        receive.append(totalReceive)
        receive.append(payment)
        
        monthName = []
        
        for i in range(1,13):
            month = calendar.month_name[i]
            monthName.append(month)
            
        thai_months = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม']

        context = {
            'totalReceive': totalReceive,
            'payment': payment,
            'remaining': remaining,
            'patient': patient,
            'data': data,
            'labels': labels,
            'patientFemale': patientFemale,
            'patientMale': patientMale,
            'patientNone': patientNone,
            'patient': patient,   
            'users': users,
            'receive': receive,
            'monthName': monthName,
            'receiveTodayVal': receiveTodayVal,
            'paymentTodayVal': paymentTodayVal,
            'largest_number': largest_number,
            'largest_number1': largest_number1,
            'empty': empty,
            'incomes_per_month': data1,
            'expense_per_month': data2,
            'month_name': labels1,
            'thai_months': thai_months
        }
    else:
        return HttpResponseRedirect(reverse('Patient:patient-queue-list', kwargs={}))
    
    return render(request, '../templates/doctor/index.html', context)

@login_required(login_url='ClinicManagement:login')
def error_page(request):
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    return render(request, '../templates/doctor/error.html', {'empty': empty})

@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def doctor_list(request):
    doctor = MyUser.objects.filter(is_doctor=True).values()
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    
    page = request.GET.get('page', 1)
    paginator = Paginator(doctor, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = doctor.count()
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return render(request, '../templates/doctor/doctor-list.html', {
        'page_obj': page_obj,
        'count': count,
        'empty': empty,
    })

@login_required(login_url='ClinicManagement:login')            
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')      
def doctor_add(request):
    form = DoctorForm()
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            form.save_m2m()
            messages.success(request, 'บันทึกข้อมูลสำเร็จ')
            return HttpResponseRedirect(reverse('ClinicManagement:doctor-list', kwargs={}))
        messages.error(request, 'กรุณากรอกข้อมูลให้ครบถ้วน')
    return render(request, '../templates/doctor/doctor-add.html', {
        'form': form,
        'empty': empty,
    })

@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def doctor_delete(request, id):
    data = get_object_or_404(MyUser, id=id) 

    data.delete()
    messages.success(request, 'ลบข้อมูลสำเร็จ')
    return HttpResponseRedirect(reverse('ClinicManagement:doctor-list', kwargs={}))

@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def doctor_detail(request, id, slug):
    doctor = get_object_or_404(MyUser, id=id, slug=slug)
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    
    try:
        profile = get_object_or_404(Profile, user_id=id)
        dob = profile.dob
        dobSplit = dob.split("-")
        dobYear = dobSplit[0]
        dobDay = dobSplit[2]
        dobMonth = dobSplit[1]
        
        mo = int(dobMonth)
        month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[mo]
        thai_year = int(dobYear) + 543
        x = ("%d %s %d"%(int(dobDay), month_name, thai_year))
    except:
        x = 1
        profile = 'ผู้ใช้ยังไม่ได้ทำการเพิ่มข้อมูล'
        
    context = {
        'data': doctor,
        'profile': profile,
        'x': x,
        'empty': empty
    }
    
    return render(request, '../templates/doctor/doctor-detail.html', context)

@login_required(login_url='ClinicManagement:login')    
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def doctor_update(request, id, slug):
    data = get_object_or_404(MyUser, id = id, slug = slug)
    form = DoctorForm(request.POST or None, instance = data)
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'

    if request.method == 'POST':
        form = DoctorForm(request.POST,request.FILES,instance = data)
        if form.is_valid():
            nurse = form.save(commit=False)
            nurse.is_doctor = True
            nurse.save()
            messages.success(request, 'แก้ไขข้อมูลสำเร็จ')
            return HttpResponseRedirect(reverse('ClinicManagement:doctor-list', kwargs={}))
        messages.error(request, 'แก้ไขข้อมูลไม่สำเร็จ')
    return render(request, "../templates/doctor/doctor-update.html", {
        'form': form,
        'empty': empty,
    })

@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def doctor_search(request):
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    search = request.GET.get('q')
    count = 0
    if search:
        result = MyUser.objects.filter(Q(first_name__icontains=search)|Q(last_name__icontains=search), is_doctor=True)
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

        return render(request, '../templates/doctor/doctor-search.html', {
            'page_obj': page_obj, 
            'count': count,
            'empty': empty,
        })
    else:
        return render(request, '../templates/doctor/doctor-search.html', {'empty': empty, 'count': count})

@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def nurse_list(request):
    nurse = MyUser.objects.filter(is_nurse=True).values()
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    
    page = request.GET.get('page', 1)
    paginator = Paginator(nurse, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = nurse.count()
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return render(request, '../templates/nurse/nurse-list.html', {
        'page_obj': page_obj,
        'count': count,
        'empty': empty,
    })

@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def nurse_add(request):
    form = NurseForm()
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    
    if request.method == 'POST':
        form = NurseForm(request.POST, request.FILES)
        if form.is_valid():
            nurse = form.save(commit=False)
            nurse.is_nurse = True
            nurse.save()
            form.save_m2m()
            messages.success(request, 'บันทึกข้อมูลสำเร็จ')
            return HttpResponseRedirect(reverse('ClinicManagement:nurse-list', kwargs={}))
        messages.error(request, 'กรุณากรอกข้อมูลให้ครบถ้วน')
    return render(request, '../templates/nurse/nurse-add.html', {
        'form': form,
        'empty': empty,
    })

@login_required(login_url='ClinicManagement:login')    
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def nurse_delete(request, id):
    data = get_object_or_404(MyUser, id=id) 

    data.delete()
    messages.success(request, 'ลบข้อมูลสำเร็จ')
    return HttpResponseRedirect(reverse('ClinicManagement:nurse-list', kwargs={}))

@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def nurse_detail(request, id, slug):
    nurse = get_object_or_404(MyUser, id=id, slug=slug)
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    try:
        profile = get_object_or_404(Profile, user_id=id)
        dob = profile.dob
        dobSplit = dob.split("-")
        dobYear = dobSplit[0]
        dobDay = dobSplit[2]
        dobMonth = dobSplit[1]
        
        mo = int(dobMonth)
        month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[mo]
        thai_year = int(dobYear) + 543
        x = ("%d %s %d"%(int(dobDay), month_name, thai_year))
    except:
        profile = 'ผู้ใช้ยังไม่ได้ทำการเพิ่มข้อมูล'
        x = 1
        
    context = {
        'data': nurse,
        'profile': profile,
        'x': x,
        'empty': empty,
    }
    
    return render(request, '../templates/nurse/nurse-detail.html', context)

@login_required(login_url='ClinicManagement:login')    
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def nurse_update(request, id, slug):
    data = get_object_or_404(MyUser, id = id, slug = slug)
    form = NurseForm(request.POST or None, instance = data)
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'

    if request.method == 'POST':
        form = NurseForm(request.POST,request.FILES,instance = data)
        if form.is_valid():
            nurse = form.save(commit=False)
            nurse.is_nurse = True
            nurse.save()
            messages.success(request, 'แก้ไขข้อมูลสำเร็จ')
            return HttpResponseRedirect(reverse('ClinicManagement:nurse-list', kwargs={}))
        messages.error(request, 'แก้ไขข้อมูลไม่สำเร็จ')
    return render(request, "../templates/nurse/nurse-update.html", {
        'form': form,
        'empty': empty,
    })

@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def nurse_search(request):
    search = request.GET.get('q')
    count = 0
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    if search:
        result = MyUser.objects.filter(Q(first_name__icontains=search)|Q(last_name__icontains=search), is_nurse=True)
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

        return render(request, '../templates/nurse/nurse-search.html', {
            'page_obj': page_obj, 
            'count': count,
            'empty': empty
        })
        
    else:
        return render(request, '../templates/nurse/nurse-search.html', {'empty': empty, 'count': count})