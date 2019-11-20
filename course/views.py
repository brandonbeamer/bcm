from collections import OrderedDict

from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse, reverse_lazy
from django.db.models import Max
from django.forms import formset_factory
import json

# from json import dumps

from .models import Course, Enrollment, GeneralCourseItem, ItemHeading
from .forms import GeneralCourseItemCreateForm, ItemHeadingCreateInlineForm, ItemOrderUpdateInlineForm, ItemIdForm, IdVisibleForm

# User is member of course test
# As a side-effect, sets self.user_is_instructor appropriately,
# to avoid looking up enrollment twice
def verify_enrollment(self, update_context = True):
    enrollment = Enrollment.objects.get(
        user = self.request.user,
        course = self.kwargs['course_id']
    )
    if enrollment is None:
        return False
    else:
        if update_context:
            self.context.update({'is_instructor': enrollment.role == Enrollment.INSTRUCTOR})
        return True

def verify_instructor(self, update_context = True):
    enrollment = Enrollment.objects.get(
        user = self.request.user,
        course = self.kwargs['course_id']
    )
    if enrollment is not None and enrollment.role == Enrollment.INSTRUCTOR:
        if update_context:
            self.context.update({'is_instructor': True})
        return True
    return False

# All course_* views inherit from this CourseBaseView class,
# It ensures that the user is logged in and a member of the course
class CourseBaseView(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.context = {}
        self.course = get_object_or_404(Course, id=kwargs['course_id'])
        self.context.update({'course': self.course})

# Views only for enrolled users
class EnrolledBaseView(LoginRequiredMixin, UserPassesTestMixin, CourseBaseView):
    test_func = verify_enrollment

# Views only for course instructors
class InstructorBaseView(LoginRequiredMixin, UserPassesTestMixin, CourseBaseView):
    test_func = verify_instructor

class CourseItemListView(EnrolledBaseView):
    template_name = "course/course_item_list.html"
    base_context = {
        'view_name': 'course_items',
        'view_name_pretty': 'Materials',
    }

    def get(self, request, **kwargs):
        self.context.update({
            **CourseItemListView.base_context,
            'item_list': self.course.get_general_course_item_list(),
        })
        self.context['SERVER_DATA_JSON'] = json.dumps({
            'course_item_heading_create_inline_url': reverse('course_item_heading_create_inline', kwargs = {'course_id': self.course.id}),
            'course_item_heading_delete_inline_url': reverse('course_item_heading_delete_inline', kwargs = {'course_id': self.course.id}),
            'course_item_heading_visible_update_inline_url': reverse('course_item_heading_visible_update_inline', kwargs = {'course_id': self.course.id}),
            'course_item_order_update_inline_url': reverse('course_item_order_update_inline', kwargs = {'course_id': self.course.id}),
            'course_item_delete_inline_url': reverse('course_item_delete_inline', kwargs = {'course_id': self.course.id}),
            'course_item_delete_set_inline_url': reverse('course_item_delete_set_inline', kwargs = {'course_id': self.course.id}),
            'course_item_visible_update_inline_url': reverse('course_item_visible_update_inline', kwargs = {'course_id': self.course.id}),
            # 'course_item_set_visible_update_inline_url': reverse('course_item_set_visible_update_inline', kwargs = {'course_id': self.course.id}),

        })

        return render(request, self.template_name, self.context)

class CourseItemCreateView(InstructorBaseView):
    template_name = "course/course_item_create.html"
    form = GeneralCourseItemCreateForm
    # create_heading_form = OptionalCreateItemHeadingForm
    base_context = {
        'view_name': 'create_courseitem',
        'view_name_pretty': 'Create Course Item',
    }

    def get(self, request, **kwargs):
        self.context.update({**CourseItemCreateView.base_context, 'form': self.form()})
        return render(request, self.template_name, self.context)

    def post(self, request, **kwargs):
        form = self.form(request.POST)
        self.context.update({**CourseItemCreateView.base_context, 'form': form})

        # new_category = False
        # if newheading_form.is_valid() and newheading_form.cleaned_data.get('name', ''):
        #     new_category = True

        # if newheading_form.is_valid():
        #     name = newheading_form.cleaned_data['name']

        if form.is_valid():
            # newcat = None
            # if new_category: # Neither None nor ''
            #     # Make a catgory first
            #     newcat = newheading_form.save(commit = False)
            #     newcat.course = self.course
            #     newcat.type = ItemCategory.GENERAL
            #     max_order = ItemCategory.objects.filter(course=self.course).aggregate(Max('order')).get('order__max')
            #     newcat.order = 0 if max_order is None else max_order + 1
            #     newcat.save()

            obj = form.save(commit = False)
            # if new_category:
            #     obj.category = newcat
            # max_order = GeneralCourseItem.objects.filter(course = self.course, category = obj.category).aggregate(Max('order')).get('order__max')
            # obj.order = 0 if max_order is None else max_order + 1
            obj.course = self.course

            obj.save()
            return HttpResponseRedirect(reverse('course_item_list', kwargs={'course_id': self.course.id}))

        return render(request, self.template_name, self.context)

class CourseItemDetailView(EnrolledBaseView):
    template_name = "course/course_item_list.html"

class CourseItemUpdateView(InstructorBaseView):
    template_name = "course/course_item_update.html"

class CourseItemOrderUpdateInlineView(InstructorBaseView):
    # No template, it either goes through or doesn't
    form_class = ItemOrderUpdateInlineForm

    def post(self, request, **kwargs):
        formset_class = formset_factory(self.form_class)
        formset = formset_class(request.POST)
        # print(formset.as_p())
        if not formset.is_valid():
            return HttpResponseBadRequest();

        for form in formset:
            object_class = ItemHeading if form.cleaned_data['is_heading'] else GeneralCourseItem
            object = get_object_or_404(object_class, id=form.cleaned_data['id'])
            object.order = form.cleaned_data['order']
            object.save()

        return HttpResponse();

class CourseItemVisibleUpdateInlineView(InstructorBaseView):
    template_name = "course/course_item_list/course_item.html"
    form_class = IdVisibleForm
    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest();

        object = get_object_or_404(GeneralCourseItem, id=form.cleaned_data['id'])
        object.visible = form.cleaned_data['visible']
        object.save()
        self.context.update({'item': object})
        return render(request, self.template_name, self.context)

class CourseItemDeleteInlineView(InstructorBaseView):
    form_class = ItemIdForm
    def post(self, request, **kwargs):
        form = self.form_class(request.POST)

        if not form.is_valid():
            return HttpResponseBadRequest();

        obj = get_object_or_404(GeneralCourseItem, id=form.cleaned_data['id'])
        obj.delete()
        return HttpResponse();

class CourseItemDeleteSetInlineView(InstructorBaseView):
    form_class = ItemIdForm
    def post(self, request, **kwargs):
        formset_class = formset_factory(self.form_class)
        formset = formset_class(request.POST)

        if not formset.is_valid():
            return HttpResponseBadRequest();

        for f in formset:
            obj = get_object_or_404(GeneralCourseItem, id=f.cleaned_data['id'])
            obj.delete()

        return HttpResponse();

class CourseItemHeadingCreateInlineView(InstructorBaseView):
    """
    Called from client script, creates a heading and returns an updated item list
    """
    template_name = "course/course_item_list/item_list.html"
    form_class = ItemHeadingCreateInlineForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST);
        if not form.is_valid():
            return HttpResponseBadRequest()
        obj = form.save(commit = False)
        obj.course = self.course
        obj.save()
        self.context.update({'item_list': self.course.get_general_course_item_list()})
        return render(request, self.template_name, self.context)

class CourseItemHeadingDeleteInlineView(InstructorBaseView):
    form_class = ItemIdForm
    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if(not form.is_valid()):
            return HttpResponseBadRequest();

        obj = get_object_or_404(ItemHeading, id=form.cleaned_data['id'])
        obj.delete()
        return HttpResponse();

class CourseItemHeadingVisibleUpdateInlineView(InstructorBaseView):
    template_name = "course/course_item_list/course_item_heading.html"
    form_class = IdVisibleForm
    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest();

        object = get_object_or_404(ItemHeading, id=form.cleaned_data['id'])
        object.visible = form.cleaned_data['visible']
        object.save()
        self.context.update({'item': object})
        return render(request, self.template_name, self.context)


class AssignmentListView(TemplateView):
    template_name = "course/course_item_list.html"

class GradebookView(TemplateView):
    template_name = "course/course_item_list.html"

class CourseSettingsView(TemplateView):
    template_name = "course/course_item_list.html"
