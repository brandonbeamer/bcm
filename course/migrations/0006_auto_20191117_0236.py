# Generated by Django 2.2.6 on 2019-11-17 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_auto_20191115_0516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='content_type',
            field=models.CharField(choices=[('U', 'URL'), ('T', 'Plain Text'), ('M', 'Markdown-formatted Text')], default='M', max_length=1),
        ),
        migrations.AlterField(
            model_name='generalcourseitem',
            name='content_type',
            field=models.CharField(choices=[('U', 'URL'), ('T', 'Plain Text'), ('M', 'Markdown-formatted Text')], default='M', max_length=1),
        ),
        migrations.AlterField(
            model_name='submission',
            name='content_type',
            field=models.CharField(choices=[('U', 'URL'), ('T', 'Plain Text'), ('M', 'Markdown-formatted Text')], default='M', max_length=1),
        ),
    ]
