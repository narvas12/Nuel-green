import logging

class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        # Log visitor information
        visitor_ip = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT')
        self.logger.info(f"Visitor IP: {visitor_ip}, User Agent: {user_agent}")

        response = self.get_response(request)
        return response
