# Generated by Django 2.2.6 on 2019-10-29 05:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(choices=[('U', 'URL'), ('P', 'Plain Text'), ('M', 'Markdown-formatted Text')], default='M', max_length=1)),
                ('url_content', models.URLField(blank=True)),
                ('text_content', models.TextField(blank=True)),
                ('name', models.CharField(help_text='The name or title of the course item', max_length=50)),
                ('description', models.CharField(blank=True, help_text='A short description of the course item', max_length=300)),
                ('visible', models.BooleanField(default=True, help_text='Whether students can see the course item')),
                ('open', models.CharField(choices=[('O', 'Open'), ('C', 'Closed'), ('S', 'Scheduled')], default='O', help_text='Whether submissions are being accepted. If an assignment is not visible, it is closed no matter what this is set to.', max_length=1)),
                ('closes_at', models.DateTimeField(help_text="When 'open' is set to 'Scheduled', datetime at which submissions (and their revisions) are no longer accepted")),
                ('due_at', models.DateTimeField(help_text="Datetime at which submissions become 'late'")),
            ],
            options={
                'ordering': ['course', '-due_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(help_text="The full name of the course; e.g. 'Introduction to English Linguistics Fall 2019 Section A'", max_length=100)),
                ('code', models.CharField(help_text="A short name/code for the course; e.g. 'LING100'", max_length=20)),
                ('password', models.CharField(blank=True, help_text='If provided, students need to enter this password to enroll.', max_length=30)),
                ('open', models.BooleanField(default=True, help_text='Whether the course is open')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(choices=[('U', 'URL'), ('P', 'Plain Text'), ('M', 'Markdown-formatted Text')], default='M', max_length=1)),
                ('url_content', models.URLField(blank=True)),
                ('text_content', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('D', 'Draft'), ('S', 'Submitted'), ('A', 'Accepted'), ('R', 'Revision Requested')], default='D', max_length=1)),
                ('auto_submit', models.BooleanField(default=True, help_text="If true, submission is treated as 'draft' until the due datetime, and treated as 'submitted' after. Allows students to work on submissions on-and-off without worrying about explicitly submitting.")),
                ('submitted_at', models.DateTimeField(null=True)),
                ('evaluated_at', models.DateTimeField(null=True)),
                ('revision_due_at', models.DateTimeField(help_text="If status is 'revision requested', defines when next submission becomes 'late'.", null=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Assignment')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RollCall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taken_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course')),
            ],
            options={
                'ordering': ['-taken_at'],
            },
        ),
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('A', 'Assignment'), ('G', 'General')], max_length=1)),
                ('name', models.CharField(max_length=30)),
                ('order', models.SmallIntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='GeneralCourseItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(choices=[('U', 'URL'), ('P', 'Plain Text'), ('M', 'Markdown-formatted Text')], default='M', max_length=1)),
                ('url_content', models.URLField(blank=True)),
                ('text_content', models.TextField(blank=True)),
                ('name', models.CharField(help_text='The name or title of the course item', max_length=50)),
                ('description', models.CharField(blank=True, help_text='A short description of the course item', max_length=300)),
                ('visible', models.BooleanField(default=True, help_text='Whether students can see the course item')),
                ('category', models.ForeignKey(help_text='The category or heading that this item will apear under. Leave blank to simply appear at the top.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='course.ItemCategory')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course')),
            ],
            options={
                'ordering': ['course', 'name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=6, help_text='A numeric score between 0 and 1, with 6 decimal places of precision.', max_digits=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Assignment')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='evaluations_made', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('S', 'Student'), ('I', 'Instructor')], default='S', max_length=1)),
                ('enrolled_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['role', 'enrolled_at'],
            },
        ),
        migrations.AddField(
            model_name='course',
            name='members',
            field=models.ManyToManyField(through='course.Enrollment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('P', 'Present'), ('L', 'Late'), ('A', 'Absent'), ('E', 'Excused')], default='L', max_length=1)),
                ('rollcall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.RollCall')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
            },
        ),
        migrations.AddField(
            model_name='assignment',
            name='category',
            field=models.ForeignKey(help_text='The category or heading that this item will apear under. Leave blank to simply appear at the top.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='course.ItemCategory'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course'),
        ),
        migrations.AddConstraint(
            model_name='itemcategory',
            constraint=models.UniqueConstraint(fields=('course', 'type', 'order'), name='unique_item_categories'),
        ),
    ]
