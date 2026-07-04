"""URL routes for certificate management and downloads."""

from django.urls import path

from . import views

urlpatterns = [
    path('certificate/add/', views.certificate_add, name='certificate_add'),
    path('certificate/list/', views.certificate_list, name='certificate_list'),
    path('certificate/edit/<int:pk>/', views.certificate_edit, name='certificate_edit'),
    path('certificate/delete/<int:pk>/', views.certificate_delete, name='certificate_delete'),
    path('download/<str:certificate_number>/', views.download_certificate, name='download_certificate'),
    path('email/<str:certificate_number>/', views.email_certificate, name='email_certificate'),
]
