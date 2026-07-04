"""Dashboard views for statistics, recent activity, and Excel export."""

import datetime as dt

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from openpyxl import Workbook

from certificates.models import Certificate, VerificationLog


@login_required
def dashboard_home(request):
    """Render analytics cards, recent certificates, and recent verification log entries."""
    total_certificates = Certificate.objects.count()
    today = dt.date.today()
    today_verifications = VerificationLog.objects.filter(verification_time__date=today).count()
    downloads = Certificate.objects.exclude(certificate_pdf='').count()
    recent_certificates = Certificate.objects.order_by('-created_at')[:5]
    recent_logs = VerificationLog.objects.order_by('-verification_time')[:5]
    return render(request, 'dashboard/index.html', {
        'total_certificates': total_certificates,
        'today_verifications': today_verifications,
        'downloads': downloads,
        'recent_certificates': recent_certificates,
        'recent_logs': recent_logs,
    })


@login_required
def export_certificates_excel(request):
    """Export all certificates to an Excel workbook."""
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="certificates.xlsx"'
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Certificates'
    sheet.append(['Certificate Number', 'Intern Name', 'Course / Domain', 'Mentor Name', 'Start Date', 'End Date', 'Completion Date', 'Performance Grade', 'Status'])
    for certificate in Certificate.objects.all():
        sheet.append([
            certificate.certificate_number,
            certificate.intern_name,
            certificate.course_domain,
            certificate.mentor_name,
            certificate.start_date,
            certificate.end_date,
            certificate.completion_date,
            certificate.performance_grade or 'N/A',
            certificate.status,
        ])
    workbook.save(response)
    return response
