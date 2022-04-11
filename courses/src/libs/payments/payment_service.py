import arrow
from payments_app.models import Card, Customer
from libs.payments.exceptions import CustomerNotCreatedException
from libs.payments.stripe_payment_service import StripePaymentService
from rest_framework.validators import ValidationError


class PaymentService:
    def __init__(self, user):
        self._user = user
        self._payment_service = StripePaymentService(user=user)

    def get_client_secret_key(self):
        try:
            customer = self._payment_service.get_customer()
        except CustomerNotCreatedException:
            customer = self._payment_service.create_customer()
            Customer.objects.create(user=self._user, stripe_id=customer.stripe_id)
        intent = self._payment_service.create_intent(customer.stripe_id, payment_method_types=['card'])
        return intent.client_secret

    def save_card_into_db(self, pm_id=''):
        payment_method = self._payment_service.retrieve_payment_method(pm_id)
        if payment_method is None:
            raise ValidationError({'pm_id': 'Unknown payment method id'})
        customer = Customer.objects.get(stripe_id=payment_method.customer)
        Card.objects.get_or_create(
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
