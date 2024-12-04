from rest_framework import serializers
from .models import Course, Lesson, Comment

"""
Serializers to convert python models to JSON
"""


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model.
    """
    class Meta:
        model = Course
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for the Lesson model.
    """
    class Meta:
        model = Lesson
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    """
    class Meta:
        model = Comment
        fields = '__all__'
