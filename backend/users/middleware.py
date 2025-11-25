"""
Middleware for handling JWT authentication via httpOnly cookies.
"""


class JWTAuthCookieMiddleware:
    """
    Middleware that extracts JWT token from httpOnly cookies
    and adds it to the Authorization header for JWT authentication.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get access token from cookie
        access_token = request.COOKIES.get('access_token')
        
        # If token exists in cookie and not already in Authorization header
        if access_token and not request.META.get('HTTP_AUTHORIZATION'):
            # Add token to Authorization header
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
        
        response = self.get_response(request)
        return response






