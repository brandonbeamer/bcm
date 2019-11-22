import uuid
from datetime import date
from django.utils import timezone
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.urls import reverse_lazy, reverse

# Create your models here.
class Course(models.Model):
    """ A BCM Course """
    # Primary Key
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable=False)

    creator = models.ForeignKey(User, on_delete = models.CASCADE,
        related_name = '+')
    created_at = models.DateTimeField(auto_now_add = True)

    # Information
    name = models.CharField(max_length = 100,
        help_text = "The full name of the course; e.g. 'Introduction to English Linguistics Fall 2019 Section A'. "
            "It's a good idea to make this something that will be unique among all the courses you will ever teach, "
            "but no such constraint is enforced.")
    code = models.CharField(max_length = 20,
        help_text = "A short name/code for the course; e.g. 'LING100'. "
            "It's a good idea to make this code unique among courses that will be taught simultaneously, "
            "but no such constraint is enforced.")
    password = models.CharField(max_length = 100, blank = True,
        help_text = "If provided, students need to enter this password to enroll. "
            "If left blank, anyone can enroll in the course.")

    # Flags
    open = models.BooleanField(default = True, help_text = "Whether the course is open")

    # Relations
    members = models.ManyToManyField(User, through = 'Enrollment',
        through_fields = ('course', 'user'))

    def get_course_item_list(self):
        """ Returns general items and headings, sorted """
        item_list = self.courseitem_set.all()
        heading_list = self.itemheading_set.all()
        return sorted(list(item_list) + list(heading_list), key=lambda x: (x.order, -x.created_at.timestamp()))


    def get_absolute_url(self):
        return reverse('course_item_list', args = [self.id])

    def __str__(self):
        return f"{self.id}:{self.code}"


class Enrollment(models.Model):
    """ Specifies Course Membership """
    INSTRUCTOR = 'I'
    STUDENT = 'S'
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    user   = models.ForeignKey(User, on_delete = models.CASCADE)
    role   = models.CharField(max_length = 1, default = STUDENT,
        choices = (
            (STUDENT, 'Student'),
            (INSTRUCTOR, 'Instructor'),
        ))
    enrolled_at = models.DateTimeField(auto_now_add = True)
    class Meta:
        ordering = ['role', 'enrolled_at']
    def __str__(self):
        return f"{self.user} is {self.role} of {self.course}"

class RollCall(models.Model):
    """ An instance of taking attendance """
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    taken_at = models.DateTimeField(default = timezone.now)
    def __str__(self):
        return f"{self.course} roll taken at {taken_at}"
    class Meta:
        ordering = ['-taken_at']

class Attendance(models.Model):
    """ Records whether a student was present/absent/etc. on a given date """
    PRESENT = 'P'
    ABSENT  = 'A'
    LATE    = 'L'
    EXCUSED = 'E'
    rollcall = models.ForeignKey(RollCall, on_delete = models.CASCADE)
    user   = models.ForeignKey(User, on_delete = models.CASCADE)
    status = models.CharField(max_length = 1, default = LATE,
        choices = (
            (PRESENT, 'Present'),
            (LATE, 'Late'),
            (ABSENT, 'Absent'),
            (EXCUSED, 'Excused'),
        ))
    class Meta:
        ordering = ['user']
    def __str__(self):
        return f"{self.user}'s was {self.status}"

class ItemHeading(models.Model):
    """ Headings that appear on course item pages """

    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    # type = models.CharField(max_length = 1, choices = TYPE_CHOICES, default = ITEMHEADING_TYPE_GENERAL)
    order = models.SmallIntegerField(default = 0)
    name = models.CharField(max_length = 30)
    created_at = models.DateTimeField(auto_now_add = True)
    visible = models.BooleanField(default = True)

    def is_heading(self):
        return True

    class Meta:
        ordering = ['course']

COURSEITEM_CONTENT_TYPE_URL = 'U'
COURSEITEM_CONTENT_TYPE_PLAINTEXT = 'T'
COURSEITEM_CONTENT_TYPE_MARKDOWN = 'M'
class CourseItem(models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    name = models.CharField(max_length = 50, help_text = "The name or title of the course item")
    description = models.CharField(max_length = 300, blank = True, help_text = "A short description of the course item")
    visible = models.BooleanField(default = True, help_text = "Whether students can see the course item")
    order = models.SmallIntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)

    CONTENT_TYPE_CHOICES = [
        (COURSEITEM_CONTENT_TYPE_URL, 'URL'),
        # (COURSEITEM_CONTENT_TYPE_PLAINTEXT, 'Plain Text'),
        (COURSEITEM_CONTENT_TYPE_MARKDOWN, 'Markdown-formatted Text')
    ]

    content_type = models.CharField(max_length = 1, default = COURSEITEM_CONTENT_TYPE_MARKDOWN,
        choices = CONTENT_TYPE_CHOICES)
    url_content = models.URLField(blank = True, max_length = 200)
    text_content = models.TextField(blank = True)

    # All the content-related stuff is inherited
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('course_item_detail', kwargs={
            'course_id': self.course.id,
            'item_id': self.id
        })

    class Meta:
        ordering = ['course']


class Assignment(models.Model):
    """ A task that students of a given course are expected to complete """
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    name = models.CharField(max_length = 50, help_text = "The name or title of the course item")
    description = models.CharField(max_length = 300, blank = True, help_text = "A short description of the course item")
    visible = models.BooleanField(default = True, help_text = "Whether students can see the course item")

    created_at = models.DateTimeField(auto_now_add = True)
    text_content = models.TextField(blank = True)


    OPEN = 'O'
    CLOSED = 'C'
    SCHEDULED = 'S'
    OPEN_CHOICES = [(OPEN, 'Open'), (CLOSED, 'Closed'), (SCHEDULED, 'Scheduled')]

    open = models.CharField(max_length = 1, choices = OPEN_CHOICES, default = OPEN,
        help_text = "Whether submissions are being accepted. If an assignment is not visible, it is closed no matter what this is set to.")
    closes_at = models.DateTimeField(help_text="When 'open' is set to 'Scheduled', datetime at which submissions (and their revisions) are no longer accepted")
    due_at = models.DateTimeField(help_text = "Datetime at which submissions become 'late'")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['course', '-due_at']

class Evaluation(models.Model):
    """ An evaluation/grade for an assignment """
    assignment = models.ForeignKey(Assignment, on_delete = models.CASCADE, db_index = True)
    user       = models.ForeignKey(User, on_delete = models.CASCADE, db_index = True)
    score      = models.DecimalField(decimal_places = 6, max_digits = 7, help_text = "A numeric score between 0 and 1, with 6 decimal places of precision.")
    created_at = models.DateTimeField(auto_now_add = True)
    author     = models.ForeignKey(User, null = True, on_delete = models.SET_NULL, related_name='evaluations_made')
    def __str__(self):
        return f"{user} got {score} on {assignment}"
    class Meta:
        ordering = ['-created_at']

class Submission(models.Model):
    """ A student's submission for an assignment """

    # Content-related stuff is inherited

    DRAFT     = 'D'
    SUBMITTED = 'S'
    EVALUATED = 'A'
    REVISE    = 'R'
    STATUS_CHOICES = [(DRAFT, 'Draft'), (SUBMITTED, 'Submitted'), (EVALUATED, 'Accepted'), (REVISE, 'Revision Requested')]

    author = models.ForeignKey(User, on_delete = models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete = models.CASCADE)
    status = models.CharField(max_length = 1, choices = STATUS_CHOICES, default = DRAFT)

    auto_submit = models.BooleanField(default = True,
        help_text = "If true, submission is treated as 'draft' until the due datetime, and treated as 'submitted' after. "
                    "Allows students to work on submissions on-and-off without worrying about explicitly submitting.")
    submitted_at = models.DateTimeField(null = True)
    evaluated_at = models.DateTimeField(null = True)
    revision_due_at = models.DateTimeField(null = True,
        help_text = "If status is 'revision requested', defines when next submission becomes 'late'.")


    def __str__(self):
        return f"{author}'s submission for {assignment}"
