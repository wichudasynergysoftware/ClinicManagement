from django import forms
from .models import *
import datetime
      
class ReceivePaymentTransactionForm(forms.ModelForm):
    class Meta:
        model = ReceivePaymentTransaction
        exclude = ['id', 'createdAt', 'updatedAt', 'deletedAt']
