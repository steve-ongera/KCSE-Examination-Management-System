from django.urls import path
from . import views


urlpatterns = [
    path('', views.custom_login , name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.custom_logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    # ... previous URLs ...
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('school-admin/', views.school_admin_dashboard, name='school_admin_dashboard'),
    path('knec/', views.knec_dashboard, name='knec_dashboard'),
    path('register-student-exam/', views.register_student_exam, name='register-student-exam'),
    path('performance_dashboard/', views.performance_dashboard , name='examination_dashboard'),
     path('top_students/', views.top_students_view , name='top_students_view'),
     path('subject-analysis' , views.subject_analysis_view , name='subject-analysis'),


     #school 
     path('school_performance_analysis/', views.school_performance_analysis, name='school_performance_analysis'),
     path('school-performance/', views.school_exam_performance, name='school-exam-performance'),
     path('student-result-search/', views.student_result_search, name='student_result_search'),
    path('student-result-detail/<int:student_id>/', views.student_result_detail, name='student_result_detail'),


    #admin/ student crud opertaions 
    path('student/', views.student_list, name='student_list'),
    path('student/add/', views.student_create, name='student_create'),
    path('student/<int:pk>/', views.student_detail, name='student_detail'),
    path('student/<int:pk>/edit/', views.student_update, name='student_update'),
    path('student/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('student/search/', views.student_search, name='student_search'),

    #school admin crud operations 
    path('school_students/', views.school_student_list, name='school_student_list'),
    path('school_student/<int:pk>/', views.school_student_detail, name='school_student_detail'),
    path('school_students/create/', views.school_student_create, name='school_student_create'),
    path('school_students/update/<int:pk>/', views.school_student_update, name='school_student_update'),
    path('school_students/delete/<int:pk>/', views.school_student_delete, name='school_student_delete'),


    #examinations
    path('enter-marks/', views.EnterStudentMarksView.as_view(), name='enter_student_marks'),
    # New URL pattern for student performance view
    path('search-student-performance/', views.StudentPerformanceView.as_view(), name='search_student_performance'),
    path('student/<int:student_id>/performance/', views.student_performance_view, name='student_performance'),
    path('performance/current/', views.current_year_performance, name='current_year_performance'),
    path('school-ranking/', views.school_ranking , name="school_ranking"),
    path('academic_performance_report/', views.academic_performance_report , name="academic_performance_report"),
    path('school_registration_report/', views.school_registration_report , name="school_registration_report"),
    path('school_registration_detail/<int:school_id>/', views.school_registration_detail, name='school_registration_detail'),
    path('school_registered_students/<int:school_id>/', views.school_registered_students, name='school_registered_students'),

    path('schools/', views.school_list, name='school_list'),
    path('schools/<int:pk>/', views.school_detail, name='school_detail'),
    path('schools/create/', views.school_create_edit, name='school_create'),
    path('schools/edit/<int:pk>/', views.school_create_edit, name='school_edit'),
    path('schools/delete/<int:pk>/', views.school_delete, name='school_delete'),


    path('papers/', views.paper_archive_list, name='paper-archive-list'),
    path('papers/upload/', views.paper_upload, name='paper-upload'),
    path('papers/<int:pk>/', views.paper_detail, name='paper-detail'),
    path('papers/release/', views.paper_release, name='paper-release'),
    path('releases/', views.release_schedule, name='paper-release-schedule'),

    path('knec_official_support/', views.knec_official_support, name='knec_official_support'),
    path('knec_system_configuration/', views.knec_system_configuration, name='knec_system_configuration'),
    path('school_admin_system_configuration/', views.school_admin_system_configuration, name='school_admin_system_configuration'),
    #


    # Dashboard
    path('dashboard/', views.exam_management_dashboard, name='exam-dashboard'),
    
    # Timetable URLs
    path('timetables/', views.timetable_list, name='timetable-list'),
    path('timetables/<int:pk>/', views.timetable_detail, name='timetable-detail'),
    
    # Exam Center URLs
    path('centers/', views.center_list, name='center-list'),
    path('centers/<int:pk>/', views.center_detail, name='center_detail'),
    
    # Invigilator URLs
    path('invigilators/', views.invigilator_list, name='invigilator-list'),
    path('invigilators/<int:pk>/', views.invigilator_detail, name='invigilator-detail'),


    path('school-admin-profile/', views.school_admin_profile, name='school_admin_profile'),
    path('exam_timetable_view/' , views.exam_timetable_view , name='exam_timetable_view'),
    path('subject_list_view/' , views.subject_list_view , name='subject_list_view'),
    path('kenyan_curriculum_view/' , views.kenyan_curriculum_view , name="kenyan_curriculum_view"),
    path('announcements/', views.knec_announcements, name='knec_announcements'),


    path('knec_profile/', views.knec_profile, name='knec_profile'),
    path('knec_profile/update/', views.update_knec_profile, name='update_knec_profile'),
    path('knec_profile/update-settings/', views.update_knec_settings, name='update_knec_settings'),
    path('knec_profile/update-picture/', views.update_knec_profile_picture, name='update_knec_profile_picture'),
    path('knec_profile/change-password/', views.change_knec_password, name='change_knec_password'),
    path('knec_profile/security-settings/', views.update_knec_security_settings, name='update_knec_security_settings'),
    
    # Activity Log URL
    path('activity-log/', views.knec_activity_log, name='knec_activity_log'),


    # Dashboard
    path('resources_dashboard', views.resources_dashboard, name='resources_dashboard'),
    path('archive/', views.knec_archive, name='knec_archive'),
    path('contact/', views.contact_knec, name='contact_knec'),
    path('school-profile/', views.school_profile, name='school_profile'),
    
    # Resource list and detail
    path('public-resources/', views.knec_resources, name='knec_resources'),
    path('resources/', views.resource_list, name='resource_list'),
    path('resources/<int:pk>/', views.resource_detail, name='resource_detail'),
    path('exam_dashboard', views.exam_dashboard , name='exam-dashboard'),
    
    # Resource operations
    path('resources/add/', views.add_resource, name='add_resource'),
    path('resources/<int:pk>/edit/', views.edit_resource, name='edit_resource'),
    path('resources/<int:pk>/delete/', views.delete_resource, name='delete_resource'),
    path('resources/<int:pk>/download/', views.resource_download, name='resource_download'),
    path('resources/<int:pk>/status/<str:status>/', views.change_resource_status, name='change_resource_status'),
    
    # Statistics and reporting
    path('statistics/', views.resource_statistics, name='resource_statistics'),
    
    # Import resources
    path('import/', views.import_resources, name='import_resources'),
    
    # API endpoint
    path('api/resources/', views.ResourceAPIView.as_view(), name='api_resources'),


]