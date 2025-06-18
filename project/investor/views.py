from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, F
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
import json
from decimal import Decimal
from company.models import Company_details
from .models import Investment

# Create your views here.

@login_required
@require_POST
@csrf_protect
def add_funds(request):
    try:
        data = json.loads(request.body)
        amount = Decimal(str(data.get('amount', 0)))
        
        if amount < 1000:
            return JsonResponse({'success': False, 'error': 'Minimum amount is ₹1,000'})
        
        # Update user's available amount
        request.user.available_amount = F('available_amount') + amount
        request.user.save()
        request.user.refresh_from_db()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def investor_home(request):
    # Get user's investments
    investments = Investment.objects.filter(investor=request.user).select_related('company')
    total_invested = investments.aggregate(total=Sum('amount'))['total'] or 0
    
    # Get available companies for investment
    companies = Company_details.objects.all()
    
    context = {
        'investments': investments,
        'total_invested': total_invested,
        'companies': companies,
    }
    return render(request, 'investor/home.html', context)

@login_required
def company_detail_view(request, company_id):
    company = get_object_or_404(Company_details, id=company_id)
    
    # Get total invested amount and equity for this company
    investments = Investment.objects.filter(company=company)
    total_invested = investments.aggregate(total=Sum('amount'))['total'] or 0
    total_equity = investments.aggregate(total=Sum('equity_percentage'))['total'] or 0
    
    # Calculate remaining equity and investment required
    remaining_equity = company.company_equity_percentage - total_equity
    investment_required = (company.valuation * remaining_equity) / 100
    
    # Calculate revenue growth
    revenue_growth_1 = calculate_growth(company.revenue_year_2, company.revenue_year_1)
    revenue_growth_2 = calculate_growth(company.revenue_year_3, company.revenue_year_2)
    
    # Calculate profit margin
    profit_margin = (company.profit_year_1 / company.revenue_year_1 * 100) if company.revenue_year_1 else 0
    
    context = {
        'company': company,
        'investment_required': investment_required,
        'remaining_equity': remaining_equity,
        'total_invested': total_invested,
        'revenue_growth_1': revenue_growth_1,
        'revenue_growth_2': revenue_growth_2,
        'profit_margin': profit_margin,
    }
    return render(request, 'investor/company_detail.html', context)

@login_required
@require_POST
@csrf_protect
def make_investment(request, company_id):
    try:
        data = json.loads(request.body)
        amount = Decimal(str(data.get('amount', 0)))
        company = get_object_or_404(Company_details, id=company_id)
        
        # Validate investment amount
        investment_required = company.valuation * (company.company_equity_percentage / 100)
        if amount <= 0 or amount > investment_required:
            return JsonResponse({'success': False, 'error': 'Invalid investment amount'})
            
        # Check if user has sufficient funds
        if amount > request.user.available_amount:
            return JsonResponse({'success': False, 'error': 'Insufficient funds'})
        
        # Calculate equity percentage for this investment
        equity_percentage = (amount / company.valuation) * 100

        
        # Start transaction to ensure data consistency
        with transaction.atomic():
            # Create investment
            investment = Investment.objects.create(
                investor=request.user,
                company=company,
                amount=amount,
                equity_percentage=equity_percentage
            )
            
            # Deduct amount from investor's available amount
            request.user.available_amount = F('available_amount') - amount
            request.user.save()
            
            # Add amount to entrepreneur's balance
            entrepreneur = company.entrepreneur
            entrepreneur.balance = F('balance') + amount
            entrepreneur.save()
            Investment.original_valuation = company.valuation
            
            # Refresh user instances to get updated values
            request.user.refresh_from_db()
            entrepreneur.refresh_from_db()
        
        return JsonResponse({
            'success': True,
            'message': 'Investment successful!',
            'new_balance': float(request.user.available_amount)
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def calculate_growth(old_value, new_value):
    if old_value and old_value != 0:
        return ((new_value - old_value) / old_value) * 100
    return 0

@login_required
def my_investments(request):
    investments = Investment.objects.filter(investor=request.user).select_related('company')
    total_invested = investments.aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'investments': investments,
        'total_invested': total_invested,
    }
    return render(request, 'investor/my_investments.html', context)

def contact_view(request):
    return render(request, 'contact.html')

@require_POST
def contact_submit(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
        
        # Here you can add code to save the contact form data to your database
        # or send an email to your support team
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def divest_investment(request, investment_id):
    investment = get_object_or_404(Investment, id=investment_id, investor=request.user)
    company = investment.company
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Calculate return amount based on original valuation
                return_amount = (investment.original_valuation * investment.equity_percentage) / 100
                
                # Add return amount to user's available balance
                request.user.available_amount = F('available_amount') + return_amount
                request.user.save()
                
                # Add equity back to company
                company.company_equity_percentage = F('company_equity_percentage') + investment.equity_percentage
                company.save()
                
                # Delete the investment
                investment.delete()
                
                messages.success(request, f'Successfully divested investment. ₹{return_amount:,.2f} has been added to your Investment Wallet.')
                return redirect('my_investments')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('my_investments')
    
    # Calculate return amount based on original valuation for display
    return_amount = (investment.original_valuation * investment.equity_percentage) / 100
    profit_loss = return_amount - investment.amount
    
    context = {
        'investment': investment,
        'company': company,
        'return_amount': return_amount,
        'profit_loss': profit_loss
    }
    return render(request, 'investor/divest_investment.html', context)

@login_required
def invest_in_company(request, company_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = Decimal(data.get('amount', 0))
            company = get_object_or_404(Company_details, id=company_id)
            
            # Calculate equity percentage based on investment amount and company valuation
            equity_percentage = (amount / company.valuation) * 100
            
            # Create investment record with original valuation
            investment = Investment.objects.create(
                investor=request.user,
                company=company,
                amount=amount,
                equity_percentage=equity_percentage,
                original_valuation=company.valuation  # Store original valuation
            )
            
            # Update company's remaining equity
            company.company_equity_percentage -= equity_percentage
            company.save()
            
            # Update user's available amount
            request.user.available_amount -= amount
            request.user.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})