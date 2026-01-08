"""
Custom middleware for additional security headers.
"""


class SecurityHeadersMiddleware:
    """
    Middleware to add security headers to all responses.
    This is a fallback in case Nginx headers are not applied.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Only add headers if they're not already present (Nginx should add them)
        if 'X-Content-Type-Options' not in response:
            response['X-Content-Type-Options'] = 'nosniff'
        
        if 'X-Frame-Options' not in response:
            response['X-Frame-Options'] = 'DENY'
        
        if 'Referrer-Policy' not in response:
            response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        if 'Permissions-Policy' not in response:
            response['Permissions-Policy'] = (
                'geolocation=(), microphone=(), camera=(), '
                'payment=(), usb=(), magnetometer=(), '
                'gyroscope=(), accelerometer=()'
            )
        
        # CSP - only if not already set by Nginx
        if 'Content-Security-Policy' not in response:
            response['Content-Security-Policy'] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:; "
                "connect-src 'self' https://kongoapp.pl; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "form-action 'self'; "
                "upgrade-insecure-requests;"
            )
        
        return response
