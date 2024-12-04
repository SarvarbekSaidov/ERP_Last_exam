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
    class Meta:
        model = Comment
        fields = ['id', 'lesson', 'content', 'created_at']  

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
