# Generated by Django 2.2.6 on 2019-11-02 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20191101_0549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='password',
            field=models.CharField(blank=True, help_text='If provided, students need to enter this password to enroll. If left blank, anyone can enroll in the course.', max_length=100),
        ),
    ]
