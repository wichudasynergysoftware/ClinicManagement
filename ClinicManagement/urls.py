from django.urls import reverse_lazy
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.doctor_index, name='doctor-index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='../templates/registration/password_reset.html', success_url='done/'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('ClinicManagement:password_reset_complete')), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('user/profile/<str:username>/', views.get_user_profile, name='get-user-profile'),
    path('edit/profile/', views.profile, name='edit-user-profile'),
    
    path('doctor/list', views.doctor_list, name='doctor-list'),
    path('doctor/add/', views.doctor_add, name='doctor-add'),
    path('doctor/detail/<str:id>/<slug:slug>/', views.doctor_detail, name='doctor-detail'),
    path('doctor/delete/<str:id>/', views.doctor_delete, name='doctor-delete'),
    path('doctor/update/<str:id>/<slug:slug>/', views.doctor_update, name='doctor-update'),
    path('doctor/search', views.doctor_search, name='doctor-search'),
    
    path('nurse/list', views.nurse_list, name='nurse-list'),
    path('nurse/add/', views.nurse_add, name='nurse-add'),
    path('nurse/detail/<str:id>/<slug:slug>/', views.nurse_detail, name='nurse-detail'),
    path('nurse/delete/<str:id>/', views.nurse_delete, name='nurse-delete'),
    path('nurse/update/<str:id>/<slug:slug>/', views.nurse_update, name='nurse-update'),
    path('nurse/search', views.nurse_search, name='nurse-search'),
    path('error-page', views.error_page, name='error-page'),
    
]