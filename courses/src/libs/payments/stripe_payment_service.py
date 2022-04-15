import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from libs.payments.exceptions import CustomerNotCreatedException
from stripe.error import CardError, InvalidRequestError

User = get_user_model()


class StripePaymentService:
    def __init__(self, user: User):
        stripe.api_key = settings.STRIPE_API_SECRET_KEY
        self._user = user

    def get_customer(self) -> stripe.Customer:
        if not hasattr(self._user, 'customer'):
            raise CustomerNotCreatedException
        customer = self._retrieve_customer_by_stripe_id(self._user.customer.stripe_id)
        return customer

    def create_customer(self) -> stripe.Customer:
        customer = stripe.Customer.create(name=f'{self._user.id}_{self._user.username}')
        return customer

    def _retrieve_customer_by_stripe_id(self, stripe_id: str) -> stripe.Customer:
        customer = stripe.Customer.retrieve(stripe_id)
        return customer

    def create_setup_intent(self, customer_id: str, payment_method_types: list = None) -> stripe.SetupIntent:
        methods = payment_method_types or ['card']
        intent = stripe.SetupIntent.create(
            customer=customer_id,
            payment_method_types=methods,
        )
        return intent

    def retrieve_payment_method(self, pm_id: str) -> stripe.PaymentMethod:
        try:
            payment_method = stripe.PaymentMethod.retrieve(pm_id)
        except InvalidRequestError:
            payment_method = None
        return payment_method

    def create_payment_intent(self, amount: int, currency: str, customer_id: str,
                              pm_id: str, capture_method: str = 'automatic') -> stripe.PaymentIntent:
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency or 'eur',
                customer=customer_id,
                payment_method=pm_id,
                off_session=True,
                confirm=True,
                capture_method=capture_method
            )
        except CardError as e:
            err = e.error
            payment_intent_id = err.payment_intent['id']
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return payment_intent

    def capture_money(self, pi_id: str, amount_to_capture: int = None) -> stripe.PaymentIntent:
        payment_intent = stripe.PaymentIntent.capture(
            pi_id,
            amount_to_capture=amount_to_capture
        )
        return payment_intent
