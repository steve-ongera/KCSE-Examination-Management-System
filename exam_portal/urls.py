from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.custom_login , name='login'),
    path('register/', views.register, name='register'),
    # ... previous URLs ...
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('school-admin/', views.school_admin_dashboard, name='school_admin_dashboard'),
    path('knec/', views.knec_dashboard, name='knec_dashboard'),
]