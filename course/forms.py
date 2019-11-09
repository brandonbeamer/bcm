from django.forms import ModelForm
from django.forms.widgets import TextInput
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import GeneralCourseItem, ModelWithContent


class CreateGeneralCourseItemForm(ModelForm):
    class Meta:
        model = GeneralCourseItem
        fields = [
            'content_type',
            'url_content',
            'text_content',
            'name',
            'description',
            'category',
            'visible',
        ]
        widgets = {
        # To stop browsers from trying to verify the URL themselves 
            'url_content': TextInput(attrs={'maxlength': 200})
        }
