from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse
from .forms import *
from .models import *
from django.db.models import Count
from django.utils import timezone
from collections import defaultdict
import json

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Redirect based on user_type
            if user.user_type == 1:  # Student
                return redirect('student_dashboard')
            elif user.user_type == 2:  # School Admin
                return redirect('school_admin_dashboard')
            elif user.user_type == 3:  # KNEC Official
                return redirect('knec_dashboard')
            else:
                return redirect('home')  # Fallback
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'registration/login.html')



from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SchoolAdminRegistrationForm, StudentRegistrationForm
from .models import SchoolAdminProfile, School, Student, User
from django.db import transaction


def register(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        
        if user_type == 'school_admin':
            form = SchoolAdminRegistrationForm(request.POST)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        # Extract school information
                        knec_code = form.cleaned_data['knec_code']
                        registration_number = form.cleaned_data['registration_number']
                        school_name = form.cleaned_data['school_name']
                        special_code = form.cleaned_data['special_code']
                        
                        # Verify school exists and information matches
                        try:
                            school = School.objects.get(
                                knec_code=knec_code,
                                registration_number=registration_number,
                                name=school_name
                            )
                        except School.DoesNotExist:
                            messages.error(request, 'School information does not match our records.')
                            return redirect('register')
                        
                        # Check if special_code matches the school's special_code
                        if school.special_code != special_code:
                            messages.error(request, 'Invalid special code for this school.')
                            return redirect('register')
                        
                        # Create user
                        user = form.save(commit=False)
                        user.user_type = 2  # School admin
                        user.save()
                        
                        # Check if admin profile already exists
                        admin_profile, created = SchoolAdminProfile.objects.get_or_create(
                            special_code=special_code,
                            defaults={
                                'school': school,
                                'position': 'Administrator',
                                'is_primary_admin': False
                            }
                        )
                        
                        if not created:
                            # If profile exists, update it if needed
                            if admin_profile.school != school:
                                admin_profile.school = school
                                admin_profile.save()
                        
                        messages.success(request, 'School admin account created successfully!')
                        return redirect('login')
                        
                except Exception as e:
                    messages.error(request, f'Registration failed: {str(e)}')
                    return redirect('register')
        
        elif user_type == 'student':
            form = StudentRegistrationForm(request.POST)
            if form.is_valid():
                # Create user
                user = form.save(commit=False)
                user.user_type = 1  # Student
                user.save()
                
                # Create student profile
                # student = Student.objects.create(
                #     user=user,
                #     first_name=form.cleaned_data['first_name'],
                #     last_name=form.cleaned_data['last_name'],
                #     birth_certificate_number=form.cleaned_data['birth_certificate_number'],
                #     index_number=form.cleaned_data['index_number'],
                #     # You'll need to set school and other required fields
                # )
                
                messages.success(request, 'Student account created successfully!')
                return redirect('login')
    
    else:
        form = None
    
    return render(request, 'registration/register.html', {
        'school_admin_form': SchoolAdminRegistrationForm(),
        'student_form': StudentRegistrationForm()
    })


@login_required
def student_dashboard(request):
    return render(request, 'dashboards/student_dashboard.html')

@login_required
def school_admin_dashboard(request):
    return render(request, 'dashboards/school_admin_dashboard.html')




from django.shortcuts import render
from django.db.models import Count, F, Func, Value, CharField
from django.db.models.functions import ExtractYear
from django.utils import timezone
from .models import (
    User, School, Student, ExamYear, 
    ExamRegistration, SubjectRegistration
)
from collections import defaultdict
import json

class ExtractYear(Func):
    function = 'STRFTIME'
    template = "%(function)s('%%Y', %(expressions)s)"
    output_field = CharField()

def knec_dashboard(request):
    # Ensure only KNEC officials can access this view
    if not request.user.is_authenticated or request.user.user_type != 3:
        return redirect('login')  # Or appropriate permission denied view

    # Get current exam year
    current_exam_year = ExamYear.objects.filter(is_current=True).first()
    
    # Basic counts
    total_students = Student.objects.count()
    total_schools = School.objects.count()
    
    # Students registered for current exam year
    if current_exam_year:
        registered_students = ExamRegistration.objects.filter(
            exam_year=current_exam_year
        ).count()
    else:
        registered_students = 0
    
    # Get exam registration trends by year
    registration_trends = ExamRegistration.objects.annotate(
        year=F('exam_year__year')
    ).values('year').annotate(
        count=Count('id')
    ).order_by('year')
    
    # Prepare data for charts
    years = []
    counts = []
    
    for trend in registration_trends:
        years.append(str(trend['year']))
        counts.append(trend['count'])
    
    # If no data, provide defaults
    if not years:
        years = ['2022', '2023', '2024']
        counts = [0, 0, 0]
    
    # Get school registration trends - database agnostic approach
    school_trends = School.objects.annotate(
        year=ExtractYear('created_at')
    ).values('year').annotate(
        count=Count('id')
    ).order_by('year')
    
    school_years = []
    school_counts = []
    
    for trend in school_trends:
        school_years.append(str(trend['year']))
        school_counts.append(trend['count'])
    
    # Get subject registration distribution for current year
    if current_exam_year:
        subject_distribution = SubjectRegistration.objects.filter(
            registration__exam_year=current_exam_year
        ).values(
            'subject__name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:10]  # Top 10 subjects
    else:
        subject_distribution = []
    
    subject_names = []
    subject_counts = []
    
    for subject in subject_distribution:
        subject_names.append(subject['subject__name'])
        subject_counts.append(subject['count'])
    
    # Get latest registered students
    latest_students = Student.objects.select_related('school').order_by('-created_at')[:5]
    
    # Get latest schools
    latest_schools = School.objects.order_by('-created_at')[:5]
    
    context = {
        # Basic counts
        'total_students': total_students,
        'registered_students': registered_students,
        'total_schools': total_schools,
        'current_exam_year': current_exam_year.year if current_exam_year else "N/A",
        
        # Chart data
        'registration_years': json.dumps(years),
        'registration_counts': json.dumps(counts),
        'school_years': json.dumps(school_years),
        'school_counts': json.dumps(school_counts),
        'subject_names': json.dumps(subject_names),
        'subject_counts': json.dumps(subject_counts),
        
        # Latest records
        'latest_students': latest_students,
        'latest_schools': latest_schools,
        
        # For template
        'page_title': 'KNEC Admin Dashboard',
    }
    
    return render(request, 'dashboards/knec_dashboard.html', context)