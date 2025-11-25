from django.urls import path
from .views import (
    CategoryListView,
    CategoryDetailView,
    ThreadListView,
    ThreadCreateView,
    ThreadDetailView,
    PostListView,
    PostCreateView,
    PostDetailView,
    category_threads_view,
    thread_with_posts_view
)

urlpatterns = [
    # Categories
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('categories/<slug:slug>/threads/', category_threads_view, name='category_threads'),
    
    # Threads
    path('threads/', ThreadListView.as_view(), name='thread_list'),
    path('threads/create/', ThreadCreateView.as_view(), name='thread_create'),
    path('threads/<uuid:id>/', ThreadDetailView.as_view(), name='thread_detail'),
    path('threads/<uuid:id>/posts/', thread_with_posts_view, name='thread_with_posts'),
    
    # Posts
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/<uuid:id>/', PostDetailView.as_view(), name='post_detail'),
]
