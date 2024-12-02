from django.db import models
from django.contrib.auth.models import User
# create your models here



class Course(models.Model):
    """
    course with a title, description, category, and instructor.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """
    lesson within a course.
    """
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to='lessons/videos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

LIKE_CHOICES = (
    ('like', 'Like'),
    ('dislike', 'Dislike'),
)

class Comment(models.Model):
    """
    user's comment on a lesson with a like/dislike option.
    """
    lesson = models.ForeignKey(Lesson, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    liked = models.CharField(choices=LIKE_CHOICES, max_length=7, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on lesson {self.lesson.title}'
