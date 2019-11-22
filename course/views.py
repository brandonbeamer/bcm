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
import markdown
import bleach

# from json import dumps

from .models import Course, Enrollment, CourseItem, ItemHeading
from .models import COURSEITEM_CONTENT_TYPE_MARKDOWN, COURSEITEM_CONTENT_TYPE_PLAINTEXT
from .forms import CourseItemForm, ItemHeadingCreateInlineForm, ItemOrderUpdateInlineForm
from .forms import ItemIdForm, IdVisibleForm, TextForm

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

def render_markdown(text):
    md = markdown.Markdown(extensions=['smarty'])
    return bleach.clean(
        text = md.convert(text),
        tags = [
            'ul',
            'ol',
            'li',
            'p',
            'pre',
            'code',
            'blockquote',
            'h1',
            'h2',
            'h3',
            'h4',
            'h5',
            'h6',
            'hr',
            'br',
            'strong',
            'em',
            'a',
            'img'
        ]
    )

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
    def get_base_context(self, kwargs):
        return {
            'page_name': 'course_items',
            'page_name_pretty': 'Materials',
        }

    def get(self, request, **kwargs):
        self.context.update({
            **self.get_base_context(kwargs),
            'item_list': self.course.get_course_item_list(),
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
    template_name = "course/course_item_update.html"
    form = CourseItemForm
    # create_heading_form = OptionalCreateItemHeadingForm
    def get_base_context(self):
        return {
            'page_name': 'create_courseitem',
            'page_name_pretty': 'Create Course Item',
            'form_action': reverse('course_item_create', kwargs={'course_id': self.course.id}),
            'SERVER_DATA_JSON': json.dumps({
                'markdown_preview_url': reverse('markdown_preview'),
            }),
        }

    def get(self, request, **kwargs):
        self.context.update({**self.get_base_context(), 'form': self.form()})
        return render(request, self.template_name, self.context)

    def post(self, request, **kwargs):
        form = self.form(request.POST)
        self.context.update({**self.get_base_context(), 'form': form})

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
            # max_order = CourseItem.objects.filter(course = self.course, category = obj.category).aggregate(Max('order')).get('order__max')
            # obj.order = 0 if max_order is None else max_order + 1
            obj.course = self.course

            obj.save()
            return HttpResponseRedirect(reverse('course_item_list', kwargs={'course_id': self.course.id}))

        return render(request, self.template_name, self.context)

class CourseItemDetailView(EnrolledBaseView):
    template_name = "course/course_item_detail.html"
    def get(self, request, **kwargs):
        object = get_object_or_404(CourseItem, course = self.course, id=kwargs['item_id'])
        cooked_content = None
        if object.content_type == COURSEITEM_CONTENT_TYPE_MARKDOWN:
            cooked_content = render_markdown(object.text_content)

        self.context.update({
            'page_name_pretty': object.name,
            'object': object,
            'cooked_content': cooked_content
        })
        return render(request, self.template_name, self.context)

class CourseItemUpdateView(InstructorBaseView):
    template_name = "course/course_item_update.html"
    form_class = CourseItemForm
    def get_base_context(self, kwargs):
        return {
            'page_name_pretty': 'Update Course Item',
            'form_action': reverse('course_item_update', kwargs={'course_id': self.course.id, 'item_id': kwargs['item_id']}),
            'SERVER_DATA_JSON': json.dumps({
                'markdown_preview_url': reverse('markdown_preview'),
            }),
        }

    def get(self, request, **kwargs):
        object = get_object_or_404(CourseItem, course=self.course, id=kwargs['item_id'])
        form = self.form_class(instance = object)
        self.context.update({
            **self.get_base_context(kwargs),
            'object': object,
            'form': form,
            })
        return render(request, self.template_name, self.context)

    def post(self, request, **kwargs):
        object = get_object_or_404(CourseItem, course=self.course, id=kwargs['item_id'])
        form = self.form_class(instance = object, data=request.POST)
        self.context.update({
            **self.get_base_context(kwargs),
            'object': object,
            'form': form,
        })
        if not form.is_valid():
            return render(request. self.template_name, self.context)
        form.save()
        return HttpResponseRedirect(reverse('course_item_list', kwargs={'course_id': self.course.id}))

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
            object_class = ItemHeading if form.cleaned_data['is_heading'] else CourseItem
            object = get_object_or_404(object_class, course=self.course, id=form.cleaned_data['id'])
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

        object = get_object_or_404(CourseItem, course=self.course, id=form.cleaned_data['id'])
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

        obj = get_object_or_404(CourseItem, course=self.course, id=form.cleaned_data['id'])
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
            obj = get_object_or_404(CourseItem, course=self.course, id=f.cleaned_data['id'])
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
        self.context.update({'item_list': self.course.get_course_item_list()})
        return render(request, self.template_name, self.context)

class CourseItemHeadingDeleteInlineView(InstructorBaseView):
    form_class = ItemIdForm
    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if(not form.is_valid()):
            return HttpResponseBadRequest();

        obj = get_object_or_404(ItemHeading, course=self.course, id=form.cleaned_data['id'])
        obj.delete()
        return HttpResponse();

class CourseItemHeadingVisibleUpdateInlineView(InstructorBaseView):
    template_name = "course/course_item_list/course_item_heading.html"
    form_class = IdVisibleForm
    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest();

        object = get_object_or_404(ItemHeading, course=self.course, id=form.cleaned_data['id'])
        object.visible = form.cleaned_data['visible']
        object.save()
        self.context.update({'item': object})
        return render(request, self.template_name, self.context)

class MarkdownPreviewView(LoginRequiredMixin, View):
    def post(self, request):
        form = TextForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest()

        return HttpResponse(render_markdown(form.cleaned_data['text']))

class AssignmentListView(TemplateView):
    template_name = "course/course_item_list.html"

class GradebookView(TemplateView):
    template_name = "course/course_item_list.html"

class CourseSettingsView(TemplateView):
    template_name = "course/course_item_list.html"
