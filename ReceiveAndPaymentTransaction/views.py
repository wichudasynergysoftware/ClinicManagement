from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from ClinicManagement.models import MyUser
from Patient.models import PatientQueue
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
from django.http import HttpResponse
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
from django.contrib.auth.decorators import user_passes_test

def check_staff(user: MyUser):
    return user.is_staff or user.is_superuser

@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def receive_payment_list(request):
    form = ReceivePaymentTransactionForm()
    receive = ReceivePaymentTransaction.objects.all().order_by('-createdAt')
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    
    page = request.GET.get('page', 1)
    paginator = Paginator(receive, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = receive.count()
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
        
    total = ReceivePaymentTransaction.objects.filter(type='รายรับ').aggregate(Sum('amount'))
    totalReceive = total['amount__sum']
    
    totalPayment = ReceivePaymentTransaction.objects.filter(type='รายจ่าย').aggregate(Sum('amount'))
    payment = totalPayment['amount__sum']
    
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

    return render(request, '../templates/receive-payment-transaction/receive-list.html', {
        'page_obj': page_obj,
        'count': count,
        'totalReceive': totalReceive,
        'payment': payment,
        'remaining': remaining,
        'form': form,
        'empty': empty
    })

@login_required(login_url='ClinicManagement:login')   
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def receive_payment_add(request):
    form = ReceivePaymentTransactionForm()
    
    if request.method == 'POST':
        form = ReceivePaymentTransactionForm(request.POST, request.FILES)
        if form.is_valid():
            receive = form.save(commit=False)
            receive.save()
            form.save_m2m()
            messages.success(request, 'บันทึกข้อมูลสำเร็จ')
            return HttpResponseRedirect(reverse('ReceiveAndPaymentTransaction:receive-list', kwargs={}))
        messages.error(request, 'กรุณากรอกข้อมูลให้ครบถ้วน')
    return render(request, '../templates/receive-payment-transaction/receive-add.html', {
        'form': form,
    })

@login_required(login_url='ClinicManagement:login')    
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def receive_payment_update(request, id):
    data = get_object_or_404(ReceivePaymentTransaction, id = id)
    form = ReceivePaymentTransactionForm(request.POST or None, instance = data)

    if request.method == 'POST':
        form = ReceivePaymentTransactionForm(request.POST,request.FILES,instance = data)
        if form.is_valid():
            receive = form.save(commit=False)
            receive.save()
            messages.success(request, 'แก้ไขข้อมูลสำเร็จ')
            return HttpResponseRedirect(reverse('ReceiveAndPaymentTransaction:receive-list', kwargs={}))
        messages.error(request, 'แก้ไขข้อมูลไม่สำเร็จ')
    return render(request, "../templates/receive-payment-transaction/receive-update.html", {
        'form': form,
    })

@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def receive_payment_search(request):
    search = request.GET.get('q')
    count = 0
    if PatientQueue.objects.filter(status='กำลังเข้าพบแพทย์').count() > 0:
        empty = 'ไม่ว่าง'
    else:
        empty = 'ว่าง'
    if search:
        result = ReceivePaymentTransaction.objects.filter(Q(name__icontains=search))
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

        return render(request, '../templates/receive-payment-transaction/receive-search.html', {
            'page_obj': page_obj, 
            'count': count,
            'empty': empty
        })
        
    return render(request, '../templates/receive-payment-transaction/receive-search.html', {
        'count': count,
        'empty': empty
    })

@login_required(login_url='ClinicManagement:login')
@user_passes_test(check_staff, login_url='ClinicManagement:error-page')
def receive_payment_delete(request, id):
    data = get_object_or_404(ReceivePaymentTransaction, id=id) 

    data.delete()
    messages.success(request, 'ลบข้อมูลสำเร็จ')
    return HttpResponseRedirect(reverse('ReceiveAndPaymentTransaction:receive-list', kwargs={}))
 