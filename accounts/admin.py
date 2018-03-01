from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserChangeForm, UserCreationForm

from accounts.models import User


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'name','phone','nid','role')
    list_filter = ('groups',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'groups')}),
        ('Personal info', {'fields': ('name','address','nid', 'phone', 'email')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    search_fields = ('email','nid','name','username','phone','address')
    ordering = ('-id',)

admin.site.register(User, MyUserAdmin)