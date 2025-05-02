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

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Only showing the problematic model for clarity
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver
class ExamResult(models.Model):
    """Model representing a student's results for a subject in KCSE"""
    subject_registration = models.OneToOneField('SubjectRegistration', on_delete=models.CASCADE, related_name='result')
    marks = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    grade = models.CharField(max_length=2, blank=True, null=True)  # Changed to allow null
    points = models.PositiveIntegerField(blank=True, null=True)
    
    def calculate_grade_and_points(self):
        """Calculate grade and points based on marks and grading system"""
        # Exit early if marks are None
        if self.marks is None:
            self.grade = None
            self.points = None
            return
        
        grading_system = self.subject_registration.registration.exam_year.grading_system
        marks = self.marks
        
        if isinstance(grading_system, dict):
            # Dictionary format with grade keys
            for grade, info in grading_system.items():
                min_score = info.get('min_score', 0)
                max_score = info.get('max_score', 100)
                
                if min_score <= marks <= max_score:
                    self.grade = grade
                    self.points = info.get('points', 0)
                    break
        elif isinstance(grading_system, list):
            # List format with grade info dictionaries
            for grade_info in grading_system:
                min_val = grade_info.get('min_score', grade_info.get('min', 0))
                max_val = grade_info.get('max_score', grade_info.get('max', 100))
                
                if min_val <= marks <= max_val:
                    self.grade = grade_info.get('grade', '')
                    self.points = grade_info.get('points', 0)
                    break
    
    def save(self, *args, **kwargs):
        self.calculate_grade_and_points()
        super().save(*args, **kwargs)
    
    def __str__(self):
        mark_display = f"{self.marks}%" if self.marks is not None else "No marks"
        grade_display = f"({self.grade})" if self.grade else ""
        return f"{self.subject_registration}: {mark_display} {grade_display}"


@receiver(pre_save, sender=ExamResult)
def ensure_grade_points_updated(sender, instance, **kwargs):
    """Signal handler to ensure grade and points are updated when marks change"""
    if instance.pk:  # If this is an update, not a new record
        try:
            # Get the previous instance from database
            old_instance = ExamResult.objects.get(pk=instance.pk)
            
            # If marks have changed, recalculate grade and points
            if old_instance.marks != instance.marks:
                instance.calculate_grade_and_points()
        except ExamResult.DoesNotExist:
            # This is a new instance, save() will handle it
            pass



from django.db import models
from django.core.validators import FileExtensionValidator

class ExamPaperArchive(models.Model):
    PAPER_TYPE_CHOICES = [
        ('MAIN', 'Main Exam'),
        ('SUPP', 'Supplementary'),
        ('MOCK', 'Mock Exam'),
        ('SPEC', 'Special Paper'),
    ]
    
    exam_year = models.ForeignKey('ExamYear', on_delete=models.PROTECT)
    subject = models.ForeignKey('Subject', on_delete=models.PROTECT)
    paper_type = models.CharField(max_length=4, choices=PAPER_TYPE_CHOICES, default='MAIN')
    paper_code = models.CharField(max_length=20, help_text="Unique code for this paper")
    paper_title = models.CharField(max_length=200)
    paper_file = models.FileField(
        upload_to='exam_papers/%Y/%m/%d/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])]
    )
    is_confidential = models.BooleanField(default=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey('User', related_name='approved_papers', on_delete=models.SET_NULL, null=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('exam_year', 'subject', 'paper_code')
        verbose_name_plural = "Exam Paper Archives"
        ordering = ['-exam_year__year', 'subject__name']
    
    def __str__(self):
        return f"{self.subject.name} ({self.paper_code}) - {self.exam_year.year}"

class PaperReleaseSchedule(models.Model):
    paper = models.ForeignKey('ExamPaperArchive', on_delete=models.CASCADE)
    release_date = models.DateTimeField()
    released_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    is_released = models.BooleanField(default=False)
    release_notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Paper Release Schedules"
    
    def __str__(self):
        return f"Release of {self.paper} on {self.release_date}"
    


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class ExamCenter(models.Model):
    """Model representing examination centers"""
    CENTER_TYPE_CHOICES = [
        ('MAIN', 'Main Center'),
        ('SUB', 'Sub-Center'),
        ('SPECIAL', 'Special Needs Center'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    center_type = models.CharField(max_length=10, choices=CENTER_TYPE_CHOICES, default='MAIN')
    school = models.ForeignKey('School', on_delete=models.SET_NULL, null=True, blank=True)
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    
    # Location details
    county = models.CharField(max_length=100)
    sub_county = models.CharField(max_length=100)
    address = models.TextField()
    gps_coordinates = models.CharField(max_length=50, blank=True, null=True)
    
    # Contact information
    contact_person = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class ExamTimetable(models.Model):
    """Model representing examination timetables"""
    exam_year = models.ForeignKey('ExamYear', on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True, blank=True)
    published_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.exam_year.year}"

class ExamSession(models.Model):
    """Model representing individual exam sessions in a timetable"""
    timetable = models.ForeignKey(ExamTimetable, on_delete=models.CASCADE, related_name='sessions')
    subject = models.ForeignKey('Subject', on_delete=models.PROTECT)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes")
    paper_code = models.CharField(max_length=20)
    instructions = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['date', 'start_time']
    
    def __str__(self):
        return f"{self.subject.name} - {self.date} {self.start_time} to {self.end_time}"

class Invigilator(models.Model):
    """Model representing exam invigilators"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invigilator_profile')
    tsc_number = models.CharField(max_length=20, blank=True, null=True)
    id_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    qualification = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    # Areas of specialization
    subjects = models.ManyToManyField('Subject', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.id_number})"

class InvigilationAssignment(models.Model):
    """Model representing assignment of invigilators to exam centers"""
    invigilator = models.ForeignKey(Invigilator, on_delete=models.CASCADE)
    exam_center = models.ForeignKey(ExamCenter, on_delete=models.CASCADE)
    exam_session = models.ForeignKey(ExamSession, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, default='Invigilator')  # e.g., Chief Invigilator, Deputy, etc.
    is_confirmed = models.BooleanField(default=False)
    
    date_assigned = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        unique_together = ('invigilator', 'exam_session')
    
    def __str__(self):
        return f"{self.invigilator} assigned to {self.exam_center} for {self.exam_session}"
    
    
class OverallResult(models.Model):
    """Model representing a student's overall KCSE performance"""
    registration = models.OneToOneField(ExamRegistration, on_delete=models.CASCADE, related_name='overall_result')
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    average_grade = models.CharField(max_length=2, blank=True, null=True)  # Changed to allow null
    average_points = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    division = models.CharField(max_length=20, blank=True, null=True)  # Changed to allow null
    
    def calculate_results(self):
        # Get all subject results for this registration
        subject_results = ExamResult.objects.filter(
            subject_registration__registration=self.registration
        )
        
        # Exit early if no results or no results with points
        valid_results = [result for result in subject_results if result.marks is not None and result.points is not None]
        if not valid_results:
            self.total_marks = None
            self.average_points = None
            self.average_grade = None
            self.division = None
            return
        
        # Calculate total marks and average points
        total_points = 0
        total_marks = 0
        count = 0
        
        for result in valid_results:
            total_points += result.points
            total_marks += result.marks
            count += 1
        
        if count > 0:
            self.total_marks = total_marks / count
            self.average_points = total_points / count
            
            # Determine overall grade based on average points
            grading_system = self.registration.exam_year.grading_system
            
            # Debug info
            print(f"Overall grading system type: {type(grading_system)}")
            print(f"Average points: {self.average_points}")
            
            # Match average points to the closest grade in the grading system
            if isinstance(grading_system, dict):
                # Find the grade that matches the average points
                for grade, info in grading_system.items():
                    if info.get('points') == round(self.average_points):
                        self.average_grade = grade
                        # Set division based on grade ranges
                        points = info.get('points', 0)
                        if points >= 10:  # A, A-, B+
                            self.division = "Division 1"
                        elif points >= 8:  # B, B-
                            self.division = "Division 2"
                        elif points >= 6:  # C+, C
                            self.division = "Division 3"
                        elif points >= 2:  # C-, D+, D, D-
                            self.division = "Division 4"
                        else:  # E
                            self.division = "Division 5"
                        break
            elif isinstance(grading_system, list):
                # Alternative format handling if needed
                for grade_info in grading_system:
                    points_val = grade_info.get('points', 0)
                    if points_val == round(self.average_points):
                        self.average_grade = grade_info.get('grade', '')
                        self.division = grade_info.get('division', '')
                        break
        else:
            # Set all fields to None if no valid results
            self.total_marks = None
            self.average_points = None
            self.average_grade = None
            self.division = None
    
    def save(self, *args, **kwargs):
        self.calculate_results()
        super().save(*args, **kwargs)
    
    def __str__(self):
        if self.average_grade and self.average_points is not None:
            return f"{self.registration}: {self.average_grade} ({self.average_points} points)"
        return f"{self.registration}: No results yet"
    



from django.utils import timezone
from django.core.validators import RegexValidator

class KNECProfile(models.Model):
    """Model for KNEC official profile information"""
    
    DEPARTMENT_CHOICES = [
        ('Examinations', 'Examinations'),
        ('Quality Assurance', 'Quality Assurance'),
        ('Research', 'Research'),
        ('Administration', 'Administration'),
        ('ICT', 'ICT'),
    ]
    
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('system', 'System Default'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='knec_profile')
    knec_id = models.CharField(max_length=15, unique=True, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, blank=True)
    phone_number = models.CharField(
        max_length=15, 
        blank=True,
        
    )
    office_location = models.CharField(max_length=100, blank=True)
    responsibilities = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='knec_profile_pics/', blank=True, null=True)
    
    # Security settings
    two_factor_enabled = models.BooleanField(default=False)
    login_alerts = models.BooleanField(default=True)
    session_timeout = models.BooleanField(default=True)
    
    # Notification preferences
    system_notifications = models.BooleanField(default=True)
    security_alerts = models.BooleanField(default=True)
    exam_updates = models.BooleanField(default=True)
    
    # Interface preferences
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    results_per_page = models.IntegerField(default=25)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}'s KNEC Profile"
    
    def save(self, *args, **kwargs):
        # Generate KNEC ID if not provided
        if not self.knec_id:
            # Format: KNEC-YYYY-XXXXX where XXXXX is the user ID padded with zeros
            year = timezone.now().year
            user_id_padded = str(self.user.id).zfill(5)
            self.knec_id = f"KNEC-{year}-{user_id_padded}"
        super().save(*args, **kwargs)


class LoginAttempt(models.Model):
    """Model to track login attempts for security monitoring"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_attempts')
    timestamp = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        status = "Successful" if self.successful else "Failed"
        return f"{status} login attempt by {self.user.username} at {self.timestamp}"


class ActivityLog(models.Model):
    """Model to log user activities within the system"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities' , null=True,
        blank=True  )
    activity_type = models.CharField(max_length=50)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        if self.user:
            return f"{self.activity_type} by {self.user.username}"
        return f"{self.activity_type} (no user)"
    

# models.py - Django models for KNEC Resources

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class ResourceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    css_class = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class Resource(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='resources/')
    file_size = models.PositiveIntegerField(blank=True, null=True)  # Size in KB
    thumbnail = models.ImageField(upload_to='resources/thumbnails/', blank=True, null=True)
    
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    download_count = models.PositiveIntegerField(default=0)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_resources')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_resources')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # If status is being changed to published, set published_at
        if self.pk:
            old_instance = Resource.objects.get(pk=self.pk)
            if old_instance.status != 'published' and self.status == 'published':
                self.published_at = timezone.now()
        elif self.status == 'published':
            self.published_at = timezone.now()
            
        super().save(*args, **kwargs)

class ResourceDownloadLog(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    downloaded_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} downloaded {self.resource.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    def __str__(self):
        return self.user.username