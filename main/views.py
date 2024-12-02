from django.core.mail import send_mail
from django.conf import settings
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson, Comment
from .serializers import CourseSerializer, LessonSerializer, CommentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

def send_email_notification(subject, message):
    """
    Sends an email notification to the admin when an event occurs.
    Args:
        subject (str): The subject of the email.
        message (str): The content of the email.
    """
    recipient_list = ['saidovsarvarbek@hotmail.com']   
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
    )


class CourseViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage courses. Allows users to list, create, update, and delete courses.
    Only authenticated users can access the course-related endpoints.

    Filters:
        - category: Filters courses by category.
        - title: Filters courses by title.

    Search:
        - title: Searches courses by title.
        - description: Searches courses by description.

    Ordering:
        - title: Orders courses by title.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]  
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filterset_fields = ['category', 'title']   
    search_fields = ['title', 'description']  
    ordering_fields = ['title']   
    ordering = ['title']   

    def perform_create(self, serializer):
        """
        Creates a new course and sends a notification email.
        Args:
            serializer (CourseSerializer): The serializer used to create the course.
        """
        course = serializer.save()
        send_email_notification(
            subject='New Course Created',
            message=f'A new course "{course.title}" has been created.'
        )
        
    def perform_update(self, serializer):
        """
        Updates an existing course and sends a notification email.
        """
        course = serializer.save()
        send_email_notification(
            subject='Course Updated',
            message=f'The course "{course.title}" has been updated.'
        )

    def perform_destroy(self, instance):
        """
        Deletes a course and sends a notification email.
        """
        course_title = instance.title  
        instance.delete()
        send_email_notification(
            subject='Course Deleted',
            message=f'The course "{course_title}" has been deleted.'
        )



class LessonViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage lessons. Allows users to list, create, update, and delete lessons.
    Only authenticated users can access the lesson-related endpoints.
    Filters:
        - course: Filters lessons by course.
        - title: Filters lessons by title.
    Search:
        - title: Searches lessons by title.
        - description: Searches lessons by description.
    Ordering:
        - title: Orders lessons by title.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]  
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filterset_fields = ['course', 'title']   
    search_fields = ['title', 'description']  
    ordering_fields = ['title']   
    ordering = ['title']  

    def perform_create(self, serializer):
        """
        Creates a new lesson and sends a notification email.
        """
        lesson = serializer.save()
        send_email_notification(
            subject='New Lesson Created',
            message=f'A new lesson "{lesson.title}" has been added to the course "{lesson.course.title}".'
        )

    def perform_update(self, serializer):
        """
        Updates an existing lesson and sends a notification email.
        """
        lesson = serializer.save()
        send_email_notification(
            subject='Lesson Updated',
            message=f'The lesson "{lesson.title}" has been updated in the course "{lesson.course.title}".'
        )

    def perform_destroy(self, instance):
        """
        Deletes a lesson and sends a notification email.
        """
        lesson_title = instance.title   
        course_title = instance.course.title
        instance.delete()
        send_email_notification(
            subject='Lesson Deleted',
            message=f'The lesson "{lesson_title}" from the course "{course_title}" has been deleted.'
        )


class CommentViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage comments on lessons. Allows users to list, create, update, and delete comments.
    Only authenticated users can access the comment-related endpoints.

    Filters:
        - lesson: Filters comments by lesson.

    Search:
        - content: Searches comments by content.

    Ordering:
        - created_at: Orders comments by creation date.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filterset_fields = ['lesson']  
    search_fields = ['content']  
    ordering_fields = ['created_at']  
    ordering = ['created_at']   

    def perform_create(self, serializer):
        """
        Creates a new comment and sends a notification email.

        Args:
            serializer (CommentSerializer): The serializer used to create the comment.
        """
        comment = serializer.save(user=self.request.user)  
        send_email_notification(
            subject='New Comment Added',
            message=f'A new comment has been added to the lesson "{comment.lesson.title}".'
        )


@api_view(['POST'])
def register_user(request):
    """
    Registers a new user. Takes username, password, and email as input.
    Args:
        request (Request): The request object containing user data (username, password, email).
    Returns:
        Response: Response with a token for the user if registration is successful, or an error message.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)
    token_object = Token.objects.get_or_create(user=user)[0]
    return Response({'token': token.key, 'message': 'User registered successfully'})


@api_view(['POST'])
def login_user(request):
    """
    Authenticates a user and returns a token. Takes username and password as input.

    Args:
        request (Request): The request object containing username and password.

    Returns:
        Response: Response with a token if login is successful, or an error message.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token_object = Token.objects.get_or_create(user=user)[0]

        return Response({'token': token.key, 'message': 'Login successful'})
    return Response(status=400)


