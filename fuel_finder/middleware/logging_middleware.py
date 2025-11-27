import json
import time
import logging

logger = logging.getLogger("api_logger")

class APILoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        # ---------- REQUEST LOG ----------
        method = request.method
        path = request.path

        query_params = dict(request.GET)

        try:
            body = request.body.decode("utf-8")
            body_json = json.loads(body) if body else {}
        except:
            body_json = "Non-JSON Body"

        logger.info(
            f"[REQUEST] {method} {path} | "
            f"Query={query_params} | Body={body_json}"
        )

        # ---------- RESPONSE ----------
        response = self.get_response(request)

        execution_time = round(time.time() - start_time, 4)

        # try:
        #     response_data = response.content.decode("utf-8")
        # except:
        #     response_data = "Non-JSON Response"

        logger.info(
            f"[RESPONSE] {method} {path} | "
            f"Status={response.status_code} | "
            f"Time={execution_time}s"
        )

        return response
