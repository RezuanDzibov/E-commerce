from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from . import models


class CustomerCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = models.Customer
        fields = ("first_name", "last_name", "email")


class CustomerChangeForm(UserChangeForm):
    class Meta:
        model = models.Customer
        fields = ("first_name", "last_name", "email")
