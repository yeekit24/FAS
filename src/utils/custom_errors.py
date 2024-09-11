from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR


class ServerError(APIException):
    """Used for manually throwing server_error."""

    status_code = HTTP_500_INTERNAL_SERVER_ERROR
    default_code = "server_error"
    default_detail = "Error. If problem persists, please contact our Jewel Support."
