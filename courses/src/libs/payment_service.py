from payments_app.models import Customer
from libs.exceptions import CustomerNotCreatedException
from libs.stripe_payment_service import StripePaymentService


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
