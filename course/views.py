from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse

# from json import dumps

from .models import Course, Enrollment, CourseItem, ModelWithContent
from .forms import CreateGeneralCourseItemForm

# User is member of course test
# As a side-effect, sets self.user_is_instructor appropriately,
# to avoid looking up enrollment twice
def verify_enrollment(self):
    enrollment = Enrollment.objects.get(
        user = self.request.user,
        course = self.kwargs['pk']
    )
    if enrollment is None:
        return False
    else:
        self.context.update({'is_instructor': enrollment.role == Enrollment.INSTRUCTOR})
        return True

def verify_instructor(self):
    enrollment = Enrollment.objects.get(
        user = self.request.user,
        course = self.kwargs['pk']
    )
    if enrollment is not None and enrollment.role == Enrollment.INSTRUCTOR:
        self.context.update({'is_instructor': True})
        return True
    return False

# All course_* views inherit from this CourseBaseView class,
# It ensures that the user is logged in and a member of the course
class CourseBaseView(View):
    context = {}
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.course = get_object_or_404(Course, pk=kwargs['pk'])
        self.context.update({'course': self.course})

# Views only for enrolled users
class EnrolledBaseView(LoginRequiredMixin, UserPassesTestMixin, CourseBaseView):
    test_func = verify_enrollment

# Views only for course instructors
class InstructorBaseView(LoginRequiredMixin, UserPassesTestMixin, CourseBaseView):
    test_func = verify_instructor


class CourseItemsView(EnrolledBaseView):
    template_name = "course/course_items.html"

    def get(self, request, **kwargs):
        self.context.update({
            'view_name': 'course_items',
            'view_name_pretty': 'Materials',
            'item_list': self.course.generalcourseitem_set.all(),
        })
        return render(request, self.template_name, self.context)


class CreateCourseItemView(InstructorBaseView):
    template_name = "course/create_courseitem.html"
    form = CreateGeneralCourseItemForm
    base_context = {
        'view_name': 'create_courseitem',
        'view_name_pretty': 'Create Course Item',
    }

    def get(self, request, **kwargs):
        self.context.update({'form': self.form()})
        return render(request, self.template_name, self.context)

    def post(self, request, **kwargs):
        post = request.POST.copy()
        if post.get('content_type') == ModelWithContent.URL:
            post.pop('text_content', None)
        else:
            post.pop('url_content', None)

        form = self.form(post)
        self.context.update({'form': form})
        if form.is_valid():
            obj = form.save(commit = False)
            obj.course = self.course
            obj.save()
            return HttpResponseRedirect(reverse('course_items', kwargs={'pk': self.course.id}))

        return render(request, self.template_name, self.context)

class CourseItemView(EnrolledBaseView):
    template_name = "course/course_items.html"

class EditCourseItemView(InstructorBaseView):
    template_name = "course/edit_courseitem.html"

class AssignmentsView(TemplateView):
    template_name = "course/course_items.html"

class GradebookView(TemplateView):
    template_name = "course/course_items.html"

class CourseSettingsView(TemplateView):
    template_name = "course/course_items.html"
