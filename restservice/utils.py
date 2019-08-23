from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if issubclass(exc.__class__, ObjectDoesNotExist):
        response = Response(exc.args[0], status=status.HTTP_404_NOT_FOUND)

    return response
