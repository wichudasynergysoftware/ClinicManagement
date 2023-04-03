from django.contrib.auth.models import AbstractUser
from django.db import models

INCOME_EXPENSE_CHOICES = (
    ('รายรับ','รายรับ'),
    ('รายจ่าย','รายจ่าย'), 
)

class ReceivePaymentTransaction(models.Model):
    name = models.CharField(max_length=100, verbose_name='ชื่อรายการ')
    type = models.CharField(max_length=10, choices=INCOME_EXPENSE_CHOICES, default="รายรับ", verbose_name='ประเภทรายการ')
    amount = models.FloatField(max_length=10, verbose_name='จำนวนเงิน', default=0)
    remark = models.CharField(max_length=500, blank=True, null=True, verbose_name='หมายเหตุ')
    createdAt = models.DateTimeField(auto_now_add=True, blank=False)
    updatedAt = models.DateTimeField(auto_now=True, blank=False)
    
class ReceivePaymentPosition(models.Model):
    openPositionAmount = models.FloatField(max_length=10, verbose_name='ยอดยกมา') # คิดจากยอดฐานะสิ้นวันของวันก่อนหน้า
    receiveAmount = models.FloatField(max_length=10, verbose_name='จำนวนเงินรับ', default=0)
    paymentAmount = models.FloatField(max_length=10, verbose_name='จำนวนเงินจ่าย', default=0)
    closePositionAmount = models.FloatField(max_length=10, verbose_name='ยอดฐานะสิ้นวัน') # รายรับ - รายจ่าย
    closeCurrentPositionAmount = models.FloatField(max_length=10, verbose_name='ยอดฐานะสิ้นวันพึ่งจ่ายได้') # รายรับ - รายจ่าย
    createdAt = models.DateTimeField(auto_now_add=True, blank=False)
    updatedAt = models.DateTimeField(auto_now=True, blank=False)
    