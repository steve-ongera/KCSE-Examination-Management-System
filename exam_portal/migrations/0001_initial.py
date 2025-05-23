# Generated by Django 5.2 on 2025-04-29 07:37

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField(unique=True)),
                ('grading_system', models.JSONField()),
                ('is_current', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('knec_code', models.CharField(max_length=20, unique=True)),
                ('registration_number', models.CharField(max_length=50, unique=True)),
                ('school_type', models.CharField(choices=[('PUBLIC', 'Public'), ('PRIVATE', 'Private'), ('EXTRA_COUNTY', 'Extra County'), ('NATIONAL', 'National'), ('INTERNATIONAL', 'International')], max_length=20)),
                ('category', models.CharField(choices=[('BOYS', 'Boys Only'), ('GIRLS', 'Girls Only'), ('MIXED', 'Mixed')], max_length=10)),
                ('registration_date', models.DateField()),
                ('established_date', models.DateField()),
                ('motto', models.CharField(blank=True, max_length=100, null=True)),
                ('mission', models.TextField(blank=True, null=True)),
                ('vision', models.TextField(blank=True, null=True)),
                ('county', models.CharField(max_length=100)),
                ('sub_county', models.CharField(max_length=100)),
                ('ward', models.CharField(blank=True, max_length=100, null=True)),
                ('postal_address', models.CharField(max_length=100)),
                ('physical_address', models.TextField()),
                ('gps_coordinates', models.CharField(blank=True, max_length=50, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('alternative_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('principal_name', models.CharField(max_length=100)),
                ('principal_phone', models.CharField(max_length=15)),
                ('principal_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('principal_tsc_number', models.CharField(blank=True, max_length=20, null=True)),
                ('curriculum', models.CharField(default='8-4-4', max_length=100)),
                ('number_of_streams', models.PositiveIntegerField(default=1)),
                ('is_active', models.BooleanField(default=True)),
                ('last_inspection_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('CORE', 'Core Compulsory'), ('SCIENCE', 'Science Subjects'), ('HUMANITIES', 'Humanities Subjects'), ('TECHNICAL', 'Technical Subjects'), ('LANGUAGES', 'Language Subjects')], max_length=20)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.PositiveSmallIntegerField(choices=[(1, 'student'), (2, 'school_admin'), (3, 'knec_official')])),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ExamRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('exam_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam_portal.examyear')),
            ],
        ),
        migrations.CreateModel(
            name='KNECOfficialProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=100)),
                ('employee_id', models.CharField(max_length=20, unique=True)),
                ('is_supervisor', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='knec_official_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OverallResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_marks', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('average_grade', models.CharField(blank=True, max_length=2)),
                ('average_points', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('division', models.CharField(blank=True, max_length=20)),
                ('registration', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='overall_result', to='exam_portal.examregistration')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('birth_date', models.DateField()),
                ('birth_certificate_number', models.CharField(blank=True, max_length=20, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('nationality', models.CharField(default='Kenyan', max_length=50)),
                ('county_of_origin', models.CharField(max_length=50)),
                ('sub_county', models.CharField(max_length=50)),
                ('passport_photo', models.ImageField(blank=True, null=True, upload_to='student_photos/')),
                ('disability', models.CharField(blank=True, max_length=100, null=True)),
                ('disability_description', models.TextField(blank=True, null=True)),
                ('index_number', models.CharField(max_length=20, unique=True)),
                ('admision_number', models.CharField(max_length=20, null=True)),
                ('admission_date', models.DateField()),
                ('current_class', models.CharField(max_length=20)),
                ('house', models.CharField(blank=True, max_length=50, null=True)),
                ('is_boarder', models.BooleanField(default=False)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('postal_address', models.CharField(blank=True, max_length=100, null=True)),
                ('residential_address', models.TextField(blank=True, null=True)),
                ('previous_school', models.CharField(blank=True, max_length=100, null=True)),
                ('kcpe_year', models.PositiveIntegerField(blank=True, null=True)),
                ('kcpe_index', models.CharField(blank=True, max_length=20, null=True)),
                ('kcpe_marks', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='exam_portal.school')),
            ],
        ),
        migrations.AddField(
            model_name='examregistration',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='exam_portal.student'),
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_verified', models.BooleanField(default=False)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to='exam_portal.student')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_compulsory', models.BooleanField(default=False)),
                ('registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='exam_portal.examregistration')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam_portal.subject')),
            ],
            options={
                'unique_together': {('registration', 'subject')},
            },
        ),
        migrations.CreateModel(
            name='ExamResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('grade', models.CharField(blank=True, max_length=2)),
                ('points', models.PositiveIntegerField(blank=True, null=True)),
                ('subject_registration', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='result', to='exam_portal.subjectregistration')),
            ],
        ),
        migrations.CreateModel(
            name='SchoolAdminProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=100)),
                ('tsc_number', models.CharField(blank=True, max_length=20, null=True)),
                ('is_primary_admin', models.BooleanField(default=False)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admins', to='exam_portal.school')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='school_admin_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'school')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='examregistration',
            unique_together={('student', 'exam_year')},
        ),
    ]
