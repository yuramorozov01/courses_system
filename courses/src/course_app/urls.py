from course_app import views as course_views
from lecture_app import views as lecture_views
from task_app import views as task_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter


# Base course API (under root)
router = DefaultRouter()
router.register(
    r'course',
    course_views.CourseViewSet,
    basename='course'
)


# Lecture API (under course)
lecture_router = NestedSimpleRouter(router, r'course', lookup='course')
lecture_router.register(
    r'lecture',
    lecture_views.LectureViewSet,
    basename='lecture'
)

# Lecture file API (under lecture)
lecture_file_router = NestedSimpleRouter(lecture_router, r'lecture', lookup='lecture')
lecture_file_router.register(
    r'lecture_file',
    lecture_views.LectureFileViewSet,
    basename='lecture_file'
)


# Task statement API (under lecture)
task_statement_router = NestedSimpleRouter(lecture_router, r'lecture', lookup='lecture')
task_statement_router.register(
    r'task_statement',
    task_views.TaskStatementViewSet,
    basename='task_statement'
)

# Task statement file API (under task_statement)
task_statement_file_router = NestedSimpleRouter(task_statement_router, r'task_statement', lookup='task_statement')
task_statement_file_router.register(
    r'task_statement_file',
    task_views.TaskStatementFileViewSet,
    basename='task_statement_file'
)


# Task API (under task_statement)
task_router = NestedSimpleRouter(task_statement_router, r'task_statement', lookup='task_statement')
task_router.register(
    r'task',
    task_views.TaskViewSet,
    basename='task'
)

# Task file API (under task)
task_file_router = NestedSimpleRouter(task_router, r'task', lookup='task')
task_file_router.register(
    r'task_file',
    task_views.TaskFileViewSet,
    basename='task_file'
)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(lecture_router.urls)),
    path(r'', include(task_statement_router.urls)),
    path(r'', include(task_statement_file_router.urls)),
    path(r'', include(task_router.urls)),
    path(r'', include(task_file_router.urls)),
]
