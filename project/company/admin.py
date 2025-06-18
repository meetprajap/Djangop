from django.contrib import admin
from .models import Company_details
from django.contrib import messages

@admin.register(Company_details)
class CompanyDetailsAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'entrepreneur', 'valuation', 'company_equity_percentage', 'created_at')
    search_fields = ('company_name', 'entrepreneur__username')
    list_filter = ('created_at',)
    
    actions = ['delete_all_companies']
    
    def delete_all_companies(self, request, queryset):
        # Delete all companies
        Company_details.objects.all().delete()
        self.message_user(request, "All companies have been deleted successfully.", messages.SUCCESS)
    
    delete_all_companies.short_description = "Delete all companies from database"
