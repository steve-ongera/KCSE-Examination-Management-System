from django.core.management.base import BaseCommand
from django.db.models import Count
from django.apps import apps
from datetime import date, timedelta
import random

School = apps.get_model('exam_portal', 'School')
Student = apps.get_model('exam_portal', 'Student')

def random_date(start_date, end_date):
    """Generate a random date between start_date and end_date."""
    days = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, days))

def random_county():
    """Select a random county from a predefined list."""
    counties = [
        "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Uasin Gishu", "Kiambu",
        "Machakos", "Kajiado", "Bungoma", "Kakamega", "Kilifi", "Nyeri",
        "Meru", "Embu", "Kisii", "Siaya", "Nandi"
    ]
    return random.choice(counties)

def random_sub_county(county):
    """Select a random sub-county from a predefined list based on the county."""
    sub_counties = {
        "Nairobi": ["Westlands", "Dagoretti", "Langata"],
        "Kisii": ["Kisii Central", "Bomachoge"],
        "Kiambu": ["Juja", "Thika", "Ruiru"]
        # Add more counties and sub-counties as needed
    }
    return random.choice(sub_counties.get(county, ["Central"]))

def generate_index_number(school):
    """Generate a unique index number for a student."""
    school_code = school.knec_code
    count = Student.objects.filter(school=school).count()
    return f"{school_code}/{count + 1:04d}/2020"

def generate_admission_number(existing_adms):
    """Generate a unique admission number."""
    while True:
        adm = f"ADM/{random.randint(1000,9999)}/{random.randint(2020,2025)}"
        if adm not in existing_adms:
            existing_adms.add(adm)
            return adm

class Command(BaseCommand):
    help = 'Generates students for all schools, regardless of student count.'

    def handle(self, *args, **kwargs):
        current_year = date.today().year
        today = date.today()
        schools = School.objects.all()  # Get all schools, regardless of student count

        for school in schools:
            num_students = random.randint(14, 27)  # You can adjust this range as needed
            existing_adms = set()

            # Combined first and middle name lists for male and female
            names = {
                'M': [
                    'Elias', 'Geoffrey', 'Simon', 'Mohamed', 'Chris', 'Maxwell', 'Ben', 'Justus', 'Allan', 'Evans',
                    'Ronald','Maulid', 'Sylvester', 'Arnold', 'Brian', 'Eric', 'Clinton', 'Julius', 'Oscar', 'Patrick', 'Newton',
                    'Trevor', 'Martin', 'Omar', 'Lemmy', 'Ibrahim', 'Faisal', 'Anthony', 'Titus', 'Brayo', 'Kelvin',
                    'Elvis', 'Duncan', 'Felix','Abute', 'Alvin', 'Dan', 'Levi', 'Boniface', 'Cyrus', 'Mark', 'Abdallah',                  
                    'Tom', 'Brian', 'Khalid', 'Rashid', 'Jackson', 'Japhet', 'Barack', 'Kassim', 'Ramadhan', 'Ismail'
                ],
                'F': [
                    'Gladys', 'Veronica', 'Emily', 'Vivian', 'Fridah', 'Tabitha', 'Alice', 'Connie', 'Deborah', 'Judith',
                    'Brenda', 'Janet', 'Zuleika', 'Valerie', 'Linet', 'Lucy', 'Angela', 'Dorothy', 'Beatrice', 'Patricia',
                    'Winnie', 'Hope', 'Tina', 'Zena', 'Farida', 'Rahab', 'Judy', 'Norah', 'Peris', 'Damaris'
                    'Rose', 'Monica', 'Florence', 'Edna', 'Carol', 'Mildred', 'Abigail', 'Celestine', 'Salome', 'Nancy',
                    'Christine', 'Purity', 'Sharleen', 'Yvonne', 'Lilian', 'Eunice', 'Peninah', 'Leah', 'Miriam', 'Asha'
                    
                ]
            }


            last_names = [
                    'Abdullahi', 'Mugo', 'Oluoch', 'Anyango', 'Ng’ang’a', 'Wandera', 'Cheruiyot', 'Otieno', 'Muli', 'Koskei',         
                    'Omondi', 'Were', 'Kariuki', 'Mutua', 'Barasa', 'Okumu', 'Kimemia', 'Gakuru', 'Owino', 'Mutiso',
                     'Ochieng', 'Mungai', 'Musimbi', 'Nduta', 'Lagat', 'Ali', 'Mwende', 'Kiptum', 'Juma', 'Naliaka',
                    'Ruto', 'Odhiambo', 'Chege', 'Wekesa', 'Mburu', 'Njiru', 'Abuya', 'Mugambi', 'Odinga', 'Lusweti',
                    'Musyoka', 'Gathungu', 'Karanja', 'Makau', 'Mwanzia', 'Munyua', 'Kemei', 'Wafula', 'Tobiko', 'Kipchoge',
                    'Koech', 'Mwangangi', 'Chebet', 'Nyambane', 'Ongeri', 'Simba', 'Omondi', 'Kilonzo', 'Masai', 'Muthee',
                    'Waiguru', 'Atieno', 'Njenga', 'Okoth', 'Mwita', 'Mwachiro', 'Yatich', 'Ngugi', 'Muli', 'Ndung’u',
                    'Mbithi', 'Njoki', 'Gicheru', 'Tumbo', 'Cherop', 'Wanyama', 'Karimi', 'Mbogo', 'Wairimu', 'Nakitare'
                   
                ]


            for _ in range(num_students):
                gender = random.choice(['M', 'F'])
                fname = random.choice(names[gender])
                lname = random.choice(last_names)

                bdate = random_date(date(today.year - 20, 1, 1), date(today.year - 15, 12, 31))
                county = random_county()
                sub_county = random_sub_county(county)

                index = generate_index_number(school)
                adm_no = generate_admission_number(existing_adms)

                adm_date = random_date(date(today.year - 4, 1, 1), date(today.year - 1, 12, 31))
                kcpe_year = adm_date.year - 1
                kcpe_index = f"{random.randint(10000,99999)}/{kcpe_year}"
                kcpe_marks = random.randint(250, 420)
                current_class = f"Form {min(4, today.year - adm_date.year + 1)}"

                student = Student(
                    first_name=fname,
                    middle_name=fname,
                    last_name=lname,
                    birth_date=bdate,
                    birth_certificate_number=f"BC{random.randint(100000, 999999)}",
                    gender=gender,
                    nationality="Kenyan",
                    county_of_origin=county,
                    sub_county=sub_county,
                    school=school,
                    index_number=index,
                    admision_number=adm_no,
                    admission_date=adm_date,
                    current_class=current_class,
                    is_boarder=bool(random.getrandbits(1)),
                    email=f"{fname.lower()}.{lname.lower()}@gmail.com" if random.random() > 0.3 else None,
                    phone_number=f"07{random.randint(10000000, 99999999)}" if random.random() > 0.5 else None,
                    previous_school=f"{random.choice(['St.', 'Unity', 'Green'])} {random.choice(['Primary', 'Prep'])} School",
                    kcpe_year=kcpe_year,
                    kcpe_index=kcpe_index,
                    kcpe_marks=kcpe_marks,
                )
                student.save()

            self.stdout.write(self.style.SUCCESS(f"✔ Created {num_students} students for {school.name}"))
        
        self.stdout.write(self.style.SUCCESS("🎉 All student generation complete."))
