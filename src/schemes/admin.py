from django.contrib import admin

from .models import Scheme, SchemeBenefit, SchemeCriteria


class InlineBenefitAdmin(admin.TabularInline):
    model = SchemeBenefit
    readonly_fields = ["uid", "modified_time"]


class InlineCriteriaAdmin(admin.TabularInline):
    model = SchemeCriteria
    readonly_fields = ["uid", "modified_time"]


@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = ("uid", "name", "is_active")
    search_fields = ["name"]
    list_filter = ["is_active"]
    readonly_fields = ["uid", "modified_time"]
    ordering = ("-modified_time",)
    inlines = [InlineBenefitAdmin, InlineCriteriaAdmin]
