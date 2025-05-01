from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
import random
import string

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'student'),
        (2, 'school_admin'),
        (3, 'knec_official'),
    )
    
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class School(models.Model):
    """Model representing schools with comprehensive details"""
    SCHOOL_TYPE_CHOICES = [
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
        ('EXTRA_COUNTY', 'Extra County'),
        ('NATIONAL', 'National'),
        ('INTERNATIONAL', 'International')
    ]
    
    SCHOOL_CATEGORY_CHOICES = [
        ('BOYS', 'Boys Only'),
        ('GIRLS', 'Girls Only'),
        ('MIXED', 'Mixed')
    ]
    
    # Basic Information
    name = models.CharField(max_length=200)
    knec_code = models.CharField(max_length=20, unique=True)
    registration_number = models.CharField(max_length=50, unique=True)
    special_code = models.CharField(max_length=100, blank=True, null=True , unique=True)
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPE_CHOICES)
    category = models.CharField(max_length=10, choices=SCHOOL_CATEGORY_CHOICES)
    registration_date = models.DateField()
    established_date = models.DateField()
    motto = models.CharField(max_length=100, blank=True, null=True)
    mission = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
    
    # Location Information
    county = models.CharField(max_length=100)
    sub_county = models.CharField(max_length=100)
    ward = models.CharField(max_length=100, blank=True, null=True)
    postal_address = models.CharField(max_length=100)
    physical_address = models.TextField()
    gps_coordinates = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    # Contact Information
    phone_number = models.CharField(max_length=15)
    alternative_phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    # Principal Information
    principal_name = models.CharField(max_length=100)
    principal_phone = models.CharField(max_length=15)
    principal_email = models.EmailField(blank=True, null=True)
    principal_tsc_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Academic Information
    curriculum = models.CharField(max_length=100, default='8-4-4')  # or CBC
    number_of_streams = models.PositiveIntegerField(default=1)
   
 
    
    # Status
    is_active = models.BooleanField(default=True)
    last_inspection_date = models.DateField(blank=True, null=True)
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def generate_unique_special_code(self, length=10):
        """Generates a unique uppercase special code."""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
            if not School.objects.filter(special_code=code).exists():
                return code

    def save(self, *args, **kwargs):
        # Generate special code if it's missing or invalid
        if not self.special_code or len(self.special_code) < 8 or not self.special_code.isupper():
            self.special_code = self.generate_unique_special_code()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.knec_code}) - {self.get_school_type_display()}"

class Subject(models.Model):
    """Model representing all possible KCSE subjects"""
    SUBJECT_CATEGORIES = [
        ('CORE', 'Core Compulsory'),
        ('SCIENCE', 'Science Subjects'),
        ('HUMANITIES', 'Humanities Subjects'),
        ('TECHNICAL', 'Technical Subjects'),
        ('LANGUAGES', 'Language Subjects'),
    ]
    
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SUBJECT_CATEGORIES)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class ExamYear(models.Model):
    """Model representing an academic year for KCSE exams"""
    year = models.PositiveIntegerField(unique=True)
    grading_system = models.JSONField()  # Stores the grading criteria for the year
    is_current = models.BooleanField(default=False)
    
    def __str__(self):
        return f"KCSE {self.year}"

class Student(models.Model):
    """Model representing students with comprehensive details"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    birth_certificate_number = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    nationality = models.CharField(max_length=50, default='Kenyan')
    county_of_origin = models.CharField(max_length=50)
    sub_county = models.CharField(max_length=50)
    passport_photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    disability = models.CharField(max_length=100, blank=True, null=True)
    disability_description = models.TextField(blank=True, null=True)
    
    # School Information
    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name='students')
    index_number = models.CharField(max_length=20, unique=True) # for kcse purpose format schoolcode/001/year for examination
    admision_number = models.CharField(max_length=20, null=True) 
    admission_date = models.DateField()
    current_class = models.CharField(max_length=20)  # e.g., Form 1, Form 2, etc.
    house = models.CharField(max_length=50, blank=True, null=True)  # For boarding schools
    is_boarder = models.BooleanField(default=False)
    
    # Contact Information
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    postal_address = models.CharField(max_length=100, blank=True, null=True)
    residential_address = models.TextField(blank=True, null=True)
      
    
    # Previous Education
    previous_school = models.CharField(max_length=100, blank=True, null=True)
    kcpe_year = models.PositiveIntegerField(blank=True, null=True)
    kcpe_index = models.CharField(max_length=20, blank=True, null=True)
    kcpe_marks = models.PositiveIntegerField(blank=True, null=True)
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.index_number} - {self.first_name} {self.last_name}"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='user_profile')
    
    # Additional student-specific user fields can go here
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Student Profile for {self.user.username}"

class SchoolAdminProfile(models.Model):
    special_code = models.CharField(max_length=100 , unique=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='admins')
    position = models.CharField(max_length=100)  # e.g., "Principal", "Deputy", "Exam Officer"
    tsc_number = models.CharField(max_length=20, blank=True, null=True)
    is_primary_admin = models.BooleanField(default=False)  # Main admin for the school
    
    
    
    def __str__(self):
        return f"School Admin Profile for {self.special_code} at {self.school.name}"


class KNECOfficialProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='knec_official_profile')
    department = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    is_supervisor = models.BooleanField(default=False)
    
    def __str__(self):
        return f"KNEC Official Profile for {self.user.username}"

class ExamRegistration(models.Model):
    """Model representing a student's registration for KCSE in a particular year"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='registrations')
    exam_year = models.ForeignKey(ExamYear, on_delete=models.CASCADE)
    registration_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('student', 'exam_year')
    
    def __str__(self):
        return f"{self.student} - KCSE {self.exam_year.year}"

class SubjectRegistration(models.Model):
    """Model representing subjects a student has registered for in a particular KCSE exam"""
    registration = models.ForeignKey(ExamRegistration, on_delete=models.CASCADE, related_name='subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    is_compulsory = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('registration', 'subject')
    
    def __str__(self):
        return f"{self.registration.student} - {self.subject.name} ({self.registration.exam_year.year})"

class ExamResult(models.Model):
    """Model representing a student's results for a subject in KCSE"""
    subject_registration = models.OneToOneField(SubjectRegistration, on_delete=models.CASCADE, related_name='result')
    marks = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    grade = models.CharField(max_length=2, blank=True)
    points = models.PositiveIntegerField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Calculate grade and points based on the exam year's grading system
        grading_system = self.subject_registration.registration.exam_year.grading_system
        marks = self.marks
        
        # Determine grade and points based on the grading system
        for grade_info in grading_system:
            if grade_info['min'] <= marks <= grade_info['max']:
                self.grade = grade_info['grade']
                self.points = grade_info['points']
                break
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.subject_registration}: {self.marks}% ({self.grade})"

class OverallResult(models.Model):
    """Model representing a student's overall KCSE performance"""
    registration = models.OneToOneField(ExamRegistration, on_delete=models.CASCADE, related_name='overall_result')
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    average_grade = models.CharField(max_length=2, blank=True)
    average_points = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    division = models.CharField(max_length=20, blank=True)
    
    def calculate_results(self):
        # Get all subject results for this registration
        subject_results = ExamResult.objects.filter(
            subject_registration__registration=self.registration
        )
        
        # Calculate total marks and average points
        total_points = 0
        total_marks = 0
        count = 0
        
        for result in subject_results:
            if result.points is not None:
                total_points += result.points
                total_marks += result.marks
                count += 1
        
        if count > 0:
            self.total_marks = total_marks / count
            self.average_points = total_points / count
            
            # Determine overall grade based on average points
            grading_system = self.registration.exam_year.grading_system
            for grade_info in grading_system:
                if grade_info['min_avg'] <= self.average_points <= grade_info['max_avg']:
                    self.average_grade = grade_info['grade']
                    self.division = grade_info['division']
                    break
    
    def save(self, *args, **kwargs):
        self.calculate_results()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.registration}: {self.average_grade} ({self.average_points} points)"