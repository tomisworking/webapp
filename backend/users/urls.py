from django.urls import path

from .views import (
    RegisterView,
    CurrentUserView,
    UserDetailView,
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    logout_view,
    user_threads_view,
    user_posts_view
)

urlpatterns = [
    # Authentication with httpOnly cookies
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', logout_view, name='logout'),
    
    # User profile
    path('user/', CurrentUserView.as_view(), name='current_user'),
    path('users/<int:id>/', UserDetailView.as_view(), name='user_detail'),
    path('users/<int:id>/threads/', user_threads_view, name='user_threads'),
    path('users/<int:id>/posts/', user_posts_view, name='user_posts'),
]
