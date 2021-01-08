import logging

from django.core.handlers.wsgi import WSGIRequest
from rest_framework.response import Response


class LoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

        # One-time configuration and initialization.
        self.logger = logging.getLogger("dal.logs")

    def _log_request(self, request: WSGIRequest) -> None:
        try:
            self.logger.debug("Request: %s, %s", request, request.GET.copy())
        except AttributeError as exc:
            self.logger.error("Failed to log request: %s", exc)

    def _log_response(self, response: Response) -> None:
        try:
            self.logger.debug("Response: %s", response.data.copy())
        except AttributeError as exc:
            self.logger.error("Failed to log response: %s", exc)

    def __call__(self, request: WSGIRequest):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        self._log_request(request)

        # Process request
        response: Response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        self._log_response(response)

        # Propagate response further
        return response
