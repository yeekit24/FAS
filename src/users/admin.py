import datetime
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin

import pytz

from src.users.models import User


def to_local_date(val: str) -> datetime.datetime:
    return pytz.timezone(settings.TIME_ZONE).localize(
        datetime.datetime.strptime(val, "%Y-%m-%d")
    )


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "email",
                    "username",
                    "password",
                    "last_login",
                    "date_joined",
                )
            },
        ),
        (
            "Settings",
            {
                "classes": ("collapse",),
                "fields": (),
            },
        ),
        (
            "Permissions",
            {
                "classes": ("collapse",),
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    readonly_fields = ["uid"]
    list_display = ["uid", "username", "name", "is_superuser"]
    search_fields = ["name"]
