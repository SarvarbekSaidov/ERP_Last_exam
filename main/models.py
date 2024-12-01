from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100 , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to='lessons/videos/')
    created_at = models.DateTimeField(auto_now_add=True)
    liked = models.BooleanField(null = True , blank = True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author}'

