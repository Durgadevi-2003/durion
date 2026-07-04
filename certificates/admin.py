"""Admin configuration for certificate management."""

from django.contrib import admin

from .models import Certificate, VerificationLog


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    """Admin interface for certificate records."""
    list_display = ('certificate_number', 'intern_name', 'course_domain', 'status', 'created_at')
    search_fields = ('certificate_number', 'intern_name', 'course_domain', 'mentor_name')
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at', 'updated_at', 'qr_code')


@admin.register(VerificationLog)
class VerificationLogAdmin(admin.ModelAdmin):
    """Admin interface for verification log records."""
    list_display = ('certificate_number', 'status', 'verification_time', 'ip_address')
    search_fields = ('certificate_number', 'status')
    list_filter = ('status', 'verification_time')
    readonly_fields = ('verification_time',)
