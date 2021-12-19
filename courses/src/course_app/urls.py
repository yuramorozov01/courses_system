from course_app import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'course', views.CourseViewSet, basename='Course')

urlpatterns = [
    path('', include(router.urls)),
]
