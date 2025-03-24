from django.contrib import admin
from .models import DriverMatch  # Import necessary models

@admin.register(DriverMatch)
class DriverMatchAdmin(admin.ModelAdmin):
    list_display = ("id", "driver")  # Display only valid fields

    search_fields = ("driver__username", "car_owner__username")  # Enable search by related user fields
    list_filter = ()  # Remove invalid filters

    ordering = ()  # Remove invalid ordering


    actions = ["approve_match", "reject_match"]  # Define custom admin actions

    def approve_match(self, request, queryset):
        queryset.update(status="Approved")
        self.message_user(request, "Selected matches have been approved.")
    approve_match.short_description = "Approve selected matches"

    def reject_match(self, request, queryset):
        queryset.update(status="Rejected")
        self.message_user(request, "Selected matches have been rejected.")
    reject_match.short_description = "Reject selected matches"

# Register additional models if they exist
# from .models import AnotherModel  # Example: Import other models


# @admin.register(AnotherModel)
# class AnotherModelAdmin(admin.ModelAdmin):
#     list_display = ("id", "name", "created_at")  # Adjust based on model fields
#     search_fields = ("name",)
#     list_filter = ("created_at",)
#     ordering = ("-created_at",)


# If there are more models, register them similarly.
