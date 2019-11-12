from django.forms import ModelForm
from django.forms.widgets import TextInput
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import GeneralCourseItem
# class OptionalCreateItemHeadingForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['name'].required = False
#
#     class Meta:
#         model = ItemHeading
#         fields = ['name']

class CreateGeneralCourseItemForm(ModelForm):
    class Meta:
        model = GeneralCourseItem
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
