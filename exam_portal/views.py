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



from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

def student_list(request):
    # Search functionality
    search_query = request.GET.get('search', '')
    
    # Base queryset
    students = Student.objects.all().order_by('-created_at')
    
    # Apply search filter if query exists
    if search_query:
        students = students.filter(
            Q(index_number__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(admision_number__icontains=search_query))
    
    # Pagination
    paginator = Paginator(students, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'students/admin/student_list.html', context)

def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, f"Student {student.index_number} created successfully!")
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm()
    
    context = {
        'form': form,
        'title': 'Add New Student',
    }
    return render(request, 'students/admin/student_form.html', context)

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    context = {
        'student': student,
    }
    return render(request, 'students/admin/student_detail.html', context)

def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            updated_student = form.save()
            messages.success(request, f"Student {updated_student.index_number} updated successfully!")
            return redirect('student_detail', pk=updated_student.pk)
    else:
        form = StudentForm(instance=student)
    
    context = {
        'form': form,
        'title': f'Edit {student.index_number}',
        'student': student,
    }
    return render(request, 'students/admin/student_form.html', context)

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        index_number = student.index_number
        student.delete()
        messages.success(request, f"Student {index_number} deleted successfully!")
        return redirect('student_list')
    
    context = {
        'student': student,
    }
    return render(request, 'students/admin/student_confirm_delete.html', context)

def student_search(request):
    search_term = request.GET.get('q', '')
    
    if search_term:
        students = Student.objects.filter(
            Q(index_number__icontains=search_term) |
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(admision_number__icontains=search_term)
        ).order_by('-created_at')[:10]
    else:
        students = Student.objects.none()
    
    context = {
        'students': students,
        'search_term': search_term,
    }
    return render(request, 'students/admin/student_search_results.html', context)


# school admin crud operations

from functools import wraps
from django.shortcuts import redirect

def school_admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type != 2:
            return redirect('login')
        
        try:
            admin_profile = SchoolAdminProfile.objects.get(special_code=request.user.username)
            request.school = admin_profile.school
        except SchoolAdminProfile.DoesNotExist:
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def school_student_list(request):
    # Authentication and permission check
    if not request.user.is_authenticated or request.user.user_type != 2:
        return redirect('login')

    try:
        # Get the SchoolAdminProfile using the special_code which matches the username
        admin_profile = SchoolAdminProfile.objects.get(special_code=request.user.username)
        school = admin_profile.school
    except SchoolAdminProfile.DoesNotExist:
        return redirect('login')

    # Get search query from GET request
    search_query = request.GET.get('search', '')

    # Filter students based on search query and school
    students = Student.objects.filter(
        school=school,
        is_active=True
    ).filter(
        Q(first_name__icontains=search_query) |
        Q(last_name__icontains=search_query) |
        Q(index_number__icontains=search_query) |
        Q(admision_number__icontains=search_query)
    ).order_by('first_name')

    # Paginate results
    paginator = Paginator(students, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'students': students,  # Optional: not used in template directly
        'page_obj': page_obj,
        'search_query': search_query,
        'school': school
    }
    return render(request, 'students/school_admin/student_list.html', context)


def school_student_detail(request, pk):
    # Authentication and permission check
    if not request.user.is_authenticated or request.user.user_type != 2:
        return redirect('login')

    try:
        admin_profile = SchoolAdminProfile.objects.get(special_code=request.user.username)
        school = admin_profile.school
    except SchoolAdminProfile.DoesNotExist:
        return redirect('login')

    # Ensure the student belongs to this admin's school
    student = get_object_or_404(Student, pk=pk, school=school)

    context = {
        'student': student,
    }
    return render(request, 'students/admin/student_detail.html', context)



def school_student_create(request):
    # Authentication and permission check
    if not request.user.is_authenticated or request.user.user_type != 2:
        return redirect('login')
    
    try:
        admin_profile = SchoolAdminProfile.objects.get(special_code=request.user.username)
        school = admin_profile.school
    except SchoolAdminProfile.DoesNotExist:
        return redirect('login')
    
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.school = school
            
            # Generate admission number if not provided
            if not student.admision_number:
                last_student = Student.objects.filter(school=school).order_by('-id').first()
                last_number = int(last_student.admision_number) if last_student else 0
                student.admision_number = str(last_number + 1).zfill(4)
            
            student.save()
            messages.success(request, 'Student created successfully!')
            return redirect('student_list')
    else:
        form = StudentForm(initial={'school': school})
    
    context = {
        'form': form,
        'school': school
    }
    return render(request, 'students/school_admin/student_form.html', context)

def school_student_update(request, pk):
    # Authentication and permission check
    if not request.user.is_authenticated or request.user.user_type != 2:
        return redirect('login')
    
    try:
        admin_profile = SchoolAdminProfile.objects.get(special_code=request.user.username)
        school = admin_profile.school
    except SchoolAdminProfile.DoesNotExist:
        return redirect('login')
    
    student = get_object_or_404(Student, pk=pk)
    
    # Verify the student belongs to the admin's school
    if student.school != school:
        messages.error(request, "You can only update students from your school.")
        return redirect('student_list')
    
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    
    context = {
        'form': form,
        'student': student,
        'school': school
    }
    return render(request, 'students/school_admin/student_form.html', context)


def school_student_delete(request, pk):
    # Authentication and permission check
    if not request.user.is_authenticated or request.user.user_type != 2:
        return redirect('login')
    
    try:
        admin_profile = SchoolAdminProfile.objects.get(special_code=request.user.username)
        school = admin_profile.school
    except SchoolAdminProfile.DoesNotExist:
        return redirect('login')
    
    student = get_object_or_404(Student, pk=pk)
    
    # Verify the student belongs to the admin's school
    if student.school != school:
        messages.error(request, "You can only delete students from your school.")
        return redirect('student_list')
    
    if request.method == 'POST':
        # Soft delete by setting is_active to False
        student.is_active = False
        student.save()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')
    
    context = {
        'student': student
    }
    return render(request, 'students/school_admin/student_confirm_delete.html', context)
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.urls import reverse
from urllib.parse import urlencode
from django.core.exceptions import ValidationError

from .models import Student, ExamYear, ExamRegistration, ExamResult


class EnterStudentMarksView(View):
    template_name = 'exams/enter_student_marks.html'

    def get(self, request):
        context = {}
        index_number = request.GET.get('index_number', '').strip()

        if index_number:
            try:
                current_year = ExamYear.objects.get(is_current=True)
                student = Student.objects.get(index_number=index_number)
                registration = student.registrations.get(exam_year=current_year)
                subject_registrations = registration.subjects.all()

                context.update({
                    'student': student,
                    'subject_registrations': subject_registrations,
                    'current_year': current_year,
                })

            except Student.DoesNotExist:
                messages.error(request, 'Student with this index number was not found.')
            except ExamYear.DoesNotExist:
                messages.error(request, 'No current exam year is set.')
            except ExamRegistration.DoesNotExist:
                messages.error(request, 'Student is not registered for the current exam year.')
            except Exception as e:
                messages.error(request, f'Unexpected error: {str(e)}')

        return render(request, self.template_name, context)

    def post(self, request):
        index_number = request.POST.get('index_number', '').strip()
        if not index_number:
            messages.error(request, 'Index number is required.')
            return redirect(reverse('enter_student_marks'))

        try:
            # Debug: Print POST data for verification
            print("POST Data Received:", request.POST)

            current_year = ExamYear.objects.get(is_current=True)
            student = Student.objects.get(index_number=index_number)
            registration = student.registrations.get(exam_year=current_year)

            # Process each subject mark
            for subject_reg in registration.subjects.all():
                mark_field = f'mark_{subject_reg.id}'
                mark_value = request.POST.get(mark_field, '').strip()

                if not mark_value:
                    continue  # Skip if no mark provided

                try:
                    # Validate and convert mark
                    mark = int(mark_value)
                    if mark < 0 or mark > 100:
                        raise ValidationError(f"Mark for {subject_reg.subject.name} must be between 0 and 100.")

                    # Modified approach: Get or create result then explicitly save changes
                    result, created = ExamResult.objects.get_or_create(subject_registration=subject_reg)
                    result.marks = mark
                    # Force save to trigger the grade and points calculation
                    result.save()

                except ValueError:
                    messages.error(request, f"Invalid mark format for {subject_reg.subject.name}. Must be a whole number.")
                except ValidationError as ve:
                    messages.error(request, str(ve))
                except Exception as e:
                    messages.error(request, f"Error processing {subject_reg.subject.name}: {str(e)}")

            messages.success(request, 'Marks saved successfully!')

        except ExamYear.DoesNotExist:
            messages.error(request, 'No current exam year is set.')
        except Student.DoesNotExist:
            messages.error(request, 'Student with this index number was not found.')
        except ExamRegistration.DoesNotExist:
            messages.error(request, 'Student is not registered for the current exam year.')
        except Exception as e:
            messages.error(request, f'System error: {str(e)}')
            # Log full error for debugging
            import traceback
            print(f"Full Error Traceback:\n{traceback.format_exc()}")

        # Redirect back with the index number
        return redirect(f"{reverse('enter_student_marks')}?{urlencode({'index_number': index_number })}")
    



from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.db.models import Avg, Sum
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Student, ExamYear, ExamRegistration, SubjectRegistration, ExamResult, OverallResult


class StudentPerformanceView(LoginRequiredMixin, View):
    template_name = 'exams/search_student_performance.html'
    
    def get(self, request):
        context = {}
        index_number = request.GET.get('index_number', '').strip()
        exam_year_id = request.GET.get('exam_year', None)
        
        # Get all exam years for the dropdown
        exam_years = ExamYear.objects.all().order_by('-year')
        context['exam_years'] = exam_years
        
        if index_number:
            try:
                student = Student.objects.get(index_number=index_number)
                context['student'] = student
                
                # Get all registrations for this student
                registrations = ExamRegistration.objects.filter(student=student)
                
                if not registrations.exists():
                    messages.error(request, f"No exam registrations found for student {index_number}")
                    return render(request, self.template_name, context)
                
                # If year is specified, filter by that year
                if exam_year_id:
                    try:
                        exam_year = ExamYear.objects.get(id=exam_year_id)
                        registrations = registrations.filter(exam_year=exam_year)
                    except ExamYear.DoesNotExist:
                        messages.error(request, "Selected exam year not found")
                        return render(request, self.template_name, context)
                
                # Get the latest registration if multiple exist
                registration = registrations.order_by('-exam_year__year').first()
                context['registration'] = registration
                context['exam_year'] = registration.exam_year
                
                # Get all subject registrations and their results
                subject_registrations = SubjectRegistration.objects.filter(
                    registration=registration
                ).select_related('subject', 'result')
                
                # Prepare subject results for display
                subject_results = []
                total_marks = 0
                total_points = 0
                valid_results_count = 0
                
                for subject_reg in subject_registrations:
                    result_data = {
                        'subject': subject_reg.subject.name,
                        'code': subject_reg.subject.code,
                        'marks': None,
                        'grade': None,
                        'points': None
                    }
                    
                    try:
                        result = subject_reg.result
                        result_data['marks'] = result.marks
                        result_data['grade'] = result.grade
                        result_data['points'] = result.points
                        
                        # Only count if marks and points are not None
                        if result.marks is not None and result.points is not None:
                            total_marks += result.marks
                            total_points += result.points
                            valid_results_count += 1
                    except ExamResult.DoesNotExist:
                        pass  # Leave as None if no result exists
                    
                    subject_results.append(result_data)
                
                context['subject_results'] = subject_results
                
                # Calculate averages
                if valid_results_count > 0:
                    context['total_marks'] = total_marks
                    context['avg_marks'] = round(total_marks / valid_results_count, 2)
                    context['total_points'] = total_points
                    context['avg_points'] = round(total_points / valid_results_count, 2)
                
                # Get overall result if exists
                try:
                    overall_result = OverallResult.objects.get(registration=registration)
                    context['overall_result'] = overall_result
                except OverallResult.DoesNotExist:
                    # Calculate on the fly if no saved result exists
                    if valid_results_count > 0:
                        avg_points = total_points / valid_results_count
                        
                        # Get the grade that corresponds to this point average
                        # (This is simplified - you'd need to match according to your grading system)
                        grading_system = registration.exam_year.grading_system
                        mean_grade = None
                        division = None
                        
                        if isinstance(grading_system, dict):
                            for grade, info in grading_system.items():
                                if info.get('points') == round(avg_points):
                                    mean_grade = grade
                                    # Determine division based on points
                                    points = info.get('points', 0)
                                    if points >= 10:
                                        division = "Division 1"
                                    elif points >= 8:
                                        division = "Division 2"
                                    elif points >= 6:
                                        division = "Division 3"
                                    elif points >= 2:
                                        division = "Division 4"
                                    else:
                                        division = "Division 5"
                                    
                                    break
                        elif isinstance(grading_system, list):
                            for grade_info in grading_system:
                                if grade_info.get('points') == round(avg_points):
                                    mean_grade = grade_info.get('grade', '')
                                    division = grade_info.get('division', '')
                                    break
                        
                        context['mean_grade'] = mean_grade
                        context['division'] = division
                
            except Student.DoesNotExist:
                messages.error(request, f"Student with index number {index_number} not found")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                # Log the full error for debugging
                import traceback
                print(f"Error in StudentPerformanceView:\n{traceback.format_exc()}")
        
        return render(request, self.template_name, context)
    


# from django.shortcuts import render, get_object_or_404
# from django.views import View
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# from django.utils import timezone
# import weasyprint
# #from io import BytesIO

# from .models import Student, ExamRegistration, SubjectRegistration, ExamResult, OverallResult


# class PrintStudentPerformanceView(LoginRequiredMixin, View):
#     """View for generating a printable PDF of student performance"""
    
#     def get(self, request, registration_id):
#         # Get the exam registration
#         registration = get_object_or_404(ExamRegistration, id=registration_id)
#         student = registration.student
#         exam_year = registration.exam_year
        
#         # Get all subject registrations and their results
#         subject_registrations = SubjectRegistration.objects.filter(
#             registration=registration
#         ).select_related('subject', 'result')
        
#         # Prepare subject results for display
#         subject_results = []
#         total_marks = 0
#         total_points = 0
#         valid_results_count = 0
        
#         for subject_reg in subject_registrations:
#             result_data = {
#                 'subject': subject_reg.subject.name,
#                 'code': subject_reg.subject.code,
#                 'marks': None,
#                 'grade': None,
#                 'points': None
#             }
            
#             try:
#                 result = subject_reg.result
#                 result_data['marks'] = result.marks
#                 result_data['grade'] = result.grade
#                 result_data['points'] = result.points
                
#                 # Only count if marks and points are not None
#                 if result.marks is not None and result.points is not None:
#                     total_marks += result.marks
#                     total_points += result.points
#                     valid_results_count += 1
#             except ExamResult.DoesNotExist:
#                 pass  # Leave as None if no result exists
            
#             subject_results.append(result_data)
        
#         # Calculate averages
#         avg_marks = None
#         avg_points = None
#         if valid_results_count > 0:
#             avg_marks = round(total_marks / valid_results_count, 2)
#             avg_points = round(total_points / valid_results_count, 2)
        
#         # Get overall result if exists
#         try:
#             overall_result = OverallResult.objects.get(registration=registration)
#         except OverallResult.DoesNotExist:
#             overall_result = None
            
#         # Determine mean grade if no overall result exists
#         mean_grade = None
#         division = None
#         if overall_result is None and valid_results_count > 0:
#             avg_points_value = total_points / valid_results_count
            
#             # Get the grade that corresponds to this point average
#             grading_system = registration.exam_year.grading_system
            
#             if isinstance(grading_system, dict):
#                 for grade, info in grading_system.items():
#                     if info.get('points') == round(avg_points_value):
#                         mean_grade = grade
#                         # Determine division based on points
#                         points = info.get('points', 0)
#                         if points >= 10:
#                             division = "Division 1"
#                         elif points >= 8:
#                             division = "Division 2"
#                         elif points >= 6:
#                             division = "Division 3"
#                         elif points >= 2:
#                             division = "Division 4"
#                         else:
#                             division = "Division 5"
#                         break
#             elif isinstance(grading_system, list):
#                 for grade_info in grading_system:
#                     if grade_info.get('points') == round(avg_points_value):
#                         mean_grade = grade_info.get('grade', '')
#                         division = grade_info.get('division', '')
#                         break
        
#         # Prepare context for PDF template
#         context = {
#             'student': student,
#             'registration': registration,
#             'exam_year': exam_year,
#             'subject_results': subject_results,
#             'total_marks': total_marks,
#             'avg_marks': avg_marks,
#             'total_points': total_points,
#             'avg_points': avg_points,
#             'overall_result': overall_result,
#             'mean_grade': mean_grade if not overall_result else overall_result.average_grade,
#             'division': division if not overall_result else overall_result.division,
#             'generated_date': timezone.now(),
#             'school': student.school,
#         }
        
#         # Render HTML template
#         html_string = render_to_string('exams/print_student_performance.html', context)
        
#         # Generate PDF
#         pdf_file = BytesIO()
#         weasyprint.HTML(string=html_string).write_pdf(pdf_file)
        
#         # Create HTTP response with PDF
#         response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="report_card_{student.index_number}_{exam_year.year}.pdf"'
        
#         return response

# views.py (updated)
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Student, ExamRegistration, SubjectRegistration, ExamResult

@login_required
def student_performance_view(request, student_id):
    # Get the student or return 404
    student = get_object_or_404(Student, pk=student_id)
    
    # Verify the requesting user has permission to view this student's performance
    if not request.user.is_superuser:
        if hasattr(request.user, 'student_profile'):
            if request.user.student_profile.student.id != student.id:
                return render(request, '403.html', status=403)
        elif hasattr(request.user, 'school_admin_profile'):
            if request.user.school_admin_profile.school.id != student.school.id:
                return render(request, '403.html', status=403)
    
    # Get all exam registrations for this student
    exam_registrations = ExamRegistration.objects.filter(student=student).select_related(
        'exam_year'
    ).prefetch_related(
        'subjects__subject',
        'subjects__result'
    ).order_by('-exam_year__year')
    
    # Prepare the performance data structure
    performance_data = []
    for registration in exam_registrations:
        subjects_data = []
        total_points = 0
        total_marks = 0
        total_subjects = 0
        
        for subject_reg in registration.subjects.all():
            result = None
            if hasattr(subject_reg, 'result'):
                result = subject_reg.result
                if result.points and result.marks:
                    total_points += result.points
                    total_marks += result.marks
                    total_subjects += 1
            
            subjects_data.append({
                'subject': subject_reg.subject,
                'is_compulsory': subject_reg.is_compulsory,
                'marks': result.marks if result else None,
                'grade': result.grade if result else None,
                'points': result.points if result else None,
            })
        
        # Calculate mean grade and mean marks if there are results
        mean_grade = None
        mean_points = None
        mean_marks = None
        if total_subjects > 0:
            mean_points = total_points / total_subjects
            mean_marks = total_marks / total_subjects
            # Simple grade calculation (customize based on your grading system)
            if mean_points >= 11: mean_grade = 'A'
            elif mean_points >= 8: mean_grade = 'B'
            elif mean_points >= 5: mean_grade = 'C'
            elif mean_points >= 3: mean_grade = 'D'
            else: mean_grade = 'E'
            
        performance_data.append({
            'exam_year': registration.exam_year,
            'subjects': subjects_data,
            'total_points': total_points,
            'total_marks': total_marks,
            'mean_points': mean_points,
            'mean_marks': mean_marks,
            'mean_grade': mean_grade,
            'is_active': registration.is_active,
        })
    
    context = {
        'student': student,
        'performance_data': performance_data,
        'school': student.school,
    }
    
    return render(request, 'exams/student_performance.html', context)
from django.db.models import Sum, Count, Q, Value
from django.db.models.functions import Concat
from django.db.models import Sum, Count, Q, Value
from django.db.models.functions import Concat
from django.core.paginator import Paginator

def current_year_performance(request):
    # Get current exam year with grading system
    current_year = ExamYear.objects.filter(is_current=True).first()
    if not current_year:
        return render(request, 'exams/current_performance.html', {
            'error': 'No current exam year configured'
        })

    # Get the grading system for this year
    grading_system = current_year.grading_system
    
    # Base query - now focusing on marks (scores) instead of points
    queryset = ExamRegistration.objects.filter(
        exam_year=current_year
    ).select_related(
        'student', 'student__school'
    ).prefetch_related(
        'subjects__result'
    ).annotate(
        total_marks=Sum('subjects__result__marks'),
        subject_count=Count('subjects'),
        full_name=Concat('student__first_name', Value(' '), 'student__last_name')
    ).exclude(total_marks=None)

    # We won't order the queryset yet as we'll need to calculate points first
    # and then sort the final list with our custom ordering

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(student__first_name__icontains=search_query) |
            Q(student__last_name__icontains=search_query) |
            Q(student__index_number__icontains=search_query) |
            Q(student__school__name__icontains=search_query)
        )

    # Process all students to add their points
    students_with_points = []
    for student in queryset:
        # Calculate total points based on actual subject grades
        total_points = 0
        subject_count = 0
        
        if hasattr(student, 'subjects'):
            for subject in student.subjects.all():
                if hasattr(subject, 'result') and subject.result and subject.result.marks is not None:
                    subject_count += 1
                    for grade, criteria in grading_system.items():
                        if criteria['min_score'] <= subject.result.marks <= criteria['max_score']:
                            total_points += criteria['points']
                            break
        
        # Calculate mean points (average points per subject)
        mean_points = total_points / subject_count if subject_count > 0 else 0
        
        # Calculate mean marks (average score)
        mean_marks = student.total_marks / student.subject_count if student.subject_count > 0 else 0
        
        # Calculate mean grade based on year-specific grading system
        mean_grade = 'E'  # Default grade
        grade_comment = ''
        
        if isinstance(grading_system, dict):
            for grade, criteria in grading_system.items():
                min_score = criteria.get('min_score', 0)
                max_score = criteria.get('max_score', 100)
                if min_score <= mean_marks <= max_score:
                    mean_grade = grade
                    grade_comment = criteria.get('comment', '')
                    break
        
        students_with_points.append({
            'data': student,
            'total_marks': student.total_marks,
            'total_points': total_points,
            'mean_points': mean_points,
            'mean_grade': mean_grade,
            'full_name': student.full_name,
            'subject_count': subject_count  # Add subject count for reference
        })
    
    # Sort students by: 1) total_points (desc), 2) total_marks (desc), 3) full_name (asc)
    sorted_students = sorted(
        students_with_points,
        key=lambda x: (-x['total_points'], -x['total_marks'], x['full_name'])
    )
    
    # Assign ranks based on points and marks (students with same points and marks get the same rank)
    ranked_students = []
    current_rank = 0
    prev_points = None
    prev_marks = None
    
    for i, student in enumerate(sorted_students, start=1):
        if student['total_points'] != prev_points or student['total_marks'] != prev_marks:
            current_rank = i
        
        student['rank'] = current_rank
        ranked_students.append(student)
        
        prev_points = student['total_points']
        prev_marks = student['total_marks']
    
    # Pagination (after sorting and ranking)
    paginator = Paginator(ranked_students, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'current_year': current_year,
        'page_obj': page_obj,
        'ranked_students': page_obj.object_list,  # Now page_obj contains the ranked_students
        'search_query': search_query,
    }
    return render(request, 'exams/current_performance.html', context)


from django.db.models import Avg, Count, Q, Sum
from django.db.models.functions import Coalesce
from django.db.models import FloatField

from django.db.models import Avg, Count, Q, Sum
from django.db.models.functions import Coalesce
from django.db.models import FloatField, Value

def school_ranking(request):
    # Get the current exam year
    current_year = ExamYear.objects.filter(is_current=True).first()
    if not current_year:
        return render(request, 'exams/ranking/school_rankings.html', {
            'error': 'No current exam year configured'
        })
    
    # Base queryset - schools with students who have exam results
    queryset = School.objects.filter(
        students__registrations__exam_year=current_year,
        students__registrations__subjects__result__isnull=False
    ).distinct()
    
    # Annotate with mean points and student count
    queryset = queryset.annotate(
        mean_points=Coalesce(
            Avg(
                'students__registrations__subjects__result__points',
                filter=Q(
                    students__registrations__exam_year=current_year,
                    students__registrations__subjects__result__points__isnull=False
                ),
                output_field=FloatField()
            ),
            Value(0.0, output_field=FloatField())
        ),
        student_count=Count(
            'students__registrations',
            filter=Q(
                students__registrations__exam_year=current_year,
                students__registrations__subjects__result__isnull=False
            ),
            distinct=True
        )
    ).order_by('-mean_points', '-student_count', 'name')
    
    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(queryset, 20)  # 20 schools per page
    page_obj = paginator.get_page(page_number)
    
    # Add ranking to schools
    ranked_schools = []
    for rank, school in enumerate(page_obj, start=1):
        school.rank = rank
        ranked_schools.append(school)
    
    context = {
        'current_year': current_year,
        'schools': ranked_schools,
        'page_obj': page_obj,
    }
    
    return render(request, 'exams/ranking/school_rankings.html', context)


#analysis view
from django.shortcuts import render
from django.db.models import Count, Avg, Sum, Case, When, IntegerField, F, Q
from .models import (
    School, Student, ExamResult, SubjectRegistration, 
    ExamYear, Subject, ExamRegistration
)
from django.db.models.functions import Coalesce

def performance_dashboard(request):
    # Get current and previous exam years
    current_year = ExamYear.objects.filter(is_current=True).first()
    previous_years = ExamYear.objects.filter(is_current=False).order_by('-year')
    
    if not current_year:
        return render(request, 'dashboard/no_current_year.html')
    
    # Performance trend comparison
    yearly_performance = ExamResult.objects.values(
        'subject_registration__registration__exam_year__year'
    ).annotate(
        year=F('subject_registration__registration__exam_year__year'),
        avg_points=Avg('points'),
        avg_marks=Avg('marks')
    ).order_by('year')
    
    # Gender performance comparison for current year
    gender_performance = ExamResult.objects.filter(
        subject_registration__registration__exam_year=current_year
    ).values(
        'subject_registration__registration__student__gender'
    ).annotate(
        gender=F('subject_registration__registration__student__gender'),
        avg_points=Avg('points'),
        avg_marks=Avg('marks'),
        count=Count('id')
    )
    
    # Top 5 schools current year vs previous year
    current_top_schools = School.objects.annotate(
        avg_points=Avg(
            'students__registrations__subjects__result__points',
            filter=Q(students__registrations__exam_year=current_year)
    )).order_by('-avg_points')[:5]
    
    previous_top_schools = School.objects.annotate(
        avg_points=Avg(
            'students__registrations__subjects__result__points',
            filter=Q(students__registrations__exam_year__is_current=False)
        )
    ).order_by('-avg_points')[:5]
    
    # Top performing student and comparison
    current_top_student = Student.objects.annotate(
        total_points=Coalesce(Sum(
            'registrations__subjects__result__points',
            filter=Q(registrations__exam_year=current_year)), 0)
    ).order_by('-total_points').first()
    
    if current_top_student:
        top_student_comparison = {
            'current_points': current_top_student.total_points,
            'school_avg': ExamResult.objects.filter(
                subject_registration__registration__exam_year=current_year,
                subject_registration__registration__student__school=current_top_student.school
            ).aggregate(avg=Avg('points'))['avg'],
            'national_avg': ExamResult.objects.filter(
                subject_registration__registration__exam_year=current_year
            ).aggregate(avg=Avg('points'))['avg']
        }
    else:
        top_student_comparison = None
    
    # Registration statistics
    registration_stats = {
        'current_total': ExamRegistration.objects.filter(exam_year=current_year).count(),
        'current_male': ExamRegistration.objects.filter(
            exam_year=current_year,
            student__gender='M'
        ).count(),
        'current_female': ExamRegistration.objects.filter(
            exam_year=current_year,
            student__gender='F'
        ).count(),
    }
    
    # Subject performance comparisons
    current_subjects = SubjectRegistration.objects.filter(
        registration__exam_year=current_year
    ).values(
        'subject__name'
    ).annotate(
        subject_name=F('subject__name'),
        avg_points=Avg('result__points'),
        avg_marks=Avg('result__marks'),
        male_avg=Avg(
            'result__points',
            filter=Q(registration__student__gender='M')
        ),
        female_avg=Avg(
            'result__points',
            filter=Q(registration__student__gender='F')
        )
    ).order_by('-avg_points')
    
    previous_subjects = SubjectRegistration.objects.filter(
        registration__exam_year__is_current=False
    ).values(
        'subject__name'
    ).annotate(
        subject_name=F('subject__name'),
        avg_points=Avg('result__points')
    ).order_by('-avg_points')
    
    context = {
        'current_year': current_year,
        'previous_years': previous_years,
        
        # Performance trends
        'yearly_performance': list(yearly_performance),
        
        # Gender comparisons
        'gender_performance': list(gender_performance),
        
        # School comparisons
        'current_top_schools': current_top_schools,
        'previous_top_schools': previous_top_schools,
        
        # Student comparisons
        'current_top_student': current_top_student,
        'top_student_comparison': top_student_comparison,
        
        # Registration stats
        'registration_stats': registration_stats,
        
        # Subject comparisons
        'current_subjects': list(current_subjects),
        'previous_subjects': list(previous_subjects),
    }
    
    return render(request, 'dashboards/performance_dashboard.html', context)


from django.db.models import Count, Sum, Avg, F
from django.shortcuts import render

def top_students_view(request):
    # Get filter parameters
    selected_year = request.GET.get('year')
    selected_school = request.GET.get('school')
    
    # Base queryset - don't slice yet
    top_students = ExamResult.objects.values(
        'subject_registration__registration__student',
        'subject_registration__registration__student__first_name',
        'subject_registration__registration__student__last_name',
        'subject_registration__registration__student__gender',
        'subject_registration__registration__student__school__name',
        'subject_registration__registration__student__school__id',
        'subject_registration__registration__exam_year__year',
        'subject_registration__registration__exam_year'
    ).annotate(
        total_points=Sum('points'),
        mean_grade=Avg('points')  # This would need adjustment to calculate actual mean grade
    ).order_by('-total_points')
    
    # Apply filters before slicing
    if selected_year:
        top_students = top_students.filter(
            subject_registration__registration__exam_year__year=selected_year
        )
    
    if selected_school:
        top_students = top_students.filter(
            subject_registration__registration__student__school__id=selected_school
        )
    
    # Now take the top 100 after filtering
    top_students = top_students[:100]
    
    # Get all years for filter dropdown
    all_years = ExamYear.objects.values('year').distinct().order_by('-year')
    
    # Get all schools for filter dropdown
    all_schools = School.objects.all().order_by('name')
    
    # Gender analysis - create a new queryset for this
    gender_queryset = ExamResult.objects.filter(
        subject_registration__registration__student__in=[s['subject_registration__registration__student'] for s in top_students]
    )
    
    gender_counts = gender_queryset.values(
        'subject_registration__registration__student__gender'
    ).annotate(
        count=Count('subject_registration__registration__student', distinct=True)
    )
    
    male_count = next(
        (item['count'] for item in gender_counts if item['subject_registration__registration__student__gender'] == 'M'), 
        0
    )
    female_count = next(
        (item['count'] for item in gender_counts if item['subject_registration__registration__student__gender'] == 'F'), 
        0
    )
    total_count = male_count + female_count
    male_percentage = round((male_count / total_count) * 100, 1) if total_count > 0 else 0
    female_percentage = round((female_count / total_count) * 100, 1) if total_count > 0 else 0
    
    # School analysis - create a new queryset
    school_queryset = ExamResult.objects.filter(
        subject_registration__registration__student__in=[s['subject_registration__registration__student'] for s in top_students]
    )
    
    top_schools = school_queryset.values(
        'subject_registration__registration__student__school__name',
        'subject_registration__registration__student__school__id'
    ).annotate(
        count=Count('subject_registration__registration__student', distinct=True)
    ).order_by('-count')[:5]
    
    # Grade distribution - create a new queryset
    grade_queryset = ExamResult.objects.filter(
        subject_registration__registration__student__in=[s['subject_registration__registration__student'] for s in top_students]
    )
    
    grade_distribution = grade_queryset.values(
        'grade'  # Assuming you have a grade field
    ).annotate(
        count=Count('subject_registration__registration__student', distinct=True)
    ).order_by('grade')
    
    # Transform data for template
    students = [
        {
            'student__id': s['subject_registration__registration__student'],
            'student__first_name': s['subject_registration__registration__student__first_name'],
            'student__last_name': s['subject_registration__registration__student__last_name'],
            'student__gender': s['subject_registration__registration__student__gender'],
            'student__school__name': s['subject_registration__registration__student__school__name'],
            'student__school__id': s['subject_registration__registration__student__school__id'],
            'total_points': s['total_points'],
            'mean_grade': s['mean_grade'],
            'exam_year__year': s['subject_registration__registration__exam_year__year']
        }
        for s in top_students
    ]
    
    context = {
        'students': students,
        'all_years': all_years,
        'all_schools': all_schools,
        'selected_year': selected_year,
        'selected_school': selected_school,
        'male_count': male_count,
        'female_count': female_count,
        'male_percentage': male_percentage,
        'female_percentage': female_percentage,
        'top_schools': top_schools,
        'grade_distribution': grade_distribution,
    }
    
    return render(request, 'dashboards/top_students.html', context)