from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("uid", "applicant", "status", "is_active")
    search_fields = ["uid"]
    list_filter = ("status", "reviewer", "is_active")
    readonly_fields = ["uid", "modified_time"]
    ordering = ("-modified_time",)
