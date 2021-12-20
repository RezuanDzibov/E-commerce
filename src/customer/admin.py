from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from src.customer.forms import CustomerChangeForm, CustomerCreationForm
from src.customer.models import Customer


class CustomerAdmin(UserAdmin):
    add_form = CustomerCreationForm
    form = CustomerChangeForm
    model = Customer
    list_display = ("first_name", "last_name", "email", "is_staff", "is_active")
    list_filter = ("first_name", "last_name", "email", "is_staff", "is_active")
    list_display_links = ("first_name", "last_name", "email")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal information", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ("first_name", "last_name", "email")
    ordering = ("first_name", "last_name", "email")


admin.site.register(Customer, CustomerAdmin)
