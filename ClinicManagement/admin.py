from django.contrib import admin
from .models import *

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'dob', 'phone', 'idCard', 'address', 'image', 'image2')
    
admin.site.register(MyUser)
admin.site.register(Profile, ProfileAdmin)

