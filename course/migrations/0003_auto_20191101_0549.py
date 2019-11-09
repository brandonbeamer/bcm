# Generated by Django 2.2.6 on 2019-11-01 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20191029_0649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='code',
            field=models.CharField(help_text="A short name/code for the course; e.g. 'LING100'. It's a good idea to make this code unique among courses that will be taught simultaneously, but no such constraint is enforced.", max_length=20),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(help_text="The full name of the course; e.g. 'Introduction to English Linguistics Fall 2019 Section A'. It's a good idea to make this something that will be unique among all the courses you will ever teach, but no such constraint is enforced.", max_length=100),
        ),
        migrations.AlterField(
            model_name='course',
            name='password',
            field=models.CharField(blank=True, help_text='If provided, students need to enter this password to enroll. If left blank, anyone can enroll in the course.', max_length=30),
        ),
    ]
