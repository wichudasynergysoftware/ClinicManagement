from django.contrib import admin
from .models import *
    
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('medCode', 'name', 'slug', 'type', 'tradeName', 'genericName', 'initial', 'countingUnit',
                    'packingUnit', 'costPrice', 'sellingPrice', 'medicineStrength', 'indication', 
                    'direction', 'createdAt', 'updatedAt')

    
admin.site.register(Medicine, MedicineAdmin)
