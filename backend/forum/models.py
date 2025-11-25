import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
import bleach


class Category(models.Model):
    """Forum category model."""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=500)
    icon = models.CharField(max_length=50, default='💬', help_text='Emoji or icon identifier')
    order = models.IntegerField(default=0, help_text='Display order (lower numbers first)')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'categories'
        ordering = ['order', 'name']
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def thread_count(self):
        """Return the number of threads in this category."""
        return self.threads.filter(is_deleted=False).count()
    
    @property
    def post_count(self):
        """Return the total number of posts in this category's threads."""
        return Post.objects.filter(
            thread__category=self,
            is_deleted=False
        ).count()


class Thread(models.Model):
    """Forum thread (discussion topic) model."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, blank=True)
    content = models.TextField()
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='threads'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='threads'
    )
    
    views_count = models.IntegerField(default=0)
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'threads'
        ordering = ['-is_pinned', '-last_activity']
        indexes = [
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['-last_activity']),
            models.Index(fields=['is_deleted', '-last_activity']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Auto-generate slug and sanitize content."""
        if not self.slug:
            self.slug = slugify(self.title)[:250]
        
        # Sanitize HTML content
        allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'a', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre']
        allowed_attrs = {'a': ['href', 'title']}
        self.content = bleach.clean(
            self.content,
            tags=allowed_tags,
            attributes=allowed_attrs,
            strip=True
        )
        
        super().save(*args, **kwargs)
    
    @property
    def post_count(self):
        """Return the number of posts (replies) in this thread."""
        return self.posts.filter(is_deleted=False).count()
    
    def increment_views(self):
        """Increment the view counter."""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def update_last_activity(self):
        """Update last activity timestamp."""
        self.last_activity = timezone.now()
        self.save(update_fields=['last_activity'])


class Post(models.Model):
    """Forum post (reply) model."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    content = models.TextField()
    
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'posts'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['thread', 'created_at']),
            models.Index(fields=['author', '-created_at']),
        ]
    
    def __str__(self):
        return f'Post by {self.author.username} on {self.thread.title}'
    
    def save(self, *args, **kwargs):
        """Sanitize content and update thread activity."""
        # Sanitize HTML content
        allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'a', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre']
        allowed_attrs = {'a': ['href', 'title']}
        self.content = bleach.clean(
            self.content,
            tags=allowed_tags,
            attributes=allowed_attrs,
            strip=True
        )
        
        is_new = self._state.adding
        super().save(*args, **kwargs)
        
        # Update thread's last activity when a new post is created
        if is_new:
            self.thread.update_last_activity()
