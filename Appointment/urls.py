from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('appointment/show-calendar', views.CalendarView.as_view(), name='calendar'),
    path('appointment/<str:event_id>', views.event, name='event_new'),
    path('appointment-edit/<str:event_id>', views.event_edit, name='event_edit'),
]