from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.custom_login , name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.custom_logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    # ... previous URLs ...
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('school-admin/', views.school_admin_dashboard, name='school_admin_dashboard'),
    path('knec/', views.knec_dashboard, name='knec_dashboard'),
]