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


]