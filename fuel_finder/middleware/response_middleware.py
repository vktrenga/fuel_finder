
import json
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

class StandardResponseMiddleware(MiddlewareMixin):
    EXCLUDE_PATHS = [
        "/api/schema",
        "/api/docs",
        "/api/redoc",
    ]
     
    def process_response(self, request, response):
        for path in self.EXCLUDE_PATHS:
            if request.path.startswith(path):
                return response

        # Skip non-JSON responses (like file downloads)
        if not hasattr(response, "data"):
            return response

        # Determine status
        if 200 <= response.status_code < 300:
            status_text = "success"
            message = "Request successful"
            error = None
        else:
            status_text = "failed"
            message = getattr(response, "status_text", "Request failed")
            error = getattr(response, "data", None)
            response.data = None

        # Wrap the original data
        standard_response = {
            "status": status_text,
            "message": message,
            "data": response.data,
            "error": error,
        }

        return JsonResponse(standard_response, status=response.status_code)
