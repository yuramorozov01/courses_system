from django.urls import include, path
from rest_framework_nested.routers import NestedSimpleRouter

from course_app.urls import router as course_router
from lecture_app import views as lecture_views

lecture_router = NestedSimpleRouter(course_router, r'course', lookup='course')
lecture_router.register(
    r'lecture',
    lecture_views.LectureViewSet,
    basename='lecture'
)

lecture_file_router = NestedSimpleRouter(lecture_router, r'lecture', lookup='lecture')
lecture_file_router.register(
    r'lecture_file',
    lecture_views.LectureFileViewSet,
    basename='lecture_file'
)

urlpatterns = [
    path(r'', include(lecture_router.urls)),
    path(r'', include(lecture_file_router.urls)),
]
