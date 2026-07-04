"""Form classes for internship certificate management."""

from django import forms

from .models import Certificate


class CertificateForm(forms.ModelForm):
    """Handles internship certificate CRUD forms with validation."""

    class Meta:
        model = Certificate
        fields = [
            'certificate_number',
            'intern_name',
            'internship_id',
            'course_domain',
            'internship_duration',
            'start_date',
            'end_date',
            'completion_date',
            'performance_grade',
            'mentor_name',
            'company_name',
            'status',
            'student_photo',
            'certificate_pdf',
            'certificate_template',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_certificate_number(self):
        value = self.cleaned_data.get('certificate_number', '').strip().upper()
        return value
