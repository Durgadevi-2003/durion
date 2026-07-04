"""URL routes for the dashboard and exports."""

from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    path('dashboard/export-excel/', views.export_certificates_excel, name='export_certificates_excel'),
]
