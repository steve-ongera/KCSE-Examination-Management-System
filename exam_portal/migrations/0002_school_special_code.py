# Generated by Django 5.2 on 2025-04-29 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_portal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='special_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
