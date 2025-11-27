from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError

def custom_exception_handler(exc, context):
    """
    Global exception handler for DRF.
    """

    # Let DRF handle common exceptions first
    response = exception_handler(exc, context)

    # If DRF already handled it (ValidationError, NotFound, etc), return it
    if response is not None:
        return response

    # Handle Django ValidationError (not DRF's)
    if isinstance(exc, ValidationError):
        return Response(
            {"error": "Validation failed", "details": exc.message},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Handle ObjectDoesNotExist
    if isinstance(exc, ObjectDoesNotExist):
        return Response(
            {"error": "Object not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Handle DB integrity issues (duplicate key, null constraint, foreign key missing)
    if isinstance(exc, IntegrityError):
        return Response(
            {
                "error": "Database integrity error",
                "details": str(exc).replace("\n", "")
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Fallback — Unknown error
    return Response(
        {
            "error": "Internal server error",
            "details": str(exc)
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
