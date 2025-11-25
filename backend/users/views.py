from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from django.conf import settings

from .serializers import (
    RegisterSerializer,
    UserSerializer,
    UserProfileSerializer,
    UserListSerializer
)

User = get_user_model()


def set_auth_cookies(response, access_token, refresh_token=None):
    """
    Helper function to set httpOnly cookies for JWT tokens.
    """
    # Set access token cookie
    response.set_cookie(
        key='access_token',
        value=access_token,
        max_age=int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
        secure=not settings.DEBUG,  # True in production (HTTPS only)
        httponly=True,  # Not accessible via JavaScript
        samesite='Lax'  # CSRF protection
    )
    
    # Set refresh token cookie if provided
    if refresh_token:
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
            secure=not settings.DEBUG,
            httponly=True,
            samesite='Lax'
        )


class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Custom login view that sets JWT tokens in httpOnly cookies.
    """
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            
            # Set tokens in httpOnly cookies
            set_auth_cookies(response, access_token, refresh_token)
            
            # Remove tokens from response body for security
            response.data = {
                'message': 'Login successful'
            }
        
        return response


class CookieTokenRefreshView(TokenRefreshView):
    """
    Custom refresh view that uses refresh token from cookies.
    """
    
    def post(self, request, *args, **kwargs):
        # Get refresh token from cookie
        refresh_token = request.COOKIES.get('refresh_token')
        
        if not refresh_token:
            return Response(
                {'error': 'Refresh token not found'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Add refresh token to request data
        request.data._mutable = True
        request.data['refresh'] = refresh_token
        request.data._mutable = False
        
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data.get('access')
            
            # Set new access token in cookie
            set_auth_cookies(response, access_token)
            
            # If rotation is enabled, set new refresh token
            if 'refresh' in response.data:
                response.set_cookie(
                    key='refresh_token',
                    value=response.data['refresh'],
                    max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
                    secure=not settings.DEBUG,
                    httponly=True,
                    samesite='Lax'
                )
            
            # Remove tokens from response body
            response.data = {'message': 'Token refreshed successfully'}
        
        return response


class RegisterView(generics.CreateAPIView):
    """User registration endpoint with httpOnly cookies."""
    
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens for the new user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        response = Response({
            'user': UserSerializer(user).data,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
        
        # Set tokens in httpOnly cookies
        set_auth_cookies(response, access_token, refresh_token)
        
        return response


class CurrentUserView(generics.RetrieveUpdateAPIView):
    """Get or update current user profile."""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        return self.request.user


class UserDetailView(generics.RetrieveAPIView):
    """Get public user profile."""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    Logout endpoint that clears httpOnly cookies and blacklists the refresh token.
    """
    try:
        # Get refresh token from cookie
        refresh_token = request.COOKIES.get('refresh_token')
        
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        response = Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
        
        # Delete cookies
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        
        return response
    except Exception as e:
        # Even if blacklisting fails, still clear cookies
        response = Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_threads_view(request, id):
    """Get all threads created by a specific user."""
    from forum.serializers import ThreadListSerializer
    
    try:
        user = User.objects.get(id=id)
        threads = user.threads.all().order_by('-created_at')
        serializer = ThreadListSerializer(threads, many=True, context={'request': request})
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_posts_view(request, id):
    """Get all posts created by a specific user."""
    from forum.serializers import PostSerializer
    
    try:
        user = User.objects.get(id=id)
        posts = user.posts.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
