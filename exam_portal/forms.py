from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, School, Student

class SchoolAdminRegistrationForm(UserCreationForm):
    knec_code = forms.CharField(max_length=20)
    registration_number = forms.CharField(max_length=50)
    school_name = forms.CharField(max_length=200)
    special_code = forms.CharField(max_length=100)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean(self):
        """Validate all fields together to ensure consistency"""
        cleaned_data = super().clean()
        knec_code = cleaned_data.get('knec_code')
        registration_number = cleaned_data.get('registration_number')
        school_name = cleaned_data.get('school_name')
        special_code = cleaned_data.get('special_code')
        
        # Check if all fields are provided
        if knec_code and registration_number and school_name and special_code:
            # Try to find the matching school
            try:
                school = School.objects.get(
                    knec_code=knec_code,
                    registration_number=registration_number,
                    name=school_name
                )
                
                # Verify special code
                if school.special_code != special_code:
                    self.add_error('special_code', 'Invalid special code for this school.')
                    
            except School.DoesNotExist:
                self.add_error(None, 'School information does not match our records.')
                
        return cleaned_data

class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    birth_certificate_number = forms.CharField(max_length=20, required=False)
    index_number = forms.CharField(max_length=20)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')