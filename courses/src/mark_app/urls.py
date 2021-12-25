from django.urls import include, path
from mark_app import views as mark_views
from rest_framework_nested.routers import NestedSimpleRouter
from task_app.urls import task_router

mark_router = NestedSimpleRouter(task_router, r'task', lookup='task')
mark_router.register(
    r'mark',
    mark_views.MarkViewSet,
    basename='mark'
)

message_router = NestedSimpleRouter(mark_router, r'mark', lookup='mark')
message_router.register(
    r'message',
    mark_views.MessageViewSet,
    basename='task_statement_file'
)

urlpatterns = [
    path(r'', include(mark_router.urls)),
    path(r'', include(message_router.urls)),
]
