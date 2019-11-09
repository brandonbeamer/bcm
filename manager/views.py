from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import views as auth_views, forms as auth_forms, models as auth_models
from django.views import View
from django.forms import ModelForm
from django.template.loader import render_to_string

from django.core.mail import send_mail
from smtplib import SMTPException

from .forms import UserForm, CredForm
from .models import Profile

from bcm.settings import cfg

import secrets

# Create your views here.
def index(request):
    # check if user is authenticated
    # redirect to dashboard if they are
    # otherwise redirect to login page

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('overview'))
    else:
        return HttpResponseRedirect(reverse('login'))

def verify(request, code=''):
    template_name = 'manager/verify.html'
    try:
        prof = Profile.objects.get(verification_code = code)
    except Profile.DoesNotExist:
        return render(request, template_name,
        {'status': 'not_found'})

    if prof.verified:
        return render(request, template_name,
        {'status': 'already_verified'})


    prof.verified = True
    prof.save()
    return render(request, template_name, {'status': 'success'})



class Login(auth_views.LoginView):
    template_name = 'manager/login.html'
    redirect_authenticated_user = True

class Logout(auth_views.LogoutView):
    pass

class Signup(View):
    input_template = 'manager/signup.html'
    done_template  = 'manager/signup-done.html'

    def get(self, request):
        cred_form = CredForm(); #auth_forms.UserCreationForm()
        user_form = UserForm()
        return render(request, self.input_template,
        {
            'cred_form': cred_form,
            'user_form': user_form
        })

    def post(self, request):
        cred_form = CredForm(request.POST) #auth_forms.UserCreationForm(request.POST)
        user_form = UserForm(request.POST)
        if cred_form.is_valid() and user_form.is_valid():
            # Set things up and send a confirmation email
            verification_code = secrets.token_urlsafe(32)
            verification_url = cfg['url_prefix'] + reverse('verify', args=[verification_code])

            # Try to send the mail
            try:
                send_mail(
                    '[BCM] Email Verification',
                    render_to_string('manager/emails/verification.html',
                        {
                            'first_name': user_form.cleaned_data['first_name'],
                            'verification_url': verification_url,
                            'use_html': False
                        }),
                    'noreply@brandonbeamer.com',
                    [user_form.cleaned_data['email']],
                    fail_silently = False,
                    html_message = render_to_string('manager/emails/verification.html',
                        {
                            'first_name': user_form.cleaned_data['first_name'],
                            'verification_url': verification_url,
                            'use_html': True
                        })
                )
            except SMTPException:
                return render(request, self.input_template,
                {
                    'cred_form': cred_form,
                    'user_form': user_form,
                    'smtp_error': True,
                })

            # Email was sent, better get on with making the user/profile!
            # Create a user
            new_user = auth_models.User.objects.create_user(
                cred_form.cleaned_data['username'],
                user_form.cleaned_data['email'],
                cred_form.cleaned_data['password1']
            )

            new_user.first_name = user_form.cleaned_data['first_name']
            new_user.last_name = user_form.cleaned_data['last_name']


            new_profile = Profile(
                user = new_user,
                verification_code = verification_code
            )

            new_user.save()
            new_profile.save()

            return render(request, self.done_template, {'email': user_form.cleaned_data['email']})
        else:
            return render(request, self.input_template,
            {
                'cred_form': cred_form,
                'user_form': user_form,
            })
