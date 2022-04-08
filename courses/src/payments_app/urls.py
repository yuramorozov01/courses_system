from payments_app import views as payments_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r'payments',
    payments_views.PaymentsViewSet,
    basename='payments'
)

urlpatterns = [
    path(r'', include(router.urls)),
]
