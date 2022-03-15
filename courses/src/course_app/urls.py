from django.urls import include, path
from rest_framework.routers import DefaultRouter

from course_app import views as course_views

router = DefaultRouter()
router.register(
    r'course',
    course_views.CourseViewSet,
    basename='course'
)

urlpatterns = [
    path(r'', include(router.urls)),
]
