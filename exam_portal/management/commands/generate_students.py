from django.core.management.base import BaseCommand
from exam_portal.models import Student, School
import random
from datetime import datetime, timedelta
from django.utils import timezone

# Kenyan Names Lists (truncated here for brevity; use your full lists)
# Kenyan first names separated by gender
kenyan_male_first_names = [
            'James', 'John', 'David', 'Michael', 'William', 'Joseph', 'Peter', 'Daniel', 'Paul', 'Mark',
            'Stephen', 'Andrew', 'Kennedy', 'Brian', 'Kevin', 'Thomas', 'Robert', 'Charles', 'Martin', 'Eric',
            'Anthony', 'Patrick', 'George', 'Simon', 'Francis', 'Isaac', 'Victor', 'Samson', 'Elijah', 'Moses',
            'Nicholas', 'Philip', 'Timothy', 'Richard', 'Edward', 'Henry', 'Benjamin', 'Fredrick', 'Dennis', 'Solomon'
]

kenyan_female_first_names = [
            'Mary', 'Elizabeth', 'Susan', 'Margaret', 'Joyce', 'Ann', 'Esther', 'Grace', 'Jane', 'Alice',
            'Dorcas', 'Sarah', 'Ruth', 'Mercy', 'Agnes', 'Lucy', 'Rose', 'Priscilla', 'Irene', 'Gladys',
            'Nancy', 'Christine', 'Beatrice', 'Lilian', 'Caroline', 'Juliet', 'Faith', 'Hannah', 'Naomi', 'Rebecca',
            'Eunice', 'Jackline', 'Martha', 'Edith', 'Terry', 'Winnie', 'Veronica', 'Cynthia', 'Janet', 'Sheila'
        ]

        # Kenyan last names
kenyan_last_names = [
            'Mwangi', 'Maina', 'Kamau', 'Kariuki', 'Njoroge', 'Ochieng', 'Odhiambo', 'Omondi', 'Otieno', 'Owino',
            'Waweru', 'Wafula', 'Wambua', 'Wanyama', 'Were', 'Wambugu', 'Wanjiru', 'Waithaka', 'Wairimu', 'Wangui',
            'Kipchoge', 'Kiplagat', 'Kiptoo', 'Korir', 'Kosgei', 'Langat', 'Mutai', 'Rono', 'Sang', 'Tanui',
            'Chebet', 'Chepkoech', 'Jepkosgei', 'Jepchirchir', 'Jeptoo', 'Kemboi', 'Kiprop', 'Korir', 'Rotich', 'Sum'
]

kenyan_middle_names = [
            'Mwangi', 'Maina', 'Kamau', 'Kariuki', 'Njoroge', 'Ochieng', 'Odhiambo', 'Omondi', 'Otieno', 'Owino',
            'Waweru', 'Wafula', 'Wambua', 'Wanyama', 'Were', 'Wambugu', 'Wanjiru', 'Waithaka', 'Wairimu', 'Wangui',
            'Kipchoge', 'Kiplagat', 'Kiptoo', 'Korir', 'Kosgei', 'Langat', 'Mutai', 'Rono', 'Sang', 'Tanui',
            'Chebet', 'Chepkoech', 'Jepkosgei', 'Jepchirchir', 'Jeptoo', 'Kemboi', 'Kiprop', 'Korir', 'Rotich', 'Sum'
]


# Sample Classes and Counties
classes = ['Form 1', 'Form 2', 'Form 3', 'Form 4']
counties = ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret', 'Kakamega', 'Bungoma', 'Busia', 'Siaya', 'Kisii']
sub_counties = ["Langata", "Embakasi", "Kasarani", "Kisauni", "Naivasha", "Nyali"]

houses = ['Simba', 'Chui', 'Twiga', 'Nyati', 'Tembo', 'Pundamilia']

class Command(BaseCommand):
    help = 'Generate 400 student records'

    def handle(self, *args, **kwargs):
        # Make sure at least one school exists
        school = School.objects.first()
        if not school:
            self.stdout.write(self.style.ERROR('No schools found. Please create a school first.'))
            return
        
        existing_students = Student.objects.count()
        if existing_students >= 400:
            self.stdout.write(self.style.WARNING(f"There are already {existing_students} students. Skipping."))
            return
        
        for i in range(400):
            gender = random.choice(['M', 'F'])
            if gender == 'M':
                first_name = random.choice(kenyan_male_first_names )
            else:
                first_name = random.choice(kenyan_female_first_names )
            
            middle_name = random.choice(kenyan_middle_names)
            last_name = random.choice(kenyan_last_names)
            
            birth_year = random.randint(2004, 2008)
            birth_date = datetime(birth_year, random.randint(1, 12), random.randint(1, 28)).date()

            admission_year = random.randint(2019, 2024)
            admission_date = datetime(admission_year, random.randint(1, 12), random.randint(1, 28)).date()
            
            index_number = f"{random.randint(1000000, 9999999)}/{str(i+1).zfill(3)}/{admission_year}"
            admission_number = f"ADM{random.randint(1000, 9999)}"
            
            phone_number = f"07{random.randint(0, 9)}{random.randint(1000000, 9999999)}"
            postal_address = f"P.O. Box {random.randint(100, 9999)}"
            residential_address = f"{random.choice(sub_counties)}, {random.choice(counties)}"

            kcpe_year = admission_year - 1
            kcpe_marks = random.randint(200, 420)
            kcpe_index = f"{random.randint(100000, 999999)}/{random.randint(1, 500)}"
            
            disability = random.choice(["", "", "Visual Impairment", "Hearing Impairment", "Physical Disability"])
            disability_description = ""
            if disability and disability != "":
                disability_description = f"Has {disability.lower()}."

            student = Student(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                birth_date=birth_date,
                birth_certificate_number=str(random.randint(10000000, 99999999)),
                gender=gender,
                nationality='Kenyan',
                county_of_origin=random.choice(counties),
                sub_county=random.choice(sub_counties),
                passport_photo=None,  # You can set default later
                disability=disability if disability else None,
                disability_description=disability_description if disability else None,
                school=school,
                index_number=index_number,
                admision_number=admission_number,
                admission_date=admission_date,
                current_class=random.choice(classes),
                house=random.choice(houses),
                is_boarder=random.choice([True, False]),
                email=None,
                phone_number=phone_number,
                postal_address=postal_address,
                residential_address=residential_address,
                previous_school="Primary School " + random.choice(["Academy", "Centre", "Primary"]),
                kcpe_year=kcpe_year,
                kcpe_index=kcpe_index,
                kcpe_marks=kcpe_marks,
                is_active=True
            )
            student.save()
        
        self.stdout.write(self.style.SUCCESS('Successfully created 400 students.'))

