from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from . import models

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = models.Customer
        fields = ("first_name", "last_name", "email")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = models.Customer
        fields = ("first_name", "last_name", "email")