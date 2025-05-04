from django import forms
from .models import *

class SchoolAdminRegistrationForm(forms.ModelForm):
    knec_code = forms.CharField(max_length=20)
    registration_number = forms.CharField(max_length=50)
    school_name = forms.CharField(max_length=200)
    special_code = forms.CharField(max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=100)
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=100)

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
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Passwords match validation
        if password1 != password2:
            self.add_error('password2', 'Passwords do not match.')

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

    def save(self, commit=True):
        """Override the save method to handle password manually"""
        user = super().save(commit=False)
        password = self.cleaned_data['password1']
        user.set_password(password)  # Set the password manually using set_password
        if commit:
            user.save()
        return user


class StudentRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    birth_certificate_number = forms.CharField(max_length=20, required=False)
    index_number = forms.CharField(max_length=20)
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=100)
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean(self):
        """Validate all fields together to ensure consistency"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Passwords match validation
        if password1 != password2:
            self.add_error('password2', 'Passwords do not match.')

        return cleaned_data

    def save(self, commit=True):
        """Override the save method to handle password manually"""
        user = super().save(commit=False)
        password = self.cleaned_data['password1']
        user.set_password(password)  # Set the password manually using set_password
        if commit:
            user.save()
        return user


class SubjectChoiceForm(forms.Form):
    optional_subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.exclude(category='CORE'),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def clean_optional_subjects(self):
        data = self.cleaned_data['optional_subjects']
        if len(data) != 4:
            raise forms.ValidationError("Please select exactly 4 optional subjects.")
        return data
    


from django import forms
from .models import Student
from django.core.validators import RegexValidator

class StudentForm(forms.ModelForm):
    phone_number = forms.CharField(
        required=False,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')]
    )
    
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'admission_date': forms.DateInput(attrs={'type': 'date'}),
            'disability_description': forms.Textarea(attrs={'rows': 3}),
            'residential_address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Special handling for boolean field
        self.fields['is_boarder'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})


    


from django import forms
from .models import School

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'
        widgets = {
            # Basic Info
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'knec_code': forms.TextInput(attrs={'class': 'form-control'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control'}),
            'special_code': forms.TextInput(attrs={'class': 'form-control'}),
            'school_type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'established_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'motto': forms.TextInput(attrs={'class': 'form-control'}),
            'mission': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'vision': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            
            # Location
            'county': forms.TextInput(attrs={'class': 'form-control'}),
            'sub_county': forms.TextInput(attrs={'class': 'form-control'}),
            'ward': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_address': forms.TextInput(attrs={'class': 'form-control'}),
            'physical_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'gps_coordinates': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),

            # Contact
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'alternative_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),

            # Principal
            'principal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'principal_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'principal_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'principal_tsc_number': forms.TextInput(attrs={'class': 'form-control'}),

            # Academic
            'curriculum': forms.TextInput(attrs={'class': 'form-control'}),
            'number_of_streams': forms.NumberInput(attrs={'class': 'form-control'}),

            # Status
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'last_inspection_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }



from django import forms
from django.contrib.auth.models import User
from .models import KNECProfile

class UserUpdateForm(forms.ModelForm):
    """Form for updating user basic information"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})


class KNECProfileUpdateForm(forms.ModelForm):
    """Form for updating KNEC profile information"""
    class Meta:
        model = KNECProfile
        fields = ['designation', 'department', 'phone_number', 'office_location', 'responsibilities']
        
    def __init__(self, *args, **kwargs):
        super(KNECProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['designation'].widget.attrs.update({'class': 'form-control'})
        self.fields['department'].widget.attrs.update({'class': 'form-select'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['office_location'].widget.attrs.update({'class': 'form-control'})
        self.fields['responsibilities'].widget.attrs.update({'class': 'form-control'})


class ProfilePictureUpdateForm(forms.ModelForm):
    """Form for updating profile picture"""
    class Meta:
        model = KNECProfile
        fields = ['profile_picture']
        
    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            if profile_picture.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file size must be less than 5MB")
            
            valid_extensions = ['jpg', 'jpeg', 'png']
            ext = profile_picture.name.split('.')[-1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError("Only JPG, JPEG, and PNG files are allowed")
        
        return profile_picture


class KNECSettingsUpdateForm(forms.ModelForm):
    """Form for updating KNEC profile settings and preferences"""
    class Meta:
        model = KNECProfile
        fields = ['system_notifications', 'security_alerts', 'exam_updates', 'theme', 'results_per_page']
        
    def __init__(self, *args, **kwargs):
        super(KNECSettingsUpdateForm, self).__init__(*args, **kwargs)
        # Display checkboxes for notification settings
        self.fields['system_notifications'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['security_alerts'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['exam_updates'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        
        # Display select dropdown for theme and results per page
        self.fields['theme'].widget = forms.Select(attrs={'class': 'form-select'}, choices=KNECProfile.THEME_CHOICES)
        self.fields['results_per_page'].widget = forms.Select(
            attrs={'class': 'form-select'},
            choices=[(10, '10'), (25, '25'), (50, '50'), (100, '100')]
        )


class SecuritySettingsForm(forms.ModelForm):
    """Form for updating security settings"""
    class Meta:
        model = KNECProfile
        fields = ['two_factor_enabled', 'login_alerts', 'session_timeout']
        
    def __init__(self, *args, **kwargs):
        super(SecuritySettingsForm, self).__init__(*args, **kwargs)
        # Use switch-style checkboxes
        self.fields['two_factor_enabled'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['login_alerts'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['session_timeout'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})


# forms.py - Django forms for KNEC Resources

from django import forms
from .models import Resource, ResourceType, Category

class ResourceForm(forms.ModelForm):
    """Form for creating and updating resources"""
    
    class Meta:
        model = Resource
        fields = [
            'title', 'description', 'file', 'thumbnail',
            'resource_type', 'category', 'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'resource_type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class ResourceFilterForm(forms.Form):
    """Form for filtering resources"""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'search-input',
            'placeholder': 'Search resources...'
        })
    )
    
    resource_type = forms.ModelChoiceField(
        queryset=ResourceType.objects.all(),
        required=False,
        empty_label="All Types",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    STATUS_CHOICES = [
        ('', 'All Statuses'),
        ('published', 'Published'),
        ('draft', 'Draft'),
        ('archived', 'Archived'),
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class ImportResourceForm(forms.Form):
    """Form for importing resources from a file"""
    
    import_file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        help_text="Upload a CSV or Excel file with resource information."
    )
    
    FILE_TYPE_CHOICES = [
        ('csv', 'CSV File'),
        ('excel', 'Excel File'),
    ]
    
    file_type = forms.ChoiceField(
        choices=FILE_TYPE_CHOICES,
        widget=forms.RadioSelect(),
        initial='csv',
    )