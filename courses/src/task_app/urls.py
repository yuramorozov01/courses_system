from lecture_app.urls import lecture_router
from task_app import views as task_views
from django.urls import include, path
from rest_framework_nested.routers import NestedSimpleRouter


task_statement_router = NestedSimpleRouter(lecture_router, r'lecture', lookup='lecture')
task_statement_router.register(
    r'task_statement',
    task_views.TaskStatementViewSet,
    basename='task_statement'
)

task_statement_file_router = NestedSimpleRouter(task_statement_router, r'task_statement', lookup='task_statement')
task_statement_file_router.register(
    r'task_statement_file',
    task_views.TaskStatementFileViewSet,
    basename='task_statement_file'
)

task_router = NestedSimpleRouter(task_statement_router, r'task_statement', lookup='task_statement')
task_router.register(
    r'task',
    task_views.TaskViewSet,
    basename='task'
)

task_file_router = NestedSimpleRouter(task_router, r'task', lookup='task')
task_file_router.register(
    r'task_file',
    task_views.TaskFileViewSet,
    basename='task_file'
)

urlpatterns = [
    path(r'', include(task_statement_router.urls)),
    path(r'', include(task_statement_file_router.urls)),
    path(r'', include(task_router.urls)),
    path(r'', include(task_file_router.urls)),
]
