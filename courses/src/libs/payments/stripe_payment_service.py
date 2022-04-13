import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from libs.payments.exceptions import CustomerNotCreatedException
from stripe.error import InvalidRequestError

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
