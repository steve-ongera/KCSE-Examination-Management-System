"""
Script to populate the database with Kenyan schools.
Run this in the Django shell:
python manage.py shell < this_script.py
or copy and paste into the shell.
"""

import random
from datetime import date, timedelta
from django.utils import timezone
from exam_portal.models import School

# Helper functions to generate realistic data
def random_date(start_year=1950, end_year=2010):
    """Generate a random date between start_year and end_year."""
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

def random_phone():
    """Generate a random Kenyan phone number."""
    prefixes = ['0700', '0710', '0720', '0730', '0740', '0750', '0760', '0770', '0780', '0790', '0110', '0111', '0112']
    return f"{random.choice(prefixes)}{random.randint(100000, 999999)}"

def random_email(name):
    """Generate a random email based on school name."""
    domains = ['gmail.com', 'yahoo.com', 'education.go.ke', 'school.co.ke', 'hotmail.com']
    school_part = name.lower().replace(' ', '').replace("'", "")[:10]
    return f"{school_part}@{random.choice(domains)}"

def random_tsc_number():
    """Generate a random TSC number for teachers."""
    return f"TSC/{random.randint(10000, 99999)}/{random.randint(10, 99)}"

def random_knec_code():
    """Generate a random KNEC code."""
    return f"{random.randint(10000, 99999)}"

def random_registration_number():
    """Generate a random school registration number."""
    return f"SC-{random.randint(1000, 9999)}-{random.randint(10, 99)}"

def random_gps():
    """Generate random GPS coordinates in Kenya."""
    # Kenya's approximate latitude and longitude ranges
    lat = random.uniform(-4.67, 5.72)
    lng = random.uniform(33.9, 41.9)
    return f"{lat:.6f}, {lng:.6f}"

# List of Kenyan counties
counties = [
    "Mombasa", "Kwale", "Kilifi", "Tana River", "Lamu", "Taita Taveta", "Garissa", 
    "Wajir", "Mandera", "Marsabit", "Isiolo", "Meru", "Tharaka-Nithi", "Embu", 
    "Kitui", "Machakos", "Makueni", "Nyandarua", "Nyeri", "Kirinyaga", "Murang'a", 
    "Kiambu", "Turkana", "West Pokot", "Samburu", "Trans-Nzoia", "Uasin Gishu", 
    "Elgeyo-Marakwet", "Nandi", "Baringo", "Laikipia", "Nakuru", "Narok", "Kajiado", 
    "Kericho", "Bomet", "Kakamega", "Vihiga", "Bungoma", "Busia", "Siaya", "Kisumu", 
    "Homa Bay", "Migori", "Kisii", "Nyamira", "Nairobi"
]

# Sample school mottos
mottos = [
    "Education is the key to success", 
    "Excellence through determination",
    "Knowledge is power",
    "Strive to achieve",
    "Forward ever, backward never",
    "Discipline is our foundation",
    "Through hardship to the stars",
    "Unity in diversity",
    "Learning today, leading tomorrow",
    "Striving for excellence",
    "Hard work pays",
    "Wisdom and knowledge"
]

# Sample school list with various types and categories
kenyan_schools = [
    # National Schools
    {"name": "Alliance High School", "type": "NATIONAL", "category": "BOYS", "county": "Kiambu"},
    {"name": "Alliance Girls High School", "type": "NATIONAL", "category": "GIRLS", "county": "Kiambu"},
    {"name": "Kenya High School", "type": "NATIONAL", "category": "GIRLS", "county": "Nairobi"},
    {"name": "Starehe Boys' Centre", "type": "NATIONAL", "category": "BOYS", "county": "Nairobi"},
    {"name": "Moi Girls' High School Eldoret", "type": "NATIONAL", "category": "GIRLS", "county": "Uasin Gishu"},
    {"name": "Moi High School Kabarak", "type": "NATIONAL", "category": "MIXED", "county": "Nakuru"},
    {"name": "Maseno School", "type": "NATIONAL", "category": "BOYS", "county": "Kisumu"},
    {"name": "Precious Blood Riruta", "type": "NATIONAL", "category": "GIRLS", "county": "Nairobi"},
    {"name": "Mangu High School", "type": "NATIONAL", "category": "BOYS", "county": "Kiambu"},
    {"name": "Maryhill Girls High School", "type": "NATIONAL", "category": "GIRLS", "county": "Kiambu"},
    {"name": "Lenana School", "type": "NATIONAL", "category": "BOYS", "county": "Nairobi"},
    {"name": "Nairobi School", "type": "NATIONAL", "category": "BOYS", "county": "Nairobi"},
    {"name": "Moi Forces Academy", "type": "NATIONAL", "category": "MIXED", "county": "Nairobi"},
    {"name": "Friends School Kamusinga", "type": "NATIONAL", "category": "BOYS", "county": "Bungoma"},
    {"name": "Nakuru High School", "type": "NATIONAL", "category": "BOYS", "county": "Nakuru"},
    
    # Extra County Schools
    {"name": "Nyeri High School", "type": "EXTRA_COUNTY", "category": "BOYS", "county": "Nyeri"},
    {"name": "St. Mary's Yala", "type": "EXTRA_COUNTY", "category": "BOYS", "county": "Siaya"},
    {"name": "Kakamega High School", "type": "EXTRA_COUNTY", "category": "BOYS", "county": "Kakamega"},
    {"name": "Lugulu Girls High School", "type": "EXTRA_COUNTY", "category": "GIRLS", "county": "Bungoma"},
    {"name": "Kapsabet Boys High School", "type": "EXTRA_COUNTY", "category": "BOYS", "county": "Nandi"},
    {"name": "Butere Girls High School", "type": "EXTRA_COUNTY", "category": "GIRLS", "county": "Kakamega"},
    {"name": "Kisii School", "type": "EXTRA_COUNTY", "category": "BOYS", "county": "Kisii"},
    {"name": "Nakuru Day Secondary School", "type": "EXTRA_COUNTY", "category": "MIXED", "county": "Nakuru"},
    {"name": "Naivasha Girls Secondary School", "type": "EXTRA_COUNTY", "category": "GIRLS", "county": "Nakuru"},
    {"name": "Oloolaiser High School", "type": "EXTRA_COUNTY", "category": "MIXED", "county": "Kajiado"},
    {"name": "Kapenguria Boys High School", "type": "EXTRA_COUNTY", "category": "BOYS", "county": "West Pokot"},
    
    # Public Schools
    {"name": "Mwiki Secondary School", "type": "PUBLIC", "category": "MIXED", "county": "Nairobi"},
    {"name": "Kayole South Secondary School", "type": "PUBLIC", "category": "MIXED", "county": "Nairobi"},
    {"name": "Dagoretti High School", "type": "PUBLIC", "category": "BOYS", "county": "Nairobi"},
    {"name": "Ngong Township Secondary School", "type": "PUBLIC", "category": "MIXED", "county": "Kajiado"},
    {"name": "Kisumu Girls High School", "type": "PUBLIC", "category": "GIRLS", "county": "Kisumu"},
    {"name": "Nyabururu Girls High School", "type": "PUBLIC", "category": "GIRLS", "county": "Kisii"},
    {"name": "Kitui High School", "type": "PUBLIC", "category": "MIXED", "county": "Kitui"},
    {"name": "Mumias Muslim Secondary School", "type": "PUBLIC", "category": "MIXED", "county": "Kakamega"},
    {"name": "Nanyuki High School", "type": "PUBLIC", "category": "MIXED", "county": "Laikipia"},
    {"name": "Nkubu High School", "type": "PUBLIC", "category": "MIXED", "county": "Meru"},
    {"name": "Kapkenda Girls High School", "type": "PUBLIC", "category": "GIRLS", "county": "Elgeyo-Marakwet"},
    {"name": "Siakago Boys High School", "type": "PUBLIC", "category": "BOYS", "county": "Embu"},
    {"name": "Kangaru School", "type": "PUBLIC", "category": "BOYS", "county": "Embu"},
    {"name": "Kaaga Boys High School", "type": "PUBLIC", "category": "BOYS", "county": "Meru"},
    
    # Private Schools
    {"name": "Brookhouse School", "type": "PRIVATE", "category": "MIXED", "county": "Nairobi"},
    {"name": "St. Andrew's School, Turi", "type": "PRIVATE", "category": "MIXED", "county": "Nakuru"},
    {"name": "Hillcrest School", "type": "PRIVATE", "category": "MIXED", "county": "Nairobi"},
    {"name": "Braeburn School", "type": "PRIVATE", "category": "MIXED", "county": "Nairobi"},
    {"name": "Greenfields School", "type": "PRIVATE", "category": "MIXED", "county": "Nairobi"},
    {"name": "Oshwal Academy", "type": "PRIVATE", "category": "MIXED", "county": "Mombasa"},
    {"name": "Light Academy", "type": "PRIVATE", "category": "MIXED", "county": "Nairobi"},
    {"name": "Riara Springs Girls High School", "type": "PRIVATE", "category": "GIRLS", "county": "Nairobi"},
    {"name": "Moi Educational Centre", "type": "PRIVATE", "category": "MIXED", "county": "Nairobi"},
    {"name": "St. Constantine International School", "type": "PRIVATE", "category": "MIXED", "county": "Arusha"},
    
    # International Schools
    {"name": "International School of Kenya", "type": "INTERNATIONAL", "category": "MIXED", "county": "Nairobi"},
    {"name": "GEMS Cambridge International School", "type": "INTERNATIONAL", "category": "MIXED", "county": "Nairobi"},
    {"name": "Rosslyn Academy", "type": "INTERNATIONAL", "category": "MIXED", "county": "Nairobi"},
    {"name": "Braeside School", "type": "INTERNATIONAL", "category": "MIXED", "county": "Nairobi"},
    {"name": "St. Mary's School", "type": "INTERNATIONAL", "category": "MIXED", "county": "Nairobi"},
    {"name": "German School Nairobi", "type": "INTERNATIONAL", "category": "MIXED", "county": "Nairobi"},
    {"name": "International School Moshi", "type": "INTERNATIONAL", "category": "MIXED", "county": "Kilimanjaro"},
    {"name": "Peponi School", "type": "INTERNATIONAL", "category": "MIXED", "county": "Kiambu"},
    {"name": "Crawford International School", "type": "INTERNATIONAL", "category": "MIXED", "county": "Nairobi"},
    {"name": "Brookhouse School Karen", "type": "INTERNATIONAL", "category": "MIXED", "county": "Nairobi"}
]

# Add more schools to the list
additional_schools = [
    {"name": "St. Mary's Yala", "type": "EXTRA_COUNTY", "category": "BOYS", "county": "Siaya"},
    {"name": "Maranda High School", "type": "NATIONAL", "category": "BOYS", "county": "Siaya"},
    {"name": "Kisumu Boys High School", "type": "EXTRA_COUNTY", "category": "BOYS", "county": "Kisumu"},
    {"name": "Bunyore Girls High School", "type": "EXTRA_COUNTY", "category": "GIRLS", "county": "Vihiga"},
    {"name": "Meru School", "type": "EXTRA_COUNTY", "category": "BOYS", "county": "Meru"},
    {"name": "Loreto High School Limuru", "type": "NATIONAL", "category": "GIRLS", "county": "Kiambu"},
    {"name": "Mang'u High School", "type": "NATIONAL", "category": "BOYS", "county": "Kiambu"},
    {"name": "St. Patrick's Iten", "type": "EXTRA_COUNTY", "category": "BOYS", "county": "Elgeyo-Marakwet"},
    {"name": "Moi Girls Nairobi", "type": "NATIONAL", "category": "GIRLS", "county": "Nairobi"},
    {"name": "Kapsabet Girls High School", "type": "EXTRA_COUNTY", "category": "GIRLS", "county": "Nandi"},
    {"name": "Rang'ala Girls High School", "type": "EXTRA_COUNTY", "category": "GIRLS", "county": "Siaya"},
    {"name": "Kisumu Girls High School", "type": "EXTRA_COUNTY", "category": "GIRLS", "county": "Kisumu"},
    {"name": "Chogoria Girls High School", "type": "EXTRA_COUNTY", "category": "GIRLS", "county": "Tharaka-Nithi"},
    {"name": "Nyambaria High School", "type": "EXTRA_COUNTY", "category": "BOYS", "county": "Nyamira"},
    {"name": "Sawagongo High School", "type": "EXTRA_COUNTY", "category": "BOYS", "county": "Siaya"},
    {"name": "Machakos Boys High School", "type": "EXTRA_COUNTY", "category": "BOYS", "county": "Machakos"},
    {"name": "Machakos Girls High School", "type": "EXTRA_COUNTY", "category": "GIRLS", "county": "Machakos"},
    {"name": "Mama Ngina Girls High School", "type": "EXTRA_COUNTY", "category": "GIRLS", "county": "Mombasa"},
    {"name": "Mombasa High School", "type": "EXTRA_COUNTY", "category": "BOYS", "county": "Mombasa"},
    {"name": "Sheikh Khalifa Bin Zayed Al Nahyan Secondary School", "type": "PRIVATE", "category": "MIXED", "county": "Mombasa"}
]

kenyan_schools.extend(additional_schools)

# Sample vision and mission statements
visions = [
    "To be a center of academic excellence and holistic education",
    "To be a leading institution in providing quality education",
    "To nurture academically excellent and morally upright citizens",
    "To be a globally competitive institution in academic excellence",
    "To be a premier institution in provision of quality education"
]

missions = [
    "To provide quality education that empowers learners to be competitive globally",
    "To nurture talents and instill values for holistic development",
    "To provide an enabling environment for academic excellence and character formation",
    "To offer quality education through effective teaching and learning",
    "To provide a conducive environment that fosters academic excellence and moral values"
]

print(f"Starting to add {len(kenyan_schools)} Kenyan schools to the database...")

# Count of schools successfully created
created_count = 0

# Create all schools
for school_data in kenyan_schools:
    try:
        # Generate a random sub-county based on the county
        sub_county = f"{school_data['county']} {random.choice(['Central', 'East', 'West', 'North', 'South'])}"
        
        # Create school object
        school = School(
            # Basic information
            name=school_data["name"],
            knec_code=random_knec_code(),
            registration_number=random_registration_number(),
            school_type=school_data["type"],
            category=school_data["category"],
            registration_date=random_date(1950, 1990),
            established_date=random_date(1950, 1990),
            motto=random.choice(mottos),
            vision=random.choice(visions),
            mission=random.choice(missions),
            
            # Location information
            county=school_data["county"],
            sub_county=sub_county,
            ward=f"{sub_county} {random.choice(['A', 'B', 'C', 'D'])}",
            postal_address=f"P.O. Box {random.randint(1, 9999)}-{random.randint(10, 99)}{random.randint(100, 999)}, {school_data['county']}",
            physical_address=f"{sub_county}, {school_data['county']} County, Kenya",
            gps_coordinates=random_gps(),
            website=f"https://www.school.ac.ke" if random.random() > 0.3 else None,
            
            # Contact information
            phone_number=random_phone(),
            alternative_phone=random_phone() if random.random() > 0.5 else None,
            email=random_email(school_data["name"]),
            
            # Principal information
            principal_name=f"Mr. {random.choice(['John', 'James', 'Peter', 'Michael', 'David', 'Robert'])}" if school_data["category"] != "GIRLS" else f"Mrs. {random.choice(['Mary', 'Jane', 'Sarah', 'Elizabeth', 'Catherine', 'Anne'])}",
            principal_phone=random_phone(),
            principal_email=random_email(f"principal_{school_data['name']}"),
            principal_tsc_number=random_tsc_number(),
            
            # Academic information
            curriculum=random.choice(['8-4-4', 'CBC', '8-4-4/CBC']),
            number_of_streams=random.randint(1, 6),
            
            # Status
            is_active=True,
            last_inspection_date=random_date(2020, 2023) if random.random() > 0.3 else None,
            
            # System fields are auto-populated
        )
        
        school.save()
        created_count += 1
        print(f"Added: {school.name} ({school.school_type})")
        
    except Exception as e:
        print(f"Error adding {school_data['name']}: {str(e)}")

print(f"\nSuccessfully added {created_count} Kenyan schools to the database.")
print("Schools added by type:")
from django.db.models import Count
school_types = School.objects.values_list('school_type').annotate(count=Count('id'))
for school_type, count in school_types:
    print(f"{School.SCHOOL_TYPE_CHOICES[[choice[0] for choice in School.SCHOOL_TYPE_CHOICES].index(school_type)][1]}: {count}")

print("\nSchools added by category:")
from django.db.models import Count
school_categories = School.objects.values_list('category').annotate(count=Count('id'))
for category, count in school_categories:
    print(f"{School.SCHOOL_CATEGORY_CHOICES[[choice[0] for choice in School.SCHOOL_CATEGORY_CHOICES].index(category)][1]}: {count}")

print("\nSchools added by county:")
for county in counties:
    count = School.objects.filter(county=county).count()
    if count > 0:
        print(f"{county}: {count}")