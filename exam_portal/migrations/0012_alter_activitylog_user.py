# Generated by Django 5.2 on 2025-05-02 19:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_portal', '0011_category_resourcetype_resource_resourcedownloadlog_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitylog',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activities', to=settings.AUTH_USER_MODEL),
        ),
    ]
