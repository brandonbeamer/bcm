from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import View, TemplateView, ListView, DetailView, FormView, CreateView, UpdateView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password, check_password

from course.models import Course, Enrollment
from manager.models import Profile
from manager.forms import UserForm
from .forms import EnrollForm, ProfileForm

# Helper functions
def is_enrolled(user, course):
    if Enrollment.objects.filter(user = user, course = course).count() != 0:
        return True
    else:
        return False

# Create your views here.
class AccountView(LoginRequiredMixin, View):
    template_name = "dashboard/account.html"
    extra_context = {
        'view_name': 'account',
        'view_name_pretty': 'Account'
    }

    user_form = UserForm
    pass_form = PasswordChangeForm

    def get(self, request):
        user_form = self.user_form(instance = request.user)
        pass_form = self.pass_form(request.user)
        context = {
            'user_form': user_form,
            'pass_form': pass_form,
        }

        return render(request, self.template_name, {**self.extra_context, **context})

    def post(self, request):
        context = None # define context outside the if scope

        if request.POST.get('update_user') is not None:
            # User submitted updated user information
            user_form = self.user_form(request.POST, instance = request.user)
            pass_form = self.pass_form(user = request.user)
            context = {'user_form': user_form, 'pass_form': pass_form}

            if user_form.is_valid():
                user_form.save()
                context['user_success'] = True

        else:
            # User submitted updated password information
            user_form = self.user_form(instance = request.user)
            pass_form = self.pass_form(user = request.user, data = request.POST)
            context = {'user_form': user_form, 'pass_form': pass_form}
            if pass_form.is_valid():
                pass_form.save()
                update_session_auth_hash(request, request.user)
                context['pass_success'] = True

        return render(request, self.template_name, {**self.extra_context, **context})

class CreateCourseView(LoginRequiredMixin, CreateView):
    model = Course
    template_name = 'dashboard/create_course.html'
    success_url = reverse_lazy('my_courses');
    fields = ['name', 'code', 'password']

    def form_valid(self, form):
        #name, code, and password provided
        password = form.cleaned_data['password']
        self.object = form.save(commit = False)

        #creator and initial enrollment needed
        self.object.creator = self.request.user
        if password: # If it's not blank, hash it
            self.object.password = make_password(form.cleaned_data['password'])

        self.object.save()

        Enrollment.objects.create(
            course = self.object,
            user   = self.request.user,
            role   = Enrollment.INSTRUCTOR,
        ).save()

        return HttpResponseRedirect(self.get_success_url())


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = 'create_course'
        context['view_name_pretty'] = 'Create Course'
        return context

    pass

class EnrollView(LoginRequiredMixin, View):
    form = EnrollForm
    template_name = "dashboard/enroll.html"

    def get(self, request, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['pk'])
        form = self.form()
        if is_enrolled(request.user, course):
            return render(request, self.template_name,
                {'course': course,
                 'already_enrolled': True})

        # Valid course id and not already enrolled, let's jam
        return render(request, self.template_name, {'course': course, 'form': form})

    def post(self, request, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['pk'])
        form = self.form(request.POST)

        # Even for post requests, make sure user isn't enrolled already
        if is_enrolled(request.user, course):
            return render(request, self.template_name,
                {'course': course,
                 'already_enrolled': True})

        if course.password:
            # If the course has a password, check the form

            if not form.is_valid(): # return w/ form.errors and no success flag
                return render(request, self.template_name,
                    {'course': course, 'form': form})

            if not check_password(form.cleaned_data['password'], course.password):
                form.add_error('password', 'The password you provided is incorrect.')
                return render(request, self.template_name,
                    {'course': course, 'form': form})

        # form is valid and password matches if it needs to, actually enroll the user
        Enrollment.objects.create(
            user = request.user,
            course = course,
            role = Enrollment.STUDENT
        ).save()

        return render(request, self.template_name,
            {'course': course, 'success': True})

class FindCourseView(LoginRequiredMixin, ListView):
    template_name = "dashboard/find_course.html"
    def get_queryset(self):
        return Course.objects.exclude(members = self.request.user)

class MyCoursesView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "dashboard/my_courses.html"

    def get_queryset(self):
        return self.model.objects.filter(members = self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = 'my_courses'
        context['view_name_pretty'] = 'My Courses'
        return context

class OverviewView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = 'overview'
        context['view_name_pretty'] = 'Overview'

        # Get Course ListView
        context['course_list'] = Course.objects.filter(members = self.request.user)

        return context

class ProfileView(LoginRequiredMixin, View):
    template_name = "dashboard/profile.html"
    form = ProfileForm
    extra_context = {
        'view_name': 'profile',
        'view_name_pretty': 'Profile'
    }

    def get(self, request):
        profile = request.user.profile
        form = self.form(instance = profile)
        context = {'form': form}
        return render(request, self.template_name, {**self.extra_context, **context})

    def post(self, request):
        profile = request.user.profile
        form = self.form(request.POST, instance = profile)
        context = {'form': form}
        if form.is_valid():
            form.save()
            context['success'] = True

        return render(request, self.template_name, {**self.extra_context, **context})
