from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import *

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'user_type', 'phone_number', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        (_('User Type'), {'fields': ('user_type',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'user_type', 'phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('username',)

admin.site.register(User, UserAdmin)


# Custom filters
class ActiveFilter(SimpleListFilter):
    title = 'Active Status'
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return (
            ('active', 'Active'),
            ('inactive', 'Inactive'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(is_active=True)
        if self.value() == 'inactive':
            return queryset.filter(is_active=False)

class SchoolTypeFilter(SimpleListFilter):
    title = 'School Type'
    parameter_name = 'school_type'

    def lookups(self, request, model_admin):
        return School.SCHOOL_TYPE_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(school_type=self.value())

# Inline Admin Classes
class SubjectRegistrationInline(admin.TabularInline):
    model = SubjectRegistration
    extra = 1
    fields = ('subject', 'is_compulsory')
    autocomplete_fields = ['subject']

class ExamResultInline(admin.TabularInline):
    model = ExamResult
    extra = 0
    readonly_fields = ('grade', 'points')
    fields = ('subject_registration', 'marks', 'grade', 'points')

# Main Admin Classes
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'knec_code', 'special_code', 'school_type', 'county', 'is_active')
    list_filter = (ActiveFilter, SchoolTypeFilter, 'county', 'is_active')
    search_fields = ('name', 'knec_code', 'principal_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name', 'knec_code',  'special_code' , 'registration_number',
                'school_type', 'category', 'is_active'
            )
        }),
        ('Dates', {
            'fields': ('registration_date', 'established_date', 'last_inspection_date')
        }),
        ('Location', {
            'fields': (
                'county', 'sub_county', 'ward',
                'postal_address', 'physical_address',
                'gps_coordinates', 'website'
            )
        }),
        ('Contact Information', {
            'fields': (
                'phone_number', 'alternative_phone', 'email',
                'principal_name', 'principal_phone',
                'principal_email', 'principal_tsc_number'
            )
        }),
        ('Academic Information', {
            'fields': ('curriculum', 'number_of_streams')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Admin class for SchoolAdminProfile
class SchoolAdminProfileAdmin(admin.ModelAdmin):
    list_display = ('special_code', 'school', 'position', 'tsc_number', 'is_primary_admin')
    search_fields = ('special_code', 'school__name', 'position')  # Allow searching by special_code, school name, or position
    list_filter = ('is_primary_admin', 'school')  # Filter by primary admin status and school
    ordering = ('school',)  # Default ordering by school

    # Optional: Fields to display in the admin form
    fields = ('special_code', 'school', 'position', 'tsc_number', 'is_primary_admin')

    # Optional: Add inline editing for related models (e.g., showing the associated users in a school admin)
    # inlines = [SomeInlineModelAdmin]

# Register the SchoolAdminProfile model with the admin interface
admin.site.register(SchoolAdminProfile, SchoolAdminProfileAdmin)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'code')
    list_editable = ('is_active',)
    prepopulated_fields = {'code': ('name',)}

@admin.register(ExamYear)
class ExamYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'is_current')
    search_fields = ('year',)
    ordering = ('-year',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'index_number', 'full_name', 'school', 
        'current_class', 'gender', 'is_active'
    )
    list_filter = ('school', 'gender', 'current_class', ActiveFilter)
    search_fields = (
        'first_name', 'last_name', 'index_number',
        'birth_certificate_number'
    )
    readonly_fields = ('created_at', 'updated_at')
    list_select_related = ('school',)
    autocomplete_fields = ['school']
    
    fieldsets = (
        ('Personal Information', {
            'fields': (
                'first_name', 'middle_name', 'last_name',
                'birth_date', 'birth_certificate_number',
                'gender', 'nationality', 'passport_photo'
            )
        }),
        ('School Information', {
            'fields': (
                'school', 'index_number', 'admission_date',
                'current_class', 'house', 'is_boarder'
            )
        }),
        ('Contact Information', {
            'fields': (
                'email', 'phone_number', 'postal_address',
                'residential_address'
            )
        }),
        ('Previous Education', {
            'fields': (
                'previous_school', 'kcpe_year',
                'kcpe_index', 'kcpe_marks'
            )
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'

@admin.register(ExamRegistration)
class ExamRegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam_year', 'registration_date', 'is_active')
    list_filter = ('exam_year', 'is_active')
    search_fields = ('student__first_name', 'student__last_name')
    autocomplete_fields = ['student', 'exam_year']
    inlines = [SubjectRegistrationInline]
    readonly_fields = ('registration_date',)

@admin.register(SubjectRegistration)
class SubjectRegistrationAdmin(admin.ModelAdmin):
    list_display = ('registration', 'subject', 'is_compulsory')
    list_filter = ('subject', 'is_compulsory')
    search_fields = (
        'registration__student__first_name',
        'registration__student__last_name',
        'subject__name'
    )
    autocomplete_fields = ['registration', 'subject']

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = (
        'subject_registration', 'marks', 
        'grade', 'points', 'exam_year'
    )
    list_filter = ('grade',)
    search_fields = (
        'subject_registration__registration__student__first_name',
        'subject_registration__registration__student__last_name',
        'subject_registration__subject__name'
    )
    readonly_fields = ('grade', 'points')
    
    def exam_year(self, obj):
        return obj.subject_registration.registration.exam_year.year
    exam_year.short_description = 'Exam Year'

@admin.register(OverallResult)
class OverallResultAdmin(admin.ModelAdmin):
    list_display = (
        'registration', 'average_points', 
        'average_grade', 'division'
    )
    list_filter = ('average_grade', 'division')
    search_fields = (
        'registration__student__first_name',
        'registration__student__last_name'
    )
    readonly_fields = (
        'total_marks', 'average_grade', 
        'average_points', 'division'
    )
    
    def has_add_permission(self, request):
        return False  # Prevent manual addition since it's auto-calculated