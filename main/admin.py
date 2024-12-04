from django.contrib import admin
from .models import Course, Lesson, Comment

"""
Customizing admin panel for better usability and control
"""

class CourseAdmin(admin.ModelAdmin):
    """
    Custom admin for the Course model.
    """
    list_display = ('title', 'instructor', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'category')
    list_filter = ('category', 'instructor', 'created_at')
    ordering = ('-created_at',)

class LessonAdmin(admin.ModelAdmin):
    """
    Custom admin for the Lesson model.
    """
    list_display = ('title', 'course', 'created_at')
    search_fields = ('title',)
    list_filter = ('course', 'created_at')
    ordering = ('-created_at',)

class CommentAdmin(admin.ModelAdmin):
    """
    Custom admin for the Comment model.
    """
    list_display = ('author', 'lesson', 'content', 'liked', 'created_at')
    search_fields = ('author__username', 'content')
    list_filter = ('liked', 'created_at', 'lesson')
    ordering = ('-created_at',)

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Comment, CommentAdmin)
