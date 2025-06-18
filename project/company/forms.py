from django import forms
from .models import Company_details

class CompanyRegistrationForm(forms.ModelForm):
    class Meta:
        model = Company_details
        fields = [
            'company_name', 'description', 
            'company_equity_percentage',
            'valuation',
            'profit_year_3', 'profit_year_2', 'profit_year_1',
            'revenue_year_3', 'revenue_year_2', 'revenue_year_1',
            'office_address', 'government_certificate',
            'last_year_revenue', 'last_year_profit',
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Make certificate required
        self.fields['government_certificate'].required = True
        self.fields['government_certificate'].help_text = "Please upload a valid government certificate (PDF, JPG, PNG)"
        
    def clean_government_certificate(self):
        certificate = self.cleaned_data.get('government_certificate')
        if not certificate:
            raise forms.ValidationError("Government certificate is required")
        
        # Check file type
        if certificate:
            if not certificate.content_type in ['application/pdf', 'image/jpeg', 'image/png']:
                raise forms.ValidationError("Only PDF, JPG, and PNG files are allowed")
            
            # Check file size (max 5MB)
            if certificate.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size must be less than 5MB")
        
        return certificate