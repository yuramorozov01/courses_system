from course_app import views as course_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r'course',
    course_views.CourseViewSet,
    basename='course'
)

urlpatterns = [
    path(r'', include(router.urls)),
]
