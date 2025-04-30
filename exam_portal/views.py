from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse
from .forms import *
from .models import *
from django.db.models import Count
from django.utils import timezone
from collections import defaultdict
import json
from django.core.mail import EmailMultiAlternatives, send_mail
from django.core.cache import cache
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
Account = get_user_model()
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models import Count, Q
from datetime import datetime
import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import os
from django.contrib.auth import authenticate, login , logout

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

def custom_logout(request):
    logout(request)
    messages.error(request, "Logged out successfully!")
    return redirect('login')


#forgot password view 
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)

            # Generate reset password token and send email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http'
            }
            
            # Render both HTML and plain text versions of the email
            html_message = render_to_string('auth/reset_password_email.html', context)
            plain_message = strip_tags(html_message)
            
            to_email = email
            
            # Use EmailMultiAlternatives for sending both HTML and plain text
            email = EmailMultiAlternatives(
                mail_subject,
                plain_message,
                'noreply@yourdomain.com',
                [to_email]
            )
            email.attach_alternative(html_message, "text/html")
            email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgot_password')
    return render(request, 'auth/forgot_password.html')



def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if password == confirm_password:
                if len(password) < 6:
                    messages.error(request, 'Password must be at least 6 characters.')
                    return redirect('reset_password', uidb64=uidb64, token=token)

                user.set_password(password)
                user.last_password_change = timezone.now()
                user.save()
                messages.success(request, 'Password reset successful. You can now login with your new password.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')
                return redirect('reset_password', uidb64=uidb64, token=token)

        # GET request – render the form
        return render(request, 'auth/reset_password.html')
    else:
        messages.error(request, 'Invalid or expired reset link. Please try again.')
        return redirect('login')

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
from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Student, ExamRegistration, SchoolAdminProfile

def school_admin_dashboard(request):
    if not request.user.is_authenticated or request.user.user_type != 2:
        return redirect('login')
    
    try:
        # Get the SchoolAdminProfile using the special_code which matches the username
        admin_profile = SchoolAdminProfile.objects.get(special_code=request.user.username)
        school = admin_profile.school
    except SchoolAdminProfile.DoesNotExist:
        return redirect('login')
    
    # Get statistics
    total_students = Student.objects.filter(school=school).count()
    
    # All exam registrations for current year
    exam_registrations = ExamRegistration.objects.filter(
        student__school=school,
        exam_year__is_current=True
    ).count()
    
    # Since there's no exam_type field, we need to determine KCSE/KCPE a different way
    # Let's assume students in certain classes (Forms) are for KCSE and others for KCPE
    # For example, students in Classes 1-8 are for KCPE, and Forms 1-4 are for KCSE
    
    # For KCSE registrations, assuming students in Forms 1-4 (could be stored as 'Form 1', 'Form 2', etc.)
    # Get all registered students who are in Forms
    kcse_registrations = ExamRegistration.objects.filter(
        student__school=school,
        exam_year__is_current=True,
        student__current_class__startswith='Form'  # Adjust based on your actual data model
    ).count()
    
    # Get distinct class counts
    active_classes = Student.objects.filter(
        school=school
    ).values('current_class').distinct().count()
    
    # Recent activities (you would implement this based on your activity log model)
    recent_activities = [
        {
            'title': 'New student registered',
            'description': 'John Doe was added to Form 2',
            'timestamp': '2023-06-15 10:30:00'
        },
        {
            'title': 'Exam registration',
            'description': '15 students registered for KCSE 2023',
            'timestamp': '2023-06-14 14:45:00'
        }
    ][:5]  # Just sample data - replace with your actual activity log query
    
    context = {
        'kcse_registrations': kcse_registrations,
        'total_students': total_students,
        'exam_registrations': exam_registrations,
        'active_classes': active_classes,
        'recent_activities': recent_activities,
        'school': school
    }
    
    return render(request, 'dashboards/school_admin_dashboard.html', context)




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


from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Subject, ExamYear, ExamRegistration, SubjectRegistration
from django.contrib import messages
from django.db import transaction

def register_student_exam(request):
    student = None
    optional_categories = ['SCIENCE', 'HUMANITIES', 'TECHNICAL', 'LANGUAGES']
    optional_subjects = Subject.objects.filter(category__in=optional_categories, is_active=True)
    core_subjects = Subject.objects.filter(category='CORE')
    current_year = ExamYear.objects.filter(is_current=True).first()

    if request.method == 'POST':
        index_number = request.POST.get('index_number')
        student = Student.objects.filter(index_number=index_number).first()

        if not student:
            messages.error(request, "Student with that index number not found.")
        elif 'register_subjects' in request.POST:
            selected_subject_ids = request.POST.getlist('optional_subjects')
            
            if not current_year:
                messages.error(request, "No current exam year found.")
            elif len(selected_subject_ids) != 4:
                messages.error(request, "You must select exactly 4 optional subjects.")
            else:
                try:
                    with transaction.atomic():
                        # Check if student is already registered for current year
                        if ExamRegistration.objects.filter(student=student, exam_year=current_year).exists():
                            messages.error(request, "This student is already registered for this exam year.")
                            return redirect('register-student-exam')

                        # Create new exam registration
                        exam_reg = ExamRegistration.objects.create(
                            student=student,
                            exam_year=current_year
                        )

                        # Register core subjects
                        for subject in core_subjects:
                            SubjectRegistration.objects.create(
                                registration=exam_reg,
                                subject=subject,
                                is_compulsory=True
                            )

                        # Register selected optional subjects
                        for subject_id in selected_subject_ids:
                            subject = Subject.objects.get(id=subject_id)
                            SubjectRegistration.objects.create(
                                registration=exam_reg,
                                subject=subject,
                                is_compulsory=False
                            )

                        messages.success(request, "Student registered successfully!")
                        return redirect('register-student-exam')

                except Exception as e:
                    messages.error(request, f"An error occurred: {str(e)}")

    # Check if student is already registered (for template context)
    is_registered = False
    if student and current_year:
        is_registered = ExamRegistration.objects.filter(
            student=student, 
            exam_year=current_year
        ).exists()

    return render(request, 'school_admin/exam_registration.html', {
        'student': student,
        'core_subjects': core_subjects,
        'optional_subjects': optional_subjects,
        'is_registered': is_registered,
        'current_year': current_year,
    })