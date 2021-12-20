from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from src.customer.models import Customer


class CustomerCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Customer
        fields = ("first_name", "last_name", "email")


class CustomerChangeForm(UserChangeForm):
    class Meta:
        model = Customer
        fields = ("first_name", "last_name", "email")
