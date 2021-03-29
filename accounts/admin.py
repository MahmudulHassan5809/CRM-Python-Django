from django.utils.html import format_html
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username','user_type','branch','password1', 'password2',)
        }),
    )
    model = User
    list_display = ['email', 'username', 'first_name',
                    'last_name', 'is_staff', 'branch','user_type','active']
    list_filter = ['is_staff', 'user_type']
    list_editable = ['user_type','branch','active']
    list_perpage = 20


admin.site.register(User, CustomUserAdmin)
