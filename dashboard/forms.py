from django.forms import ModelForm, PasswordInput

from course.models import Course
from manager.models import Profile

class EnrollForm(ModelForm):
    class Meta:
        model = Course
        fields = ['password']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'institution_id']
