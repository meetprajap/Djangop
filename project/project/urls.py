"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from entrepreneur import views as entrepreneur_views
from investor import views as investor_views
from company import views as company_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', entrepreneur_views.login, name='login'),
    path('register/', entrepreneur_views.register, name='register'),
    path('logout/', entrepreneur_views.logout_view, name='logout'),
    path('entrepreneur/home/', entrepreneur_views.entrepreneur_home, name='entrepreneur_home'),
    path('investor/home/', investor_views.investor_home, name='investor_home'),
    path('investor/add-funds/', investor_views.add_funds, name='add_funds'),
    path('investor/my-investments/', investor_views.my_investments, name='my_investments'),
    path('company/register/', company_views.company_registration, name='company_registration'),
    path('company/<int:company_id>/', investor_views.company_detail_view, name='company_detail'),
    path('company/<int:company_id>/invest/', investor_views.make_investment, name='make_investment'),
    path('contact/', investor_views.contact_view, name='contact'),
    path('contact/submit/', investor_views.contact_submit, name='contact_submit'),
    path('company/<int:company_id>/update/', company_views.update_company, name='update_company'),
    path('investment/<int:investment_id>/divest/', investor_views.divest_investment, name='divest_investment'),
    
    # # Company management URLs
    # path('company/edit/', company_views.edit_company, name='edit_company'),
    # path('company/<int:company_id>/', company_views.company_detail, name='company_detail'),
    # path('company/investment/accept/<int:request_id>/', company_views.accept_investment, name='accept_investment'),
    # path('company/investment/reject/<int:request_id>/', company_views.reject_investment, name='reject_investment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
