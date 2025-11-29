# Create a middleware that logs each user’s requests to a file, including the 
# timestamp, user and the request path.

from django.conf import settings
from django.core.exceptions import PermissionDenied, MiddlewareNotUsed
from datetime import datetime, time, timedelta
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


class RestrictAccessByTimeMiddleware:
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

from django.core.cache import cache
from django.http import JsonResponse

class OffensiveLanguageMiddleware:
    """
    Limits sending to a maximum of 5 messages per minute per IP address
    """
    MAX_REQUESTS = 5
    TIME_WINDOW = 60  # seconds
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only apply rate limiting to POST requests on /api/messages/
        if request.method == 'POST' and request.path == '/api/messages/':
            ip_address = self.get_client_ip(request)
            cache_key = f'rate_limit_{ip_address}'
            
            # Get current request count and timestamps from cache
            request_times = cache.get(cache_key, [])
            
            # Remove timestamps older than TIME_WINDOW
            current_time = datetime.now()
            cutoff_time = current_time - timedelta(seconds=self.TIME_WINDOW)
            request_times = [t for t in request_times if t > cutoff_time]
            
            # Check if limit exceeded
            if len(request_times) >= self.MAX_REQUESTS:
                return JsonResponse(
                    {'error': 'Rate limit exceeded. Maximum 5 messages per minute.'},
                    status=429
                )
            
            # Add current request timestamp
            request_times.append(current_time)
            cache.set(cache_key, request_times, self.TIME_WINDOW)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Get the client's IP address from the request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip