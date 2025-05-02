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
    


from django.utils import timezone  # Add this import
from django.contrib import admin
from django.utils.html import format_html
from .models import ExamPaperArchive, PaperReleaseSchedule

class ExamPaperArchiveAdmin(admin.ModelAdmin):
    list_display = ('paper_code', 'subject', 'exam_year', 'paper_type', 
                    'is_confidential', 'approved', 'uploaded_by', 'date_uploaded')
    list_filter = ('exam_year', 'subject', 'paper_type', 'is_confidential', 'approved')
    search_fields = ('paper_code', 'paper_title', 'subject__name')
    readonly_fields = ('date_uploaded', 'uploaded_by', 'approval_date')
    list_per_page = 20
    actions = ['approve_papers', 'mark_as_confidential']
    raw_id_fields = ('subject', 'exam_year')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('exam_year', 'subject', 'paper_type', 'paper_code', 'paper_title')
        }),
        ('Paper File', {
            'fields': ('paper_file', 'is_confidential')
        }),
        ('Approval Status', {
            'fields': ('approved', 'approved_by', 'approval_date')
        }),
        ('Upload Information', {
            'fields': ('uploaded_by', 'date_uploaded'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(uploaded_by=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)
    
    def approve_papers(self, request, queryset):
        updated = queryset.update(
            approved=True,
            approved_by=request.user,
            approval_date=timezone.now()
        )
        self.message_user(request, f"{updated} papers were approved.")
    approve_papers.short_description = "Approve selected papers"
    
    def mark_as_confidential(self, request, queryset):
        updated = queryset.update(is_confidential=True)
        self.message_user(request, f"{updated} papers were marked as confidential.")
    mark_as_confidential.short_description = "Mark selected as confidential"
    
    def view_paper_link(self, obj):
        if obj.paper_file:
            return format_html('<a href="{}" target="_blank">View Paper</a>', obj.paper_file.url)
        return "-"
    view_paper_link.short_description = "Paper Link"

class PaperReleaseScheduleAdmin(admin.ModelAdmin):
    list_display = ('paper', 'release_date', 'is_released', 'released_by')
    list_filter = ('is_released', 'release_date')
    search_fields = ('paper__paper_code', 'paper__paper_title')
    date_hierarchy = 'release_date'
    readonly_fields = ('released_by',)
    raw_id_fields = ('paper',)
    
    fieldsets = (
        (None, {
            'fields': ('paper', 'release_date', 'is_released', 'release_notes')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if obj.is_released and not change:
            obj.released_by = request.user
        super().save_model(request, obj, form, change)
    
    def release_papers(self, request, queryset):
        updated = queryset.update(
            is_released=True,
            released_by=request.user,
            release_date=timezone.now()
        )
        self.message_user(request, f"{updated} papers were released.")
    release_papers.short_description = "Release selected papers"

admin.site.register(ExamPaperArchive, ExamPaperArchiveAdmin)
admin.site.register(PaperReleaseSchedule, PaperReleaseScheduleAdmin)



from django.contrib import admin
from django.utils import timezone
from .models import ExamCenter, ExamTimetable, ExamSession, Invigilator, InvigilationAssignment

@admin.register(ExamCenter)
class ExamCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'center_type', 'capacity', 'county', 'is_active')
    list_filter = ('center_type', 'county', 'is_active')
    search_fields = ('name', 'code', 'county', 'sub_county')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'center_type', 'school', 'capacity', 'is_active')
        }),
        ('Location Details', {
            'fields': ('county', 'sub_county', 'address', 'gps_coordinates')
        }),
        ('Contact Information', {
            'fields': ('contact_person', 'contact_phone', 'contact_email')
        }),
    )

@admin.register(ExamTimetable)
class ExamTimetableAdmin(admin.ModelAdmin):
    list_display = ('title', 'exam_year', 'is_published', 'published_date')
    list_filter = ('exam_year', 'is_published')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['publish_timetables']
    
    def save_model(self, request, obj, form, change):
        if 'is_published' in form.changed_data and obj.is_published:
            obj.published_date = timezone.now()
            obj.published_by = request.user
        super().save_model(request, obj, form, change)
    
    def publish_timetables(self, request, queryset):
        updated = queryset.update(
            is_published=True, 
            published_date=timezone.now(), 
            published_by=request.user
        )
        self.message_user(request, f"{updated} timetable(s) were successfully published.")
    publish_timetables.short_description = "Publish selected timetables"

class ExamSessionInline(admin.TabularInline):
    model = ExamSession
    extra = 1
    fields = ('subject', 'date', 'start_time', 'end_time', 'duration_minutes', 'paper_code')

@admin.register(ExamSession)
class ExamSessionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'timetable', 'date', 'start_time', 'end_time', 'duration_minutes')
    list_filter = ('date', 'subject', 'timetable')
    search_fields = ('subject__name', 'paper_code', 'instructions')
    date_hierarchy = 'date'

@admin.register(Invigilator)
class InvigilatorAdmin(admin.ModelAdmin):
    list_display = ('user', 'tsc_number', 'id_number', 'phone_number', 'is_active')
    list_filter = ('is_active', 'qualification')
    search_fields = ('user__first_name', 'user__last_name', 'tsc_number', 'id_number')
    filter_horizontal = ('subjects',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(InvigilationAssignment)
class InvigilationAssignmentAdmin(admin.ModelAdmin):
    list_display = ('invigilator', 'exam_center', 'exam_session', 'role', 'is_confirmed')
    list_filter = ('role', 'is_confirmed', 'exam_session__date')
    search_fields = (
        'invigilator__user__first_name',
        'invigilator__user__last_name',
        'exam_center__name'
    )
    raw_id_fields = ('invigilator', 'exam_center', 'exam_session')
    actions = ['confirm_assignments']
    
    def save_model(self, request, obj, form, change):
        if not obj.assigned_by:
            obj.assigned_by = request.user
        super().save_model(request, obj, form, change)
    
    def confirm_assignments(self, request, queryset):
        updated = queryset.update(is_confirmed=True)
        self.message_user(request, f"{updated} assignment(s) were successfully confirmed.")
    confirm_assignments.short_description = "Confirm selected assignments"

# Register ExamTimetable with ExamSession inline
admin.site.unregister(ExamTimetable)  # Unregister to re-register with inline
@admin.register(ExamTimetable)
class ExamTimetableWithSessionsAdmin(ExamTimetableAdmin):
    inlines = [ExamSessionInline]


from django.contrib import admin
from .models import KNECProfile, LoginAttempt, ActivityLog

@admin.register(KNECProfile)
class KNECProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'knec_id', 'designation', 'department', 'phone_number', 'updated_at')
    list_filter = ('department', 'two_factor_enabled', 'created_at')
    search_fields = ('user__username', 'user__email', 'knec_id', 'designation', 'phone_number')
    readonly_fields = ('knec_id', 'created_at', 'updated_at')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'knec_id', 'profile_picture')
        }),
        ('Professional Details', {
            'fields': ('designation', 'department', 'phone_number', 'office_location', 'responsibilities')
        }),
        ('Security Settings', {
            'fields': ('two_factor_enabled', 'login_alerts', 'session_timeout')
        }),
        ('Notification Preferences', {
            'fields': ('system_notifications', 'security_alerts', 'exam_updates')
        }),
        ('Interface Preferences', {
            'fields': ('theme', 'results_per_page')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'successful', 'ip_address')
    list_filter = ('successful', 'timestamp')
    search_fields = ('user__username', 'ip_address')
    readonly_fields = ('user', 'timestamp', 'successful', 'ip_address', 'user_agent')
    
    def has_add_permission(self, request):
        # Prevent manual addition of login attempts
        return False
    
    def has_change_permission(self, request, obj=None):
        # Prevent editing of login attempts
        return False

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'timestamp', 'ip_address')
    list_filter = ('activity_type', 'timestamp')
    search_fields = ('user__username', 'description', 'ip_address')
    readonly_fields = ('user', 'activity_type', 'description', 'timestamp', 'ip_address')
    
    def has_add_permission(self, request):
        # Prevent manual addition of activity logs
        return False
    
    def has_change_permission(self, request, obj=None):
        # Prevent editing of activity logs
        return False
    