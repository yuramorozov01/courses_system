from django.urls import include, path
from lecture_app import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'lecture', views.LectureViewSet, basename='Lecture')
router.register(r'lecturefile', views.LectureFileViewSet, basename='Lecture file')

urlpatterns = [
    path('', include(router.urls)),
]
