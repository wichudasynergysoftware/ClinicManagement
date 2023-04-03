# Generated by Django 4.1.3 on 2023-03-19 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReceivePaymentPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openPositionAmount', models.FloatField(max_length=10, verbose_name='ยอดยกมา')),
                ('receiveAmount', models.FloatField(default=0, max_length=10, verbose_name='จำนวนเงินรับ')),
                ('paymentAmount', models.FloatField(default=0, max_length=10, verbose_name='จำนวนเงินจ่าย')),
                ('closePositionAmount', models.FloatField(max_length=10, verbose_name='ยอดฐานะสิ้นวัน')),
                ('closeCurrentPositionAmount', models.FloatField(max_length=10, verbose_name='ยอดฐานะสิ้นวันพึ่งจ่ายได้')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReceivePaymentTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='ชื่อรายการ')),
                ('type', models.CharField(choices=[('รายรับ', 'รายรับ'), ('รายจ่าย', 'รายจ่าย')], default='รายรับ', max_length=10, verbose_name='ประเภทรายการ')),
                ('amount', models.FloatField(default=0, max_length=10, verbose_name='จำนวนเงิน')),
                ('remark', models.CharField(blank=True, max_length=500, null=True, verbose_name='หมายเหตุ')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
