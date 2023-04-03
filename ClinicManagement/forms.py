from django import forms
from .models import *
import datetime
from django.contrib.auth.forms import UserCreationForm
    
NAME_TITLE_CHOICE = (
    ('นาย','นาย'),
    ('นาง','นาง'),
    ('นางสาว','นางสาว'),
    ('เด็กหญิง','เด็กหญิง'),
    ('เด็กชาย','เด็กชาย'),
)

class NewUserForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = '__all__' 
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('title', 'first_name', 'last_name', 'email')
        
class NurseForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = '__all__' 
        
class DoctorForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_doctor = forms.BooleanField(required=False, label="หมอ")
    is_nurse = forms.BooleanField(required=False, label="พยาบาล")
    is_admin = forms.BooleanField(required=False, label="ผู้ดูแลระบบ")

    class Meta:
        model = MyUser
        fields = ('username', 'password1', 'password2', 'email', 'is_admin', 'is_nurse', 'is_doctor', 
                  'first_name', 'last_name', 'title')
           
    def save(self, commit=True):
        user = super(DoctorForm, self).save(commit=False)
        user.title = self.cleaned_data['title']
        user.is_doctor = True
        user.is_nurse = False
        user.is_admin = False
        user.slug = user.username
        
        if commit:
            user.save()
        return user

class NurseForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_doctor = forms.BooleanField(required=False, label="หมอ")
    is_nurse = forms.BooleanField(required=False, label="พยาบาล")
    is_admin = forms.BooleanField(required=False, label="ผู้ดูแลระบบ")

    class Meta:
        model = MyUser
        fields = ('username', 'password1', 'password2', 'email', 'is_admin', 'is_nurse', 'is_doctor', 
                  'first_name', 'last_name', 'title')
           
    def save(self, commit=True):
        user = super(NurseForm, self).save(commit=False)
        user.title = self.cleaned_data['title']
        user.is_doctor = False
        user.is_nurse = True
        user.is_admin = False
        user.slug = user.username
        
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        widgets = {
            'dob': forms.DateInput(format=('%d-%m-%Y'), attrs={'pattern=': '\d{4}-\d{2}-\d{2}', 'lang': 'TH', 'format': 'yyyy-mm-dd', 'type': 'date'}),
            'address': forms.Textarea(attrs={'rows':3}),
        }
        fields = ('gender', 'dob', 'phone', 'idCard', 'address', 'img', 'medicalLicense')
    
# class NewUserForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     is_doctor = forms.BooleanField(required=False, label="หมอ")
#     is_nurse = forms.BooleanField(required=False, label="พยาบาล")
#     is_admin = forms.BooleanField(required=False, label="ผู้ดูแลระบบ")
    
#     class Meta:
#         model = MyUser
#         widgets = {
#             'dob': forms.DateInput(format=('%d-%m-%Y'), attrs={'pattern=': '\d{4}-\d{2}-\d{2}', 'lang': 'TH', 'format': 'yyyy-mm-dd', 'type': 'date'}),
#             'address': forms.Textarea(attrs={'rows':3}),
#         }
#         fields = ('username', 'password1', 'password2', 'email', 'is_admin', 'is_nurse', 'is_doctor', 'first_name', 'last_name',
#                   'age', 'gender', 'title', 'dob', 'phone', 'idCard', 'address', 'img', 'medicalLicense')
        
#     def save(self, commit=True):
#         user = super(NewUserForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']
#         user.is_admin = self.cleaned_data['is_admin']
#         user.is_nurse = self.cleaned_data['is_nurse']
#         user.is_doctor = self.cleaned_data['is_doctor']
#         user.age = self.cleaned_data['age']
#         user.gender = self.cleaned_data['gender']
#         user.title = self.cleaned_data['title']
#         user.dob = self.cleaned_data['dob']
#         user.phone = self.cleaned_data['phone']
#         user.idCard = self.cleaned_data['idCard']
#         user.address = self.cleaned_data['address']
#         user.img = self.cleaned_data['img']
#         user.medicalLicense = self.cleaned_data['medicalLicense']
#         user.slug = user.username
        
#         if commit:
#             user.save()
#         return user

# class DoctorForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     is_doctor = forms.BooleanField(required=False, label="หมอ")
#     is_nurse = forms.BooleanField(required=False, label="พยาบาล")
#     is_admin = forms.BooleanField(required=False, label="ผู้ดูแลระบบ")
#     age = forms.CharField(max_length=10, label='อายุ')
    
#     class Meta:
#         model = MyUser
#         widgets = {
#             'dob': forms.DateInput(format=('%d-%m-%Y'), attrs={'pattern=': '\d{4}-\d{2}-\d{2}', 'lang': 'TH', 'format': 'yyyy-mm-dd', 'type': 'date'}),
#             'address': forms.Textarea(attrs={'rows':3}),
#         }
#         fields = ('username', 'password1', 'password2', 'email', 'is_admin', 'is_nurse', 'is_doctor', 'first_name', 'last_name',
#                   'age', 'gender', 'title', 'dob', 'phone', 'idCard', 'address', 'img', 'medicalLicense')
        
#     def save(self, commit=True):
#         user = super(DoctorForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']
#         user.is_admin = self.cleaned_data['is_admin']
#         user.is_nurse = self.cleaned_data['is_nurse']
#         user.is_doctor = self.cleaned_data['is_doctor']
#         user.gender = self.cleaned_data['gender']
#         user.title = self.cleaned_data['title']
#         user.dob = self.cleaned_data['dob']
#         user.age = self.cleaned_data['age']
#         user.phone = self.cleaned_data['phone']
#         user.idCard = self.cleaned_data['idCard']
#         user.address = self.cleaned_data['address']
#         user.img = self.cleaned_data['img']
#         user.medicalLicense = self.cleaned_data['medicalLicense']
#         user.slug = user.username
        
#         user.is_doctor = True
#         user.is_nurse = False
#         user.is_admin = False
        
#         if commit:
#             user.save()
#         return user
        
# class NurseForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     is_doctor = forms.BooleanField(required=False, label="หมอ")
#     is_nurse = forms.BooleanField(required=False, label="พยาบาล")
#     is_admin = forms.BooleanField(required=False, label="ผู้ดูแลระบบ")
#     age = forms.CharField(max_length=10, label='อายุ')
    
#     class Meta:
#         model = MyUser
#         widgets = {
#             'dob': forms.DateInput(format=('%d-%m-%Y'), attrs={'pattern=': '\d{4}-\d{2}-\d{2}', 'lang': 'TH', 'format': 'yyyy-mm-dd', 'type': 'date'}),
#             'address': forms.Textarea(attrs={'rows':3}),
#         }
#         fields = ('username', 'password1', 'password2', 'email', 'is_admin', 'is_nurse', 'is_doctor', 'first_name', 'last_name',
#                   'age', 'gender', 'title', 'dob', 'phone', 'idCard', 'address', 'img', 'medicalLicense')
        
#     def save(self, commit=True):
#         user = super(NurseForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']
#         user.is_admin = self.cleaned_data['is_admin']
#         user.is_nurse = self.cleaned_data['is_nurse']
#         user.is_doctor = self.cleaned_data['is_doctor']
#         user.gender = self.cleaned_data['gender']
#         user.title = self.cleaned_data['title']
#         user.dob = self.cleaned_data['dob']
#         user.age = self.cleaned_data['age']
#         user.phone = self.cleaned_data['phone']
#         user.idCard = self.cleaned_data['idCard']
#         user.address = self.cleaned_data['address']
#         user.img = self.cleaned_data['img']
#         user.medicalLicense = self.cleaned_data['medicalLicense']
#         user.slug = user.username
        
#         user.is_doctor = False
#         user.is_nurse = True
#         user.is_admin = False
        
#         if commit:
#             user.save()
#         return user
