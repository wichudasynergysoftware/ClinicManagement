from django.urls import path
from . import views

urlpatterns = [
    path('units', views.show_units, name='show-units'),
    path('units/add-medicine-unit', views.add_medicine_unit, name='add-medicine-unit'),
    path('units/medicine-unit-list', views.medicine_unit_list, name='medicine-unit-list'),
    path('delete-medicine-unit/<str:id>', views.delete_medicine_unit, name='delete-medicine-unit'),
    path('update-medicine-unit/<str:id>', views.update_medicine_unit, name='update-medicine-unit'),
    
    path('units/add-medicine-type', views.add_medicine_type, name='add-medicine-type'),
    path('units/medicine-type-list', views.medicine_type_list, name='medicine-type-list'),
    path('delete-medicine-type/<str:id>', views.delete_medicine_type, name='delete-medicine-type'),
    path('update-medicine-type/<str:id>', views.update_medicine_type, name='update-medicine-type'),
    
    path('units/add-name-title', views.add_name_title, name='add-name-title'),
    path('units/name-title-list', views.name_title_list, name='name-title-list'),
    path('delete-name-title/<str:id>', views.delete_name_title, name='delete-name-title'),
    path('update-name-title/<str:id>', views.update_name_title, name='update-name-title'),
    
    path('units/add-essential-medicine', views.add_essential_medicine, name='add-essential-medicine'),
    path('units/essential-medicine-list', views.essential_medicine_list, name='essential-medicine-list'),
    path('delete-essential-medicine/<str:id>', views.delete_essential_medicine, name='delete-essential-medicine'),
    path('update-essential-medicine/<str:id>', views.update_essential_medicine, name='update-essential-medicine'),
    
    path('units/add-working-time', views.add_working_time, name='add-working-time'),
    path('units/working-time-list', views.working_time_list, name='working-time-list'),
    path('delete-working-time/<str:id>', views.delete_working_time, name='delete-working-time'),
    path('update-working-time/<str:id>', views.update_working_time, name='update-working-time'),
]