"""Views for certificate CRUD, public download, and email delivery."""

from io import BytesIO

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .forms import CertificateForm
from .models import Certificate


def certificate_add(request):
    """Create a new certificate and generate its QR code and PDF."""
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            certificate = form.save()
            generate_pdf(certificate)
            messages.success(request, 'Certificate created successfully.')
            return redirect('certificate_list')
    else:
        form = CertificateForm()
    return render(request, 'certificates/form.html', {'form': form, 'title': 'Add Certificate'})


@login_required
def certificate_list(request):
    """List all certificates with search support."""
    query = request.GET.get('q', '')
    certificates = Certificate.objects.all().order_by('-created_at')
    if query:
        certificates = certificates.filter(certificate_number__icontains=query) | certificates.filter(intern_name__icontains=query) | certificates.filter(course_domain__icontains=query)
    return render(request, 'certificates/list.html', {'certificates': certificates, 'query': query})


@login_required
def certificate_edit(request, pk):
    """Edit an existing certificate."""
    certificate = get_object_or_404(Certificate, pk=pk)
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES, instance=certificate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Certificate updated successfully.')
            return redirect('certificate_list')
    else:
        form = CertificateForm(instance=certificate)
    return render(request, 'certificates/form.html', {'form': form, 'title': 'Edit Certificate'})


@login_required
def certificate_delete(request, pk):
    """Delete a certificate."""
    certificate = get_object_or_404(Certificate, pk=pk)
    certificate.delete()
    messages.success(request, 'Certificate deleted successfully.')
    return redirect('certificate_list')


def download_certificate(request, certificate_number):
    """Serve a generated PDF for public download."""
    certificate = get_object_or_404(Certificate, certificate_number=certificate_number)
    if not certificate.certificate_pdf:
        generate_pdf(certificate)
    return HttpResponse(certificate.certificate_pdf.read(), content_type='application/pdf')


def email_certificate(request, certificate_number):
    """Email the certificate PDF to the student."""
    certificate = get_object_or_404(Certificate, certificate_number=certificate_number)
    if not certificate.certificate_pdf:
        generate_pdf(certificate)
    subject = f'Your Durion Technologies Certificate - {certificate.certificate_number}'
    message = 'Please find your certificate attached.'
    email = EmailMessage(subject, message, to=['student@example.com'])
    email.attach_file(certificate.certificate_pdf.path)
    email.send()
    messages.success(request, 'Certificate emailed successfully.')
    return redirect('certificate_list')


def generate_pdf(certificate):
    """Generate a polished certificate as a PDF file."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.fontName = 'Helvetica-Bold'
    title_style.fontSize = 24
    title_style.textColor = colors.HexColor('#0b4f8a')

    story = []
    story.append(Paragraph('Durion Technologies', title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph('Certificate of Completion', styles['Heading1']))
    story.append(Spacer(1, 12))
    data = [
        ['Intern Name', certificate.intern_name],
        ['Internship ID', certificate.internship_id or 'N/A'],
        ['Course / Domain', certificate.course_domain],
        ['Duration', certificate.internship_duration],
        ['Start Date', certificate.start_date],
        ['End Date', certificate.end_date],
        ['Completion Date', certificate.completion_date],
        ['Performance Grade', certificate.performance_grade or 'N/A'],
        ['Mentor Name', certificate.mentor_name],
        ['Company Name', certificate.company_name],
        ['Certificate Number', certificate.certificate_number],
    ]
    table = Table(data, colWidths=[140, 300])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f4f8fc')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#0b1f3a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#0b4f8a')),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
    ]))
    story.append(table)
    doc.build(story)
    buffer.seek(0)
    certificate.certificate_pdf.save(f'{certificate.certificate_number}.pdf', ContentFile(buffer.read()), save=True)
