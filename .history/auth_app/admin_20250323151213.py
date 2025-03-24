from django.contrib import admin  
from django.contrib.auth.admin import UserAdmin

from django.utils.html import format_html
from auth_app.models import CustomUser  # ✅ Use absolute import

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'unique_id', 'is_verified', 'is_staff', 'password_last_changed_display', 'password_reset_token')
    search_fields = ('username', 'email', 'unique_id')
    list_filter = ('role', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),  
        ('Personal Info', {'fields': ('unique_id', 'role', 'password_reset_token')}),  
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),  # ✅ Groups visible here
        ('Important Dates', {'fields': ('last_login', 'date_joined', 'password_last_changed')}),  
    )

    readonly_fields = ('unique_id', 'password_last_changed', 'password_reset_token')  # ✅ unique_id is now read-only

    def password_last_changed_display(self, obj):
        return obj.password_last_changed.strftime("%Y-%m-%d %H:%M:%S") if obj.password_last_changed else "Never Changed"
    password_last_changed_display.short_description = "Password Last Changed"

    def has_delete_permission(self, request, obj=None):
        return True  # ✅ Admins can delete users

    def is_verified(self, obj):
        """ ✅ Show a green checkmark if the user is verified """
        if obj.is_active:  # If email is verified, show green checkmark
            return format_html('<span style="color:green; font-weight:bold;">✔️</span>')
        return format_html('<span style="color:red; font-weight:bold;">❌</span>')  # Show ❌ if not verified
    is_verified.short_description = "Verified"

admin.site.register(CustomUser, CustomUserAdmin)
