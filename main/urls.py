from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, CommentViewSet, register_user

router = DefaultRouter()
router.register('courses', CourseViewSet)
router.register('lessons', LessonViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),   
    path('register/', register_user, name='register'),  
]
