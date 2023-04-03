from django.contrib import admin
from .models import *

class PatientAdmin(admin.ModelAdmin):
    list_display = ('hn', 'title', 'name', 'age', 'gender', 'number', 'dob',
                    'phone', 'idCard', 'address', 'email', 'createdAt', 'updatedAt')
    
admin.site.register(Patient, PatientAdmin)
admin.site.register(Allergic)
admin.site.register(InitialSymptoms)
admin.site.register(PatientQueue)
admin.site.register(TreatmentHistory)
admin.site.register(SuccessfulTreatment)
