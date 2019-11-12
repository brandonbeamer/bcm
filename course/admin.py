from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'password', 'open', 'creator']

@admin.register(models.Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['course', 'user', 'role']

@admin.register(models.RollCall)
class RollCallAdmin(admin.ModelAdmin):
    list_display = ['course', 'taken_at']

@admin.register(models.Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['rollcall', 'user', 'status']


@admin.register(models.ItemHeading)
class ItemHeadingAdmin(admin.ModelAdmin):
    list_display = ['course', 'type', 'order', 'name']

@admin.register(models.GeneralCourseItem)
class GeneralCourseItemAdmin(admin.ModelAdmin):
    list_display = ['course', 'name', 'visible']

@admin.register(models.Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['course', 'name', 'visible', 'open', 'due_at', 'closes_at']

@admin.register(models.Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'author', 'status', 'auto_submit']

@admin.register(models.Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'user', 'score']
