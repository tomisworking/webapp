from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Thread, Post
from .serializers import (
    CategorySerializer,
    ThreadListSerializer,
    ThreadDetailSerializer,
    ThreadCreateSerializer,
    PostSerializer
)
from .permissions import IsAuthorOrReadOnly


class CategoryListView(generics.ListAPIView):
    """List all categories with thread and post counts."""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class CategoryDetailView(generics.RetrieveAPIView):
    """Get a specific category by slug."""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class ThreadListView(generics.ListAPIView):
    """
    List threads with filtering, searching, and ordering.
    Public access - no authentication required.
    """
    
    serializer_class = ThreadListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'author__id']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'last_activity', 'views_count']
    ordering = ['-is_pinned', '-last_activity']
    
    def get_queryset(self):
        """Return non-deleted threads."""
        return Thread.objects.filter(is_deleted=False).select_related('author', 'category')


class ThreadCreateView(generics.CreateAPIView):
    """Create a new thread. Requires authentication."""
    
    serializer_class = ThreadCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        thread = serializer.save()
        
        # Return detailed thread data
        output_serializer = ThreadDetailSerializer(thread, context={'request': request})
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class ThreadDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, update, or delete a thread.
    - GET: Public access
    - UPDATE/DELETE: Author only
    """
    
    queryset = Thread.objects.filter(is_deleted=False)
    serializer_class = ThreadDetailSerializer
    permission_classes = [IsAuthorOrReadOnly]
    lookup_field = 'id'
    
    def retrieve(self, request, *args, **kwargs):
        """Increment view count when thread is retrieved."""
        instance = self.get_object()
        instance.increment_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_destroy(self, instance):
        """Soft delete the thread instead of permanent deletion."""
        instance.is_deleted = True
        instance.save()


class PostListView(generics.ListAPIView):
    """
    List posts for a specific thread.
    Public access - no authentication required.
    """
    
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['thread']
    
    def get_queryset(self):
        """Return non-deleted posts."""
        return Post.objects.filter(is_deleted=False).select_related('author', 'thread')


class PostCreateView(generics.CreateAPIView):
    """Create a new post (reply). Requires authentication."""
    
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        """Create a post and return it."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if thread is locked
        thread = serializer.validated_data['thread']
        if thread.is_locked:
            return Response(
                {'error': 'This thread is locked and cannot accept new posts.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        post = serializer.save()
        return Response(
            PostSerializer(post, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, update, or delete a post.
    - GET: Public access
    - UPDATE/DELETE: Author only
    """
    
    queryset = Post.objects.filter(is_deleted=False)
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    lookup_field = 'id'
    
    def perform_destroy(self, instance):
        """Soft delete the post instead of permanent deletion."""
        instance.is_deleted = True
        instance.save()


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def category_threads_view(request, slug):
    """Get all threads for a specific category."""
    try:
        category = Category.objects.get(slug=slug)
        threads = Thread.objects.filter(
            category=category,
            is_deleted=False
        ).select_related('author', 'category').order_by('-is_pinned', '-last_activity')
        
        serializer = ThreadListSerializer(threads, many=True, context={'request': request})
        return Response({
            'category': CategorySerializer(category).data,
            'threads': serializer.data
        })
    except Category.DoesNotExist:
        return Response(
            {'error': 'Category not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def thread_with_posts_view(request, id):
    """Get a thread with all its posts."""
    try:
        thread = Thread.objects.get(id=id, is_deleted=False)
        thread.increment_views()
        
        posts = Post.objects.filter(
            thread=thread,
            is_deleted=False
        ).select_related('author').order_by('created_at')
        
        return Response({
            'thread': ThreadDetailSerializer(thread, context={'request': request}).data,
            'posts': PostSerializer(posts, many=True, context={'request': request}).data
        })
    except Thread.DoesNotExist:
        return Response(
            {'error': 'Thread not found'},
            status=status.HTTP_404_NOT_FOUND
        )
