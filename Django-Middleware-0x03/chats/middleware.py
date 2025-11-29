# Create a middleware that logs each user’s requests to a file, including the 
# timestamp, user and the request path.

from django.conf import settings
from django.core.exceptions import PermissionDenied, MiddlewareNotUsed
from datetime import datetime, time
import logging

class RequestLoggingMiddleware:
    """
    Middleware that logs each user's requests to a file, including the timestamp, user, and path
    """
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Set up the logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)


        # File handler
        file_handler = logging.FileHandler('requests.log')

        # console handler
        console_handler = logging.StreamHandler()


        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def __call__(self, request):

        

        response = self.get_response(request)

        user = request.user if hasattr(request, 'user') else 'Unknown user'

        self.logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        return response


class RequestAccessByTimeMiddleware:
    """
    Checks server time and denies access if time is outside 9pm and 6pm
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        
        now = datetime.now().time()
        six = time(18, 0) # Notice that this time is gotten from: from datetime import datetime, time
        nine = time(21, 0)

        if not (six <= now <= nine):
            raise PermissionDenied()

        response = self.get_response(request)
        return response