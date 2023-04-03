from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect

from ClinicManagement.models import MyUser
from Patient.models import PatientQueue
from .models import *
from .forms import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

def check_staff(user: MyUser):
    return user.is_staff or user.is_superuser

def check_doctor(user: MyUser):
    return user.is_doctor

def check_nurse(user: MyUser):
    return user.is_nurse

def check_nurse_doctor(user: MyUser):
    return user.is_nurse and user.is_doctor

@login_required(login_url='ClinicManagement:login')    
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def show_units(request):
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    return render(request, '../templates/unit/unit-list.html', {
        'empty': empty
    })

@login_required(login_url='ClinicManagement:login')
def add_medicine_unit(request):
    form = MedicineUnitForm()
    if request.method == 'POST':
        form = MedicineUnitForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.name = request.POST['name']
            unit.save()
            form.save_m2m()
            messages.success(request, 'บันทึกหน่วยยาสำเร็จ')
            return HttpResponseRedirect(reverse('Unit:medicine-unit-list', kwargs={}))
        messages.error(request, 'หน่วยยามีอยู่แล้ว')
        return HttpResponseRedirect(reverse('Unit:medicine-unit-list', kwargs={}))
    return render(request, '../templates/unit/medicine-unit.html', {
        'form': form,
    })
    
@login_required(login_url='ClinicManagement:login')   
@user_passes_test(check_staff, login_url='ClinicManagement:error-page') 
def delete_medicine_unit(request, id):
    data = get_object_or_404(MedicineUnit, id=id) 
    data.delete()
    messages.success(request, 'ลบหน่วยยาสำเร็จ')
    return HttpResponseRedirect(reverse('Unit:medicine-unit-list', kwargs={}))

@login_required(login_url='ClinicManagement:login')   
@user_passes_test(check_staff, login_url='ClinicManagement:error-page') 
def update_medicine_unit(request, id):
    data = get_object_or_404(MedicineUnit, id = id)
    form = MedicineUnitForm(request.POST or None, instance = data)

    if request.method == 'POST':
        form = MedicineUnitForm(request.POST, instance = data)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.name = request.POST['name']
            medicine.save()
            messages.success(request, 'แก้ไขหน่วยยาสำเร็จ')
            return HttpResponseRedirect(reverse('Unit:medicine-unit-list', kwargs={}))
        messages.error(request, 'หน่วยยามีอยู่แล้ว')
        return HttpResponseRedirect(reverse('Unit:medicine-unit-list', kwargs={}))
    return render(request, "../templates/unit/medicine-unit.html", {
        'form': form,
    })
    
@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def medicine_unit_list(request):
    unit = MedicineUnit.objects.all()
    form = MedicineUnitForm()
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    
    page = request.GET.get('page', 1)
    paginator = Paginator(unit, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = unit.count()
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return render(request, '../templates/unit/medicine-unit.html', {
        'page_obj': page_obj,
        'count': count,
        'form': form,
        'empty': empty,
    })
    
@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def add_medicine_type(request):
    form = MedicineTypeForm()
    if request.method == 'POST':
        form = MedicineTypeForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.name = request.POST['name']
            unit.save()
            form.save_m2m()
            messages.success(request, 'บันทึกประเภทยาสำเร็จ')
            return HttpResponseRedirect(reverse('Unit:medicine-type-list', kwargs={}))
        messages.error(request, 'ประเภทยามีอยู่แล้ว')
        return HttpResponseRedirect(reverse('Unit:medicine-type-list', kwargs={}))
    return render(request, '../templates/unit/medicine-type.html', {
        'form': form,
    })
    
@login_required(login_url='ClinicManagement:login')    
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def delete_medicine_type(request, id):
    data = get_object_or_404(MedicineType, id=id) 
    data.delete()
    messages.success(request, 'ลบประเภทยาสำเร็จ')
    return HttpResponseRedirect(reverse('Unit:medicine-type-list', kwargs={}))

@login_required(login_url='ClinicManagement:login')    
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def update_medicine_type(request, id):
    data = get_object_or_404(MedicineType, id = id)
    form = MedicineTypeForm(request.POST or None, instance = data)

    if request.method == 'POST':
        form = MedicineTypeForm(request.POST, instance = data)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.name = request.POST['name']
            medicine.save()
            messages.success(request, 'แก้ไขประเภทยาสำเร็จ')
            return HttpResponseRedirect(reverse('Unit:medicine-type-list', kwargs={}))
        messages.error(request, 'ประเภทยามีอยู่แล้ว')
        return HttpResponseRedirect(reverse('Unit:medicine-type-list', kwargs={}))
    return render(request, "../templates/unit/medicine-type.html", {
        'form': form,
    })
    
@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def medicine_type_list(request):
    unit = MedicineType.objects.all()
    form = MedicineTypeForm()
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    
    page = request.GET.get('page', 1)
    paginator = Paginator(unit, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = unit.count()
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return render(request, '../templates/unit/medicine-type.html', {
        'page_obj': page_obj,
        'count': count,
        'form': form,
        'empty': empty,
    })
    
@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def add_name_title(request):
    form = NameTitleForm()
    if request.method == 'POST':
        form = NameTitleForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.name = request.POST['name']
            unit.save()
            form.save_m2m()
            messages.success(request, 'บันทึกคำนำหน้าชื่อสำเร็จ')
            return HttpResponseRedirect(reverse('Unit:name-title-list', kwargs={}))
        messages.error(request, 'คำนำหน้าชื่อมีอยู่แล้ว')
        return HttpResponseRedirect(reverse('Unit:name-title-list', kwargs={}))
    return render(request, '../templates/unit/name-title.html', {
        'form': form,
    })
    
@login_required(login_url='ClinicManagement:login')    
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def delete_name_title(request, id):
    data = get_object_or_404(NameTitle, id=id) 
    data.delete()
    messages.success(request, 'ลบคำนำหน้าชื่อสำเร็จ')
    return HttpResponseRedirect(reverse('Unit:name-title-list', kwargs={}))

@login_required(login_url='ClinicManagement:login') 
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')   
def update_name_title(request, id):
    data = get_object_or_404(NameTitle, id = id)
    form = NameTitleForm(request.POST or None, instance = data)

    if request.method == 'POST':
        form = NameTitleForm(request.POST, instance = data)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.name = request.POST['name']
            medicine.save()
            messages.success(request, 'แก้ไขคำนำหน้าชื่อสำเร็จ')
            return HttpResponseRedirect(reverse('Unit:name-title-list', kwargs={}))
        messages.error(request, 'คำนำหน้าชื่อมีอยู่แล้ว')
        return HttpResponseRedirect(reverse('Unit:name-title-list', kwargs={}))
    return render(request, "../templates/unit/name-title.html", {
        'form': form,
    })
    
@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def name_title_list(request):
    unit = NameTitle.objects.all()
    form = NameTitleForm()
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    
    page = request.GET.get('page', 1)
    paginator = Paginator(unit, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = unit.count()
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return render(request, '../templates/unit/name-title.html', {
        'page_obj': page_obj,
        'count': count,
        'form': form,
        'empty': empty,
    })
    
@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def add_essential_medicine(request):
    form = ThailandNationalListOfEssentialMedicinesForm()
    if request.method == 'POST':
        form = ThailandNationalListOfEssentialMedicinesForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.name = request.POST['name']
            unit.save()
            form.save_m2m()
            messages.success(request, 'บันทึกบัญชียาหลักแห่งชาติสำเร็จ')
            return HttpResponseRedirect(reverse('Unit:essential-medicine-list', kwargs={}))
        messages.error(request, 'บัญชียาหลักแห่งชาติมีอยู่แล้ว')
        return HttpResponseRedirect(reverse('Unit:essential-medicine-list', kwargs={}))
    return render(request, '../templates/unit/essential-medicine.html', {
        'form': form,
    })
    
@login_required(login_url='ClinicManagement:login')    
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def delete_essential_medicine(request, id):
    data = get_object_or_404(ThailandNationalListOfEssentialMedicines, id=id) 
    data.delete()
    messages.success(request, 'ลบบัญชียาหลักแห่งชาติสำเร็จ')
    return HttpResponseRedirect(reverse('Unit:essential-medicine-list', kwargs={}))

@login_required(login_url='ClinicManagement:login')    
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def update_essential_medicine(request, id):
    data = get_object_or_404(ThailandNationalListOfEssentialMedicines, id = id)
    form = ThailandNationalListOfEssentialMedicinesForm(request.POST or None, instance = data)

    if request.method == 'POST':
        form = ThailandNationalListOfEssentialMedicinesForm(request.POST, instance = data)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.name = request.POST['name']
            medicine.save()
            messages.success(request, 'แก้ไขบัญชียาหลักแห่งชาติสำเร็จ')
            return HttpResponseRedirect(reverse('Unit:essential-medicine-list', kwargs={}))
        messages.error(request, 'บัญชียาหลักแห่งชาติมีอยู่แล้ว')
        return HttpResponseRedirect(reverse('Unit:essential-medicine-list', kwargs={}))
    return render(request, "../templates/unit/essential-medicine.html", {
        'form': form,
    })
    
@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def essential_medicine_list(request):
    unit = ThailandNationalListOfEssentialMedicines.objects.all()
    form = ThailandNationalListOfEssentialMedicinesForm()
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    
    page = request.GET.get('page', 1)
    paginator = Paginator(unit, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = unit.count()
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return render(request, '../templates/unit/essential-medicine.html', {
        'page_obj': page_obj,
        'count': count,
        'form': form,
        'empty': empty,
    })
    
@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def add_working_time(request):
    form = WorkingTimeForm()
    if request.method == 'POST':
        form = WorkingTimeForm(request.POST)
        if form.is_valid():
            working_time = form.save(commit=False)
            working_time.save()
            form.save_m2m()
            messages.success(request, 'บันทึกช่วงเวลาสำเร็จ')
            return HttpResponseRedirect(reverse('Unit:working-time-list', kwargs={}))
        messages.error(request, 'ช่วงเวลานี้มีอยู่แล้ว')
        return HttpResponseRedirect(reverse('Unit:working-time-list', kwargs={}))
    return render(request, '../templates/unit/working-time.html', {
        'form': form,
    })
    
@login_required(login_url='ClinicManagement:login')    
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def delete_working_time(request, id):
    data = get_object_or_404(WorkingTime, id=id) 
    data.delete()
    messages.success(request, 'ลบช่วงเวลาสำเร็จ')
    return HttpResponseRedirect(reverse('Unit:working-time-list', kwargs={}))

@login_required(login_url='ClinicManagement:login')    
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def update_working_time(request, id):
    data = get_object_or_404(WorkingTime, id = id)
    form = WorkingTimeForm(request.POST or None, instance = data)

    if request.method == 'POST':
        form = WorkingTimeForm(request.POST, instance = data)
        if form.is_valid():
            working_time = form.save(commit=False)
            # medicine.time = request.POST['name']
            working_time.save()
            messages.success(request, 'แก้ไขช่วงเวลาสำเร็จ')
            return HttpResponseRedirect(reverse('Unit:working-time-list', kwargs={}))
        messages.error(request, 'ช่วงเวลานี้มีอยู่แล้ว')
        return HttpResponseRedirect(reverse('Unit:working-time-list', kwargs={}))
    return render(request, "../templates/unit/working-time.html", {
        'form': form,
    })
    
@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def working_time_list(request):
    worksTime = WorkingTime.objects.all()
    form = WorkingTimeForm()
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    
    page = request.GET.get('page', 1)
    paginator = Paginator(worksTime, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = worksTime.count()
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return render(request, '../templates/unit/working-time.html', {
        'page_obj': page_obj,
        'count': count,
        'form': form,
        'empty': empty,
    })