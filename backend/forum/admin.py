from django.contrib import admin
from .models import Category, Thread, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""
    
    list_display = ['name', 'slug', 'icon', 'order', 'created_at']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    ordering = ['order', 'name']


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    """Admin configuration for Thread model."""
    
    list_display = [
        'title', 'author', 'category', 'views_count',
        'is_pinned', 'is_locked', 'is_deleted', 'created_at'
    ]
    list_filter = ['category', 'is_pinned', 'is_locked', 'is_deleted', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['id', 'views_count', 'created_at', 'updated_at', 'last_activity']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'content', 'author', 'category')
        }),
        ('Status', {
            'fields': ('is_pinned', 'is_locked', 'is_deleted')
        }),
        ('Statistics', {
            'fields': ('views_count', 'created_at', 'updated_at', 'last_activity')
        }),
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin configuration for Post model."""
    
    list_display = ['thread', 'author', 'is_edited', 'is_deleted', 'created_at']
    list_filter = ['is_edited', 'is_deleted', 'created_at']
    search_fields = ['content', 'author__username', 'thread__title']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('thread', 'author', 'content')
        }),
        ('Status', {
            'fields': ('is_edited', 'is_deleted')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
