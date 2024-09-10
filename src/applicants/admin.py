from django.contrib import admin

from .models import Applicant, ApplicantHousehold


class InlineHouseholdAdmin(admin.TabularInline):
    model = ApplicantHousehold
    readonly_fields = ["modified_time"]
    ordering = ("-modified_time",)


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ("uid", "name", "is_active")
    search_fields = ["uid", "name"]
    list_filter = ("marital_status", "employment_status", "sex", "is_active")
    readonly_fields = ["uid", "modified_time"]
    ordering = ("-modified_time",)
    inlines = [
        InlineHouseholdAdmin,
    ]
