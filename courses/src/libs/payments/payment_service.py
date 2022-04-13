import arrow
from course_app.models import Course
from django.contrib.auth import get_user_model
from libs.payments.exceptions import CustomerNotCreatedException
from libs.payments.stripe_payment_service import StripePaymentService
from payments_app.choices import PaymentStatusChoices
from payments_app.models import Card, Customer, Payment
from rest_framework.validators import ValidationError

User = get_user_model()


class PaymentService:
    def __init__(self, user: User) -> None:
        self._user = user
        self._payment_service = StripePaymentService(user=user)

    def get_setup_intent_client_secret_key(self) -> str:
        try:
            customer = self._payment_service.get_customer()
        except CustomerNotCreatedException:
            customer = self._payment_service.create_customer()
            Customer.objects.create(user=self._user, stripe_id=customer.stripe_id)
        intent = self._payment_service.create_setup_intent(customer.stripe_id, payment_method_types=['card'])
        return intent.client_secret

    def save_card_into_db(self, pm_id: str = '') -> Card:
        payment_method = self._payment_service.retrieve_payment_method(pm_id)
        if payment_method is None:
            raise ValidationError({'pm_id': 'Unknown payment method id'})
        customer = Customer.objects.get(stripe_id=payment_method.customer)
        card, _ = Card.objects.get_or_create(
            user=self._user,
            pm_id=payment_method.id,
            name=payment_method.billing_details.name,
            brand=payment_method.card.brand,
            country=payment_method.card.country,
            exp_month=payment_method.card.exp_month,
            exp_year=payment_method.card.exp_year,
            fingerprint=payment_method.card.fingerprint,
            funding=payment_method.card.funding,
            last4=payment_method.card.last4,
            created=arrow.get(payment_method.created).datetime,
            customer=customer
        )
        return card

    def buy_course(self, course_id: int, pm_id: str) -> Payment:
        currency = 'eur'
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise ValidationError({'course_id': 'Unknown course ID'})

        if Payment.objects.filter(course=course, user=self._user, status=PaymentStatusChoices.SUCCEEDED).exists():
            raise ValidationError({'course_id': 'You have already purchased this course!'})

        process_statuses = [
            PaymentStatusChoices.REQUIRES_CONFIRMATION,
            PaymentStatusChoices.REQUIRES_ACTION,
            PaymentStatusChoices.PROCESSING,
            PaymentStatusChoices.REQUIRES_CAPTURE,
        ]
        if Payment.objects.filter(course=course, user=self._user, status__in=process_statuses).exists():
            raise ValidationError({
                'course_id': 'You cannot purchase this course until previous operation is completed'
            })

        try:
            card = Card.objects.get(pm_id=pm_id)
        except Card.DoesNotExist:
            raise ValidationError({'pm_id': 'Unknown payment method ID'})

        payment_intent = self._payment_service.create_payment_intent(
            course.price,
            currency,
            card.customer.stripe_id,
            pm_id
        )

        payment = Payment.objects.create(
            user=self._user,
            course=course,
            payment_intent_id=payment_intent.id,
            payment_method_id=payment_intent.payment_method,
            amount=payment_intent.amount,
            currency=payment_intent.currency,
            customer=card.customer,
            status=payment_intent.status,
            created=arrow.get(payment_intent.created).datetime
        )
        return payment
