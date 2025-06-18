from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CompanyRegistrationForm
from .models import Company_details

@login_required
def company_registration(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.entrepreneur = request.user
            company.save()
            messages.success(request, 'Company registration successful!')
            return redirect('entrepreneur_home')
    else:
        form = CompanyRegistrationForm()
    
    return render(request, 'register_company.html', {'form': form})

@login_required
def update_company(request, company_id):
    company = get_object_or_404(Company_details, id=company_id, entrepreneur=request.user)
    
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company details updated successfully!')
            return redirect('entrepreneur_home')
    else:
        form = CompanyRegistrationForm(instance=company)
    
    return render(request, 'update_company.html', {'form': form, 'company': company})