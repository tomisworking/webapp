from rest_framework import serializers
from .models import Category, Thread, Post
from users.serializers import UserListSerializer
import bleach


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category with thread and post counts."""
    
    thread_count = serializers.ReadOnlyField()
    post_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'icon',
            'order', 'thread_count', 'post_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ThreadListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for thread listings."""
    
    author = UserListSerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    post_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Thread
        fields = [
            'id', 'title', 'slug', 'author', 'category_name',
            'category_slug', 'views_count', 'post_count',
            'is_pinned', 'is_locked', 'created_at', 'last_activity'
        ]
        read_only_fields = [
            'id', 'slug', 'views_count', 'created_at', 'last_activity'
        ]


class ThreadDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single thread view."""
    
    author = UserListSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    post_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Thread
        fields = [
            'id', 'title', 'slug', 'content', 'author', 'category',
            'category_id', 'views_count', 'post_count', 'is_pinned',
            'is_locked', 'created_at', 'updated_at', 'last_activity'
        ]
        read_only_fields = [
            'id', 'slug', 'author', 'views_count',
            'created_at', 'updated_at', 'last_activity'
        ]
    
    def validate_content(self, value):
        """Sanitize HTML content to prevent XSS attacks."""
        # Allow only safe tags and attributes
        allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'a', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre']
        allowed_attrs = {'a': ['href', 'title']}
        
        # Clean the content
        cleaned = bleach.clean(
            value,
            tags=allowed_tags,
            attributes=allowed_attrs,
            strip=True
        )
        return cleaned
    
    def create(self, validated_data):
        """Set the author to the current user."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    """Serializer for posts (replies)."""
    
    author = UserListSerializer(read_only=True)
    thread_id = serializers.PrimaryKeyRelatedField(
        queryset=Thread.objects.filter(is_deleted=False, is_locked=False),
        source='thread',
        write_only=True
    )
    thread_title = serializers.CharField(source='thread.title', read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'thread_id', 'thread_title', 'author', 'content',
            'is_edited', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'author', 'is_edited', 'created_at', 'updated_at'
        ]
    
    def validate_content(self, value):
        """Sanitize HTML content to prevent XSS attacks."""
        # Allow only safe tags and attributes
        allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'a', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre']
        allowed_attrs = {'a': ['href', 'title']}
        
        # Clean the content
        cleaned = bleach.clean(
            value,
            tags=allowed_tags,
            attributes=allowed_attrs,
            strip=True
        )
        return cleaned
    
    def create(self, validated_data):
        """Set the author to the current user."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Mark post as edited when updated."""
        instance.is_edited = True
        return super().update(instance, validated_data)


class ThreadCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating threads."""
    
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category'
    )
    
    class Meta:
        model = Thread
        fields = ['title', 'content', 'category_id']
    
    def validate_content(self, value):
        """Sanitize HTML content to prevent XSS attacks."""
        # Allow only safe tags and attributes
        allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'a', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre']
        allowed_attrs = {'a': ['href', 'title']}
        
        # Clean the content
        cleaned = bleach.clean(
            value,
            tags=allowed_tags,
            attributes=allowed_attrs,
            strip=True
        )
        return cleaned
    
    def create(self, validated_data):
        """Set the author to the current user."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
