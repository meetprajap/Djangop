from django.db import models
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout

class Company_details(models.Model):
    entrepreneur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='companies',
        limit_choices_to={'user_type': 'entrepreneur'}
    )
    company_name = models.CharField(max_length=200)
    description = models.TextField()
    last_year_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    last_year_profit = models.DecimalField(max_digits=15, decimal_places=2)
    # revenue_year_5 = models.DecimalField(max_digits=15, decimal_places=2)
    # revenue_year_4 = models.DecimalField(max_digits=15, decimal_places=2)
    revenue_year_3 = models.DecimalField(max_digits=15, decimal_places=2)
    revenue_year_2 = models.DecimalField(max_digits=15, decimal_places=2)
    revenue_year_1 = models.DecimalField(max_digits=15, decimal_places=2)
    # profit_year_5 = models.DecimalField(max_digits=15, decimal_places=2)
    # profit_year_4 = models.DecimalField(max_digits=15, decimal_places=2)
    valuation = models.DecimalField(max_digits=15, decimal_places=2) 
    company_equity_percentage = models.DecimalField(max_digits=15, decimal_places=2)
    profit_year_3 = models.DecimalField(max_digits=15, decimal_places=2)
    profit_year_2 = models.DecimalField(max_digits=15, decimal_places=2)
    profit_year_1 = models.DecimalField(max_digits=15, decimal_places=2)
    office_address = models.TextField()
    government_certificate = models.FileField(upload_to='certificates/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')