from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse
from .forms import *
from .models import *

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
                student = Student.objects.create(
                    user=user,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    birth_certificate_number=form.cleaned_data['birth_certificate_number'],
                    index_number=form.cleaned_data['index_number'],
                    # You'll need to set school and other required fields
                )
                
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

@login_required
def knec_dashboard(request):
    return render(request, 'dashboards/knec_dashboard.html')