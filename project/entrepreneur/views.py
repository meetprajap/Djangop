from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from company.models import Company_details
from company.forms import CompanyRegistrationForm
from django.db.models import Sum
from investor.models import Investment

# Create your views here.

def login(request):
  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Add detailed debug messages
        print(f"Login attempt - Username: {username}")
        print(f"POST data: {request.POST}")  # Print all POST data
        
        # Check if user exists
        try:
            user_exists = CustomUser.objects.filter(username=username).exists()
            print(f"User exists in database: {user_exists}")
            if user_exists:
                user_obj = CustomUser.objects.get(username=username)
                print(f"User type: {user_obj.user_type}")
        except Exception as e:
            print(f"Error checking user existence: {e}")
        
        user = authenticate(request, username=username, password=password)
        print(f"Authentication result: {user}")  # Print the authentication result
        
        if user is not None:
            auth_login(request, user)
            print(f"User authenticated successfully. User type: {user.user_type}")
            # Check user type and redirect accordingly
            if user.user_type == 'entrepreneur':
                if user.first_login:  # Check if first login
                    user.first_login = False  # Mark it as executed
                    user.save()
                    request.session['_auth_user_id'] = user.pk
                    request.session.modified = True
                    return redirect('company_registration') 
                return redirect('entrepreneur_home')
            elif user.user_type == 'investor':
                return redirect('investor_home')
            else:
                messages.error(request, 'Invalid user type.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password. Please check your credentials.')
            print("Authentication failed - user is None")
            # Try to get user to check password hash
            try:
                user = CustomUser.objects.get(username=username)
                print("User found in database but authentication failed - possible password mismatch")
            except CustomUser.DoesNotExist:
                print("User not found in database")
            except Exception as e:
                print(f"Error during user lookup: {e}")
    
    return render(request, 'entrepreneur/login.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(f"Registration form data: {request.POST}")  # Print registration data
        if form.is_valid():
            user = form.save()
            print(f"User registered successfully: {user.username}, type: {user.user_type}")
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        else:
            print(f"Form errors: {form.errors}")  # Print form errors
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def entrepreneur_home(request):
    if request.user.user_type != 'entrepreneur':
        return redirect('investor_home')
    
    # Get the first company registered by the entrepreneur
    try:
        company = Company_details.objects.filter(entrepreneur=request.user).order_by('created_at').first()
        
        if company:
            # Get investments for the company
            investments = Investment.objects.filter(company=company).select_related('investor')
            total_investment = investments.aggregate(total=Sum('amount'))['total'] or 0
            
            # Calculate remaining equity
            remaining_equity = company.company_equity_percentage - sum(inv.equity_percentage for inv in investments)
            
            # Get total balance (available balance + total investments)
            total_balance = request.user.balance + total_investment
            
            context = {
                'company': company,
                'investments': investments,
                'total_investment': total_investment,
                'remaining_equity': remaining_equity,
                'total_balance': total_balance
            }
            
            return render(request, 'entrepreneur/home.html', context)
        else:
            # If no company exists, redirect to company registration
            messages.info(request, 'Please register your company first.')
            return redirect('company_registration')
            
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('company_registration')

    # return render(request, 'entrepreneur/home.html', {
    #     'user': request.user,
    #     'company': company
    # })
    
