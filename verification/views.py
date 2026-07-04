"""Public-facing views for home search and certificate verification."""

from django.contrib import messages
from django.shortcuts import redirect, render

from certificates.models import Certificate, VerificationLog


def home_view(request):
    """Render the professional landing page with search."""
    if request.method == 'POST':
        certificate_number = request.POST.get('certificate_number', '').strip().upper()
        if certificate_number:
            return redirect('verify_certificate', certificate_number=certificate_number)
        messages.error(request, 'Please enter a certificate number.')
    return render(request, 'verification/home.html')


def verify_certificate(request, certificate_number):
    """Display verification results for a certificate number."""
    certificate = Certificate.objects.filter(certificate_number__iexact=certificate_number).first()
    browser = request.META.get('HTTP_USER_AGENT', 'Unknown')
    ip_address = request.META.get('REMOTE_ADDR', 'Unknown')
    if certificate:
        VerificationLog.objects.create(
            certificate=certificate,
            certificate_number=certificate.certificate_number,
            ip_address=ip_address,
            browser=browser,
            status='verified',
        )
        return render(request, 'verification/verify.html', {'certificate': certificate})

    VerificationLog.objects.create(
        certificate_number=certificate_number,
        ip_address=ip_address,
        browser=browser,
        status='invalid',
    )
    return render(request, 'verification/invalid.html', {'certificate_number': certificate_number})
