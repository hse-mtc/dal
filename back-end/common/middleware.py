import logging

from django.core.handlers.wsgi import WSGIRequest
from rest_framework.response import Response

logger = logging.getLogger("dal.logging")


class LoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def _log_request(self, request: WSGIRequest) -> None:
        try:
            get = request.GET.copy()
            logger.debug("Request: {}, {}".format(request, get))
        except AttributeError as exc:
            logger.error("Failed to log request: {}".format(exc))

    def _log_response(self, response: Response) -> None:
        try:
            data = response.data.copy()
            logger.debug("Response: {}".format(data))
        except AttributeError as exc:
            logger.error("Failed to log response: {}".format(exc))

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
