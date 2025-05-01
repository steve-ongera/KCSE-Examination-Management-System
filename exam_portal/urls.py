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


]