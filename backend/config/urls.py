"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.decorators.cache import never_cache

# Health check endpoint for AWS ALB
@never_cache
def health_check(request):
    """
    Simple health check endpoint for Load Balancer
    Returns 200 OK if application is running
    """
    return JsonResponse({
        'status': 'healthy',
        'service': 'forum-backend'
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/', include('forum.urls')),
    path('api/health/', health_check, name='health_check'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
