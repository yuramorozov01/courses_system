from django.urls import include, path
from payments_app import views as payments_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r'payment',
    payments_views.PaymentViewSet,
    basename='payment'
)
router.register(
    r'card',
    payments_views.CardViewSet,
    basename='card'
)

urlpatterns = [
    path(r'', include(router.urls)),
]
