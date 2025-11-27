# Create a middleware that logs each user’s requests to a file, including the 
# timestamp, user and the request path.

from django.conf import settings
from django.core.exceptions import PermissionDenied, MiddlewareNotUsed
from datetime import datetime
import logging

class RequestLoggingMiddleware:
    """
    Middleware that logs each user's requests to a file, including the timestamp, user, and path
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):

        logging.basicConfig(filename='request.log', filemode='a', encoding='UTF8')
        logging.info(f"{datetime.now()} - User:{request.user} - Path:{request.path}")

        response = self.get_response(request)

        return response