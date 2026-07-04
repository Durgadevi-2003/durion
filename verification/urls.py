"""URL routes for the public verification experience."""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('verify/<str:certificate_number>/', views.verify_certificate, name='verify_certificate'),
]
