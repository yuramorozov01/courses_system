from django.urls import include, path
from rest_framework.routers import DefaultRouter
from task_app import views

router = DefaultRouter()
router.register(r'taskstmt', views.TaskStatementViewSet, basename='Task statement')
router.register(r'taskstmtfile', views.TaskStatementFileViewSet, basename='Task statement file')
router.register(r'task', views.TaskViewSet, basename='Task')
router.register(r'taskfile', views.TaskFileViewSet, basename='Task file')

urlpatterns = [
    path('', include(router.urls)),
]
