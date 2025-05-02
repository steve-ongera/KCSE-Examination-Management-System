import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from exam_portal.models import School
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Updates school registration dates to random dates between 1972 and 2009'

    def handle(self, *args, **options):
        # Calculate date range (1972-01-01 to 2009-12-31)
        start_date = datetime(1972, 1, 1).date()
        end_date = datetime(2009, 12, 31).date()
        delta = end_date - start_date
        
        schools = School.objects.all()
        total_schools = schools.count()
        
        self.stdout.write(f"Updating registration dates for {total_schools} schools...")
        
        updated_count = 0
        for school in schools:
            # Generate random days within the range
            random_days = random.randint(0, delta.days)
            new_date = start_date + timedelta(days=random_days)
            
            # Update both registration and established dates
            school.registration_date = new_date
            school.established_date = new_date
            school.save()
            updated_count += 1
            
            # Print progress every 100 schools
            if updated_count % 100 == 0:
                self.stdout.write(f"Updated {updated_count}/{total_schools} schools...")
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated registration dates for {updated_count} schools '
                f'to random dates between {start_date.year} and {end_date.year}'
            )
        )