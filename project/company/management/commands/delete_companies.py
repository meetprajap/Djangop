from django.core.management.base import BaseCommand
from company.models import Company_details
from investor.models import Investment

class Command(BaseCommand):
    help = 'Deletes all company data and related investments from the database'

    def handle(self, *args, **options):
        # First delete all investments to handle foreign key relationships
        investment_count = Investment.objects.count()
        Investment.objects.all().delete()
        
        # Then delete all companies
        company_count = Company_details.objects.count()
        Company_details.objects.all().delete()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully deleted {company_count} companies and {investment_count} investments'
            )
        ) 