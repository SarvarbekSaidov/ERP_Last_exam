from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.conf import settings
from .models import Course, Lesson, Comment
from .serializers import CourseSerializer, LessonSerializer, CommentSerializer
from .permissions import  IsAuthorOrAdminOrReadOnly


class BaseViewSet(ModelViewSet):
    """
    Base class for ViewSets for CRUD
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]

    def send_email(self, subject, message):
        """
        Base function for sending emails.
        """
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['saidovsarvarbek02@gmail.com'],   
        )
        print(f'Email sent: {subject}')


class CourseViewSet(BaseViewSet):
    """
    Manage courses: list, create, update, delete.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]   
    filterset_fields = ['category', 'title']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created_at', 'instructor', 'updated_at']
    ordering = ['title']
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'courses'

    def perform_create(self, serializer):
        """
        Creates a new course and sends an email notification.
        """
        course = serializer.save()
        self.send_email(
            subject='New Course Created',
            message=f'A new course "{course.title}" has been created.',
        )


class LessonViewSet(BaseViewSet):
    """
    Manage lessons: list, create, update, delete.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]  
    filterset_fields = ['course', 'title']
    search_fields = ['title', 'description']
    ordering_fields = ['title']
    ordering = ['title']
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'lessons'

    def perform_create(self, serializer):
        """
        Creates a new lesson and sends an email notification.
        """
        lesson = serializer.save()
        self.send_email(
            subject='New Lesson Created',
            message=f'A new lesson "{lesson.title}" has been added to the course "{lesson.course.title}".',
        )


class CommentViewSet(BaseViewSet):
    """
    Manage comments: list, create, update, delete.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    filterset_fields = ['lesson']
    search_fields = ['content']
    ordering_fields = ['created_at']
    ordering = ['created_at']
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'comments'

    def perform_create(self, serializer):
        """
        Creates a new comment and sends an email notification.
        The user field is automatically set by the serializer.
        """
        comment = serializer.save()   
        self.send_email(
            subject='New Comment Added',
            message=f'A new comment has been added to the lesson "{comment.lesson.title}".',
        )


@api_view(['POST'])
def register_user(request):
    """
    Register a new user
    """
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)
    token = Token.objects.create(user=user)
    return Response({'token': token.key, 'message': 'User registered successfully'})
