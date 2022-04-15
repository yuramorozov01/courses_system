from course_app.models import Course
from libs.payments import PaymentService
from payments_app.models import Card
from payments_app.serializers import CardShortDetailsSerializer
from payments_app.validators import validate_buy_course_data, validate_refund_course_data
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class PaymentViewSet(viewsets.ViewSet):
    """
    client_secret:
        Retrieve client secret key

    buy_course:
        Buy course.
        Request has to contain the following POST params:
        `pm_id` - payment method ID
        `course_id` - course ID

    refund:
        Refund money for course.
        Request has to contain the following POST params:
        `course_id` - course ID
    """

    def get_permissions(self):
        base_permissions = [permissions.IsAuthenticated]
        permissions_dict = {
            'client_secret': [],
            'buy_course': [],
            'refund': [],
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]

    @action(methods=['GET'], detail=False)
    def client_secret(self, request):
        payment_service = PaymentService(self.request.user)
        response = {
            'client_secret': payment_service.get_setup_intent_client_secret_key(),
        }
        return Response(response)

    @action(methods=['POST'], detail=False)
    def buy_course(self, request):
        course_id, pm_id = validate_buy_course_data(
            self.request.user,
            self.request.POST.get('course_id'),
            self.request.POST.get('pm_id')
        )
        payment_service = PaymentService(self.request.user)
        payment = payment_service.buy_course(
            Course.objects.get(id=course_id),
            Card.objects.get(pm_id=pm_id)
        )
        response = {
            'status': payment.get_status_display(),
            'amount': payment.amount,
            'currency': payment.currency,
        }
        return Response(response, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def refund(self, request):
        course_id = validate_refund_course_data(
            self.request.user,
            self.request.POST.get('course_id')
        )
        payment_service = PaymentService(self.request.user)
        amount, refund_status, failure_reason = payment_service.refund_money(Course.objects.get(id=course_id))
        response = {
            'amount': amount,
            'status': refund_status,
            'failure_reason': failure_reason,
        }
        return Response(response, status=status.HTTP_200_OK)


class CardViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    list:
        Get all user's saved cards

    save_card:
        Save card for future payments
        Retrieves payment method ID as parameter `pm_id`
    """

    def get_queryset(self):
        querysets_dict = {
            'list': Card.objects.filter(user=self.request.user),
            'save_card': Card.objects.filter(user=self.request.user),
        }
        queryset = querysets_dict.get(self.action)
        return queryset.distinct()

    def get_serializer_class(self):
        serializers_dict = {
            'list': CardShortDetailsSerializer,
            'save_card': CardShortDetailsSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def get_permissions(self):
        base_permissions = [permissions.IsAuthenticated]
        permissions_dict = {
            'list': [],
            'save_card': [],
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]

    @action(methods=['POST'], detail=False)
    def save_card(self, request):
        payment_service = PaymentService(self.request.user)
        pm_id = self.request.POST.get('pm_id', '')
        card = payment_service.save_card_into_db(pm_id=pm_id)
        serializer = self.get_serializer()
        return Response(serializer.to_representation(card), status=status.HTTP_201_CREATED)
