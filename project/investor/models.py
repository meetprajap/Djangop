from django.db import models
from django.conf import settings
from company.models import Company_details

# Create your models here.

class Investment(models.Model):
    investor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='investments')
    company = models.ForeignKey(Company_details, on_delete=models.CASCADE, related_name='investments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    equity_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    original_valuation = models.DecimalField(max_digits=15, decimal_places=2, default=0)
 # Store valuation at time of investment
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='pending')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.investor.username}'s investment in {self.company.company_name}"
