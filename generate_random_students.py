#!/usr/bin/env python
# Script to generate random students for schools that don't have any
# Run with: python manage.py shell < generate_random_students.py

import os
import sys
import django
import random
from datetime import date, timedelta
from django.db.models import Count

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_portal.settings')
django.setup()

# Import models
from django.apps import apps
School = apps.get_model('exam_portal', 'School')
Student = apps.get_model('exam_portal', 'Student')

# Function to generate a random date within a range
def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

# Function to generate a random Kenyan county
def random_county():
    counties = [
        "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Uasin Gishu", "Kiambu",
        "Machakos", "Kajiado", "Bungoma", "Kakamega", "Kilifi", "Nyeri",
        "Meru", "Embu", "Kisii", "Siaya", "Nandi"
    ]
    return random.choice(counties)

# Function to generate a random sub-county
def random_sub_county(county):
    sub_counties = {
        "Nairobi": ["Westlands", "Dagoretti", "Langata", "Kibra", "Roysambu", "Kasarani", "Ruaraka", "Embakasi"],
        "Mombasa": ["Mvita", "Nyali", "Kisauni", "Likoni", "Changamwe", "Jomvu"],
        "Kisumu": ["Kisumu Central", "Kisumu East", "Kisumu West", "Seme", "Nyando", "Muhoroni"],
        "Nakuru": ["Nakuru Town East", "Nakuru Town West", "Naivasha", "Gilgil", "Molo", "Njoro"],
        "Uasin Gishu": ["Ainabkoi", "Kapseret", "Kesses", "Moiben", "Soy", "Turbo"],
        "Kiambu": ["Juja", "Thika", "Ruiru", "Kikuyu", "Limuru", "Kiambu", "Gatundu"],
        "Machakos": ["Machakos Town", "Athi River", "Kangundo", "Kathiani", "Matungulu", "Mwala"],
        "Kajiado": ["Kajiado Central", "Kajiado North", "Kajiado East", "Kajiado West", "Kajiado South"],
        "Bungoma": ["Bungoma South", "Bungoma North", "Bungoma East", "Bungoma West", "Mt Elgon"],
        "Kakamega": ["Kakamega Central", "Kakamega South", "Kakamega East", "Kakamega North", "Lurambi"],
        "Kilifi": ["Kilifi North", "Kilifi South", "Malindi", "Magarini", "Kaloleni", "Rabai"],
        "Nyeri": ["Nyeri Central", "Nyeri South", "Mathira", "Kieni", "Mukurweini", "Tetu"],
        "Meru": ["North Imenti", "South Imenti", "Central Imenti", "Buuri", "Igembe", "Tigania"],
        "Embu": ["Manyatta", "Runyenjes", "Mbeere North", "Mbeere South"],
        "Kisii": ["Kisii Central", "Kisii South", "Kitutu Chache", "Nyaribari", "Bomachoge"],
        "Siaya": ["Gem", "Ugenya", "Ugunja", "Alego", "Bondo", "Rarieda"],
        "Nandi": ["Nandi Hills", "Aldai", "Chesumei", "Nandi Central", "Tinderet"]
    }
    return random.choice(sub_counties.get(county, ["Central", "North", "South", "East", "West"]))

# Function to generate a random KCSE index number
def generate_index_number(school, year):
    school_code = school.knec_code
    existing_students_count = Student.objects.filter(school=school).count()
    student_number = f"{existing_students_count + 1:03d}"
    return f"{school_code}/{student_number}/{year}"

# Function to generate a random admission number
def generate_admission_number(existing_admissions):
    while True:
        admission = f"ADM/{random.randint(1000, 9999)}/{random.randint(2020, 2025)}"
        if admission not in existing_admissions:
            return admission

# Generate random students for schools without any
def generate_students():
    current_year = date.today().year
    
    # Get all schools with a count of students
    schools = School.objects.annotate(student_count=Count('students'))
    
    print(f"Checking {schools.count()} schools for students...")
    
    for school in schools:
        if school.student_count == 0:
            # This school has no students, let's create some
            num_students = random.randint(15, 28)
            print(f"Generating {num_students} students for {school.name} ({school.knec_code})")
            
            # Store existing admission numbers for this school to avoid duplicates
            existing_admissions = set()
            
            for i in range(num_students):
                # Generate random student data
                gender = random.choice(['M', 'F'])
                
                # First names lists by gender
                male_names = ["James", "John", "Peter", "David", "Samuel", "Daniel", "Michael", 
                             "Joseph", "Robert", "William", "Charles", "Thomas", "George", "Moses",
                             "Kenneth", "Paul", "Andrew", "Joshua", "Stephen", "Richard"]
                
                female_names = ["Mary", "Elizabeth", "Sarah", "Catherine", "Jane", "Rachel", "Ruth",
                               "Rebecca", "Esther", "Grace", "Faith", "Joyce", "Anne", "Margaret",
                               "Mercy", "Linda", "Susan", "Stella", "Diana", "Irene"]
                
                # Last names (for both genders)
                last_names = ["Mwangi", "Kamau", "Ochieng", "Otieno", "Wanjiku", "Njoroge", "Kimani",
                             "Owino", "Maina", "Kariuki", "Ouma", "Wanjiru", "Ndungu", "Ogola", "Muthoni",
                             "Kinyua", "Gathoni", "Mutua", "Auma", "Njeri", "Wambui", "Onyango"]
                
                first_name = random.choice(male_names if gender == 'M' else female_names)
                middle_name = random.choice(male_names if gender == 'M' else female_names)
                last_name = random.choice(last_names)
                
                # Generate birth date (for students between 15-20 years old)
                today = date.today()
                start_date = date(today.year - 20, 1, 1)
                end_date = date(today.year - 15, 12, 31)
                birth_date = random_date(start_date, end_date)
                
                # Generate county and sub-county
                county = random_county()
                sub_county = random_sub_county(county)
                
                # Generate school-related info
                index_number = generate_index_number(school, current_year)
                admission_num = generate_admission_number(existing_admissions)
                existing_admissions.add(admission_num)
                
                # Generate admission date (1-4 years ago)
                admission_start = date(today.year - 4, 1, 1)
                admission_end = date(today.year - 1, 12, 31)
                admission_date = random_date(admission_start, admission_end)
                
                # Generate KCPE info
                kcpe_year = admission_date.year - 1
                kcpe_marks = random.randint(250, 420)
                kcpe_index = f"{random.randint(10000, 99999)}/{kcpe_year}"
                
                # Determine current class based on admission date
                years_difference = today.year - admission_date.year
                current_class = f"Form {min(4, years_difference + 1)}"
                
                # Create the student
                student = Student(
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    birth_date=birth_date,
                    birth_certificate_number=f"BC{random.randint(100000, 999999)}",
                    gender=gender,
                    nationality="Kenyan",
                    county_of_origin=county,
                    sub_county=sub_county,
                    school=school,
                    index_number=index_number,
                    admision_number=admission_num,
                    admission_date=admission_date,
                    current_class=current_class,
                    is_boarder=bool(random.getrandbits(1)),
                    email=f"{first_name.lower()}.{last_name.lower()}@example.com" if random.random() > 0.3 else None,
                    phone_number=f"07{random.randint(10000000, 99999999)}" if random.random() > 0.5 else None,
                    previous_school=f"{random.choice(['St.', 'Holy', 'Green', 'Central', 'County'])} {random.choice(['Primary', 'Elementary'])} School",
                    kcpe_year=kcpe_year,
                    kcpe_index=kcpe_index,
                    kcpe_marks=kcpe_marks,
                )
                student.save()
                
            print(f"Successfully created {num_students} students for {school.name}")
        else:
            print(f"{school.name} already has {school.student_count} students. Skipping.")
    
    print("Student generation complete!")

# Run the function
if __name__ == "__main__":
    generate_students()