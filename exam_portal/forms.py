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