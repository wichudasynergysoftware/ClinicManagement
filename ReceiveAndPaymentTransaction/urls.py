from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('receive-payment/list', views.receive_payment_list, name='receive-list'),
    path('receive-payment/add/', views.receive_payment_add, name='receive-add'),
    path('receive-payment/delete/<str:id>/', views.receive_payment_delete, name='receive-delete'),
    path('receive-payment/update/<str:id>/', views.receive_payment_update, name='receive-update'),
    path('receive-payment/search', views.receive_payment_search, name='receive-search'),
]