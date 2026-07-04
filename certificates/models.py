"""Database models for internship certificates and verification logs."""

from io import BytesIO

import qrcode
from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone


class Certificate(models.Model):
    """Represents an internship certificate issued by Durion Technologies."""

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('revoked', 'Revoked'),
        ('pending', 'Pending'),
    ]

    certificate_number = models.CharField(max_length=50, unique=True)
    intern_name = models.CharField(max_length=255)
    internship_id = models.CharField(max_length=100, blank=True, null=True)
    course_domain = models.CharField(max_length=255)
    internship_duration = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    completion_date = models.DateField()
    performance_grade = models.CharField(max_length=20, blank=True, null=True)
    mentor_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, default='Durion Technologies')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    student_photo = models.ImageField(upload_to='certificates/photos/', blank=True, null=True)
    certificate_pdf = models.FileField(upload_to='certificates/pdfs/', blank=True, null=True)
    certificate_template = models.CharField(max_length=100, default='default')
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.certificate_number} - {self.intern_name}'

    def get_public_url(self):
        return f'https://yourdomain.com/verify/{self.certificate_number}'

    def generate_qr_code(self):
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(self.get_public_url())
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white').convert('RGB')
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        filename = f'{self.certificate_number}.png'
        self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)

    def save(self, *args, **kwargs):
        if not self.certificate_number:
            self.certificate_number = self.generate_certificate_number()
        if not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_certificate_number():
        prefix = 'DUR'
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        return f'{prefix}{timestamp}'


class VerificationLog(models.Model):
    """Stores every public verification attempt."""

    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE, related_name='verification_logs')
    certificate_number = models.CharField(max_length=50)
    verification_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    browser = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, default='verified')

    def __str__(self):
        return f'{self.certificate_number} - {self.status}'
