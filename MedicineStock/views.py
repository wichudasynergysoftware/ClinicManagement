from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect

from ClinicManagement.models import MyUser
from .models import *
from .forms import *
from django.utils.text import slugify
from unidecode import unidecode
from django.template import defaultfilters
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from Patient.models import *
from ReceiveAndPaymentTransaction.models import *
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
def medicine_list(request):
    medicine = Medicine.objects.all().order_by('-createdAt')
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    
    page = request.GET.get('page', 1)
    paginator = Paginator(medicine, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = medicine.count()
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return render(request, '../templates/medicineStock/medicine-list.html', {
        'page_obj': page_obj,
        'count': count,
        'empty': empty,
    })

@login_required(login_url='ClinicManagement:login')    
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def medicine_add(request):
    form = MedicineForm()
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES)

        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.slug = defaultfilters.slugify(unidecode(medicine.name))
            # medicine.type_id = request.POST['type']
            # medicine.packingUnit_id = request.POST['packingUnit']
            # medicine.nlem_id = request.POST['nlem']
            medicine.save()
            form.save_m2m()
            messages.success(request, 'บันทึกข้อมูลสำเร็จ')
            return HttpResponseRedirect(reverse('MedicineStock:medicine-list', kwargs={}))
        messages.error(request, 'กรุณากรอกข้อมูลให้ครบถ้วน')
    return render(request, '../templates/medicineStock/medicine-add.html', {
        'form': form,
        'empty': empty,
    })

@login_required(login_url='ClinicManagement:login')    
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def medicine_delete(request, id):
    data = get_object_or_404(Medicine, id=id) 

    data.delete()
    messages.success(request, 'ลบข้อมูลสำเร็จ')
    return HttpResponseRedirect(reverse('MedicineStock:medicine-list', kwargs={}))

@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def medicine_detail(request, id, slug):
    medicine = get_object_or_404(Medicine, id=id, slug=slug)
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    
    return render(request, '../templates/medicineStock/medicine-detail.html', {'data': medicine, 'empty': empty})

@login_required(login_url='ClinicManagement:login')    
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def medicine_update(request, id, slug):
    data = get_object_or_404(Medicine, id = id, slug = slug)
    form = MedicineForm(request.POST or None, instance = data)
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'

    if request.method == 'POST':
        form = MedicineForm(request.POST,request.FILES,instance = data)

        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.slug = defaultfilters.slugify(unidecode(medicine.name))
            medicine.save()
            messages.success(request, 'แก้ไขข้อมูลสำเร็จ')
            return HttpResponseRedirect(reverse('MedicineStock:medicine-list', kwargs={}))
        messages.error(request, 'แก้ไขข้อมูลไม่สำเร็จ')
    return render(request, "../templates/medicineStock/medicine-update.html", {
        'form': form,
        'empty': empty,
    })

@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def medicine_search(request):
    search = request.GET.get('q')
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    count = 0
        
    if search:
        result = Medicine.objects.filter(Q(name__icontains=search))
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

        return render(request, '../templates/medicineStock/medicine-search.html', {
            'page_obj': page_obj, 
            'count': count,
            'empty': empty,
        })
        
    return render(request, '../templates/medicineStock/medicine-search.html', {'count': count, 'empty': empty})
