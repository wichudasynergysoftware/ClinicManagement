from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('prescriptions', views.prescriptions, name='prescriptions'),
    path('add-prescriptions/<str:id>', views.add_prescription, name='add-prescription'),
    path('export-prescriptions/<str:id>', views.export_prescription, name='export-prescription'),
    path('show-prescriptions/<str:id>', views.show_prescription, name='show-prescription'),
    
    path('delete-prescriptions/<str:id>', views.prescription_delete, name='delete-prescription'),
    path('update-prescriptions/<str:id>', views.prescription_update, name='update-prescription'),
]