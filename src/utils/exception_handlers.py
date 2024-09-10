"""DRF exception handlers."""
from typing import Dict, List, Union
from django.core.exceptions import PermissionDenied
from django.http import Http404, JsonResponse

from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import set_rollback

from src.utils.custom_errors import ServerError


def exception_handler(exc, context):
    """exception handler.

    Based off DRF's default handler.
    Returns errors in the format of:
        {
            "errors": [
                "code": "string",
                "message": "string",
            ]
        }
    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.

    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

        errors: List[Dict[str, Union[str, list, dict]]] = []
        if isinstance(exc, exceptions.ValidationError):
            # Assumption here is ONLY validation error will return code/detail
            # as a container type.
            # https://www.django-rest-framework.org/api-guide/exceptions/#validationerror
            for root_field, details in exc.detail.items():
                msgs_by_field = format_validation_error_msg(root_field, details)
                for field, msgs in msgs_by_field.items():
                    errors.extend(
                        [
                            {
                                "code": "validation_error",
                                "message": f"{field}: {msg}",
                            }
                            for msg in msgs
                        ]
                    )
        else:
            errors.append(
                {
                    "code": exc.get_codes(),
                    "message": exc.detail,
                }
            )
        set_rollback()
        return Response({"errors": errors}, status=exc.status_code, headers=headers)
    return None


def format_validation_error_msg(root_field, details):
    """Formats validation error messages.

    Handles nested fields by converting the keys to use dot notation.
    """
    msgs = {}
    if isinstance(details, dict):
        for field in details:
            msgs.update(
                format_validation_error_msg(f"{root_field}.{field}", details[field])
            )
    if isinstance(details, list):
        for msg in details:
            msgs[root_field] = details
    return msgs


def bad_request(request, *args, **kwargs):
    """Generic 400 error handler."""
    data = {"errors": [{"code": "bad_request", "messages": "Bad request"}]}
    return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


def permission_denied(request, *args, **kwargs):
    """Generic 403 error handler."""
    data = {"errors": [{"code": "permission_denied", "messages": "Permission denied"}]}
    return JsonResponse(data, status=status.HTTP_403_FORBIDDEN)


def not_found(request, *args, **kwargs):
    """Generic 404 error handler."""
    data = {"errors": [{"code": "not_found", "messages": "Not found"}]}
    return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)


def server_error(request, *args, **kwargs):
    """Generic 500 error handler."""
    data = {
        "errors": [
            {
                "code": ServerError.default_code,
                "messages": ServerError.default_detail,
            }
        ]
    }
    return JsonResponse(data, status=ServerError.status_code)
