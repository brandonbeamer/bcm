from django import forms
from django.forms import ModelForm, Form
from django.forms.widgets import TextInput
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import CourseItem, ItemHeading, Attendance

# class OptionalCreateItemHeadingForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['name'].required = False
#
#     class Meta:
#         model = ItemHeading
#         fields = ['name']

class CourseItemForm(ModelForm):
    class Meta:
        model = CourseItem
        fields = [
            'content_type',
            'url_content',
            'text_content',
            'name',
            'description',
            'visible',
        ]
        # widgets = {
        # # To stop browsers from trying to verify the URL themselves
        #     'url_content': TextInput(attrs={'maxlength': 200})
        # }

class ItemHeadingCreateInlineForm(ModelForm):
    class Meta:
        model = ItemHeading
        fields = ['name']

class ItemOrderUpdateInlineForm(Form):
    is_heading = forms.BooleanField(required = False)
    id = forms.IntegerField()
    order = forms.IntegerField()

class ItemIdForm(Form):
    id = forms.IntegerField()

class IdVisibleForm(Form):
    id = forms.IntegerField()
    visible = forms.BooleanField(required = False)

class TextForm(Form):
    text = forms.CharField()

class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance
        fields = ['user', 'status']
        widgets = {
            'user': forms.HiddenInput(),
            'status': forms.RadioSelect(attrs = {'class': 'attendance-status'}),
        }
