"""ClinicManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', include(('ClinicManagement.urls', 'ClinicManagement'), namespace='ClinicManagement')),
    path('', include(('Appointment.urls', 'Appointment'), namespace='Appointment')),
    path('', include(('Patient.urls', 'Patient'), namespace='Patient')),
    path('', include(('MedicineStock.urls', 'MedicineStock'), namespace='MedicineStock')),
    path('', include(('ReceiveAndPaymentTransaction.urls', 'ReceiveAndPaymentTransaction'), namespace='ReceiveAndPaymentTransaction')),
    path('', include(('Prescription.urls', 'Prescription'), namespace='Prescription')),
    path('', include(('Unit.urls', 'Unit'), namespace='Unit')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)