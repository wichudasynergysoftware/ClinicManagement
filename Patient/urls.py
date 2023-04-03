from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('patient-list', views.patient_list, name='patient-list'),
    path('patient-add/', views.patient_add, name='patient-add'),
    path('patient-detail/<str:id>/<slug:slug>/', views.patient_detail, name='patient-detail'),
    path('patient-delete/<str:id>/', views.patient_delete, name='patient-delete'),
    path('patient-update/<str:id>/<slug:slug>/', views.patient_update, name='patient-update'),
    path('patient-search', views.patient_search, name='patient-search'),
    
    path('patient-pdf/<str:id>', views.generate_pdf, name='patient-pdf'),
    path('patient-appointment/<str:id>', views.export_appointment, name='patient-appointment'),

    path('patient-present/<str:id>/', views.add_present_patient, name='patient-present'),
    path('patient-present', views.patient_present_data, name='patient-present-data'),
    path('patient-queue/<str:id>/', views.add_patient_queue, name='patient-queue'),
    path('patient-queue/list', views.patient_queue_list, name='patient-queue-list'),
    path('patient-delete/queue/<str:id>/', views.patient_delete_queue, name='patient-delete-queue'),
    path('patient-add/patient-allergic-history/<str:id>/', views.add_patient_allergic_history, name='add-patient-allergic-history'),
    path('patient-add/initial-symptom/<str:id>/', views.add_patient_initial_symptoms, name='add-patient-initial-symptom'),
    path('patient-initial-symptom/<str:id>/', views.patient_initial_symptoms, name='patient-initial-symptom'),

    path('patient-treatment-history/<str:id>/', views.add_treatment_history, name='add-treatment-history'),
    path('show-patient-treatment-history/<str:id>/', views.show_treatment_history, name='show-patient-treatment-history'),
    path('patient-appointment-treatment/<str:id>', views.export_appointment_treatment, name='patient-appointment-treatment'),

    path('successful-treatment/<str:id>', views.successful_treatment, name='successful-treatment'),
    path('show-successful-treatment', views.show_successful_treatment, name='show-successful-treatment'), 
    path('delete-successful-treatment/<str:id>/', views.delete_successful_treatment, name='delete-successful-treatment'),
    path('show-prescriptions/<str:id>', views.show_prescription, name='show-prescription'),
    
    path('patient-successful-treatment-search', views.success_search, name='patient-successful-treatment-search'),
    path('show-present-prescription/<str:id>/', views.show_present_prescription, name='show-present-prescription'),
    path('export-csv-patient', views.export_csv_patient, name='export-csv-patient'),
    
    path('test', views.render_pdf_view, name='test'),
    path('test-pdf/<pk>', views.patient_render_pdf_view, name='test-pdf'),
    
    path('export-patient-record/<str:id>', views.export_patient_record, name='export-patient-record'),
    path('export-patient-prescriptions/<str:id>', views.export_patient_prescriptions, name='export-patient-prescriptions'),
    path('export-patient-appointment/<str:id>', views.export_patient_appointment, name='export-patient-appointment'),
    path('export-patient-prescriptions-present/<str:id>', views.export_patient_prescriptions_present, name='export-patient-prescriptions-present'),
    path('export-patient-prescriptions-treatment/<str:id>', views.export_patient_prescriptions_treatment, name='export-patient-prescriptions-treatment'),
    path('export-patient-appointment-treatment/<str:id>', views.export_patient_appointment_treatment, name='export-patient-appointment-treatment'),
]