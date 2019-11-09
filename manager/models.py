from django.conf import settings
from django.db import models

# Create your models here.
class Profile(models.Model):
    """ User details """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        primary_key = True,
    )

    verification_code = models.CharField(
        max_length = 43,
        null = False,
        unique = True,
    )

    verified = models.BooleanField(default = False)

    nickname = models.CharField(
        max_length = 20,
        blank = True,
        help_text = "Enter a nickname you prefer to go by. If provided, your nickname will be "
            "displayed instead of your real name on BCM courses, though instructors can still "
            "look your real name up if they choose."
    )

    institution_id = models.CharField(max_length = 100, blank = True,
        help_text = "If you would like to associate your account with an existing ID at "
            "another institution, enter it here."
    )

    def __str__(self):
        return f"{self.user.get_full_name}'s profile"
