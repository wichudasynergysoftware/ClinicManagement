from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('medicine/list', views.medicine_list, name='medicine-list'),
    path('medicine/add/', views.medicine_add, name='medicine-add'),
    path('medicine/detail/<str:id>/<slug:slug>/', views.medicine_detail, name='medicine-detail'),
    path('medicine/delete/<str:id>/', views.medicine_delete, name='medicine-delete'),
    path('medicine/update/<str:id>/<slug:slug>/', views.medicine_update, name='medicine-update'),
    path('medicine/search', views.medicine_search, name='medicine-search'),
]