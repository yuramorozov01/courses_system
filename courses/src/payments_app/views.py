from payments_app.models import Customer
from libs import PaymentService
from rest_framework import permissions, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response


class PaymentsViewSet(viewsets.ViewSet):
    '''
    client_secret:
        Retrieve client secret key
    '''

    # def get_queryset(self):
    #     querysets_dict = {
    #         'client_secret': Customer.objects.filter(user=self.request.user.id),
    #     }
    #     queryset = querysets_dict.get(self.action)
    #     return queryset.distinct()

    # def get_serializer_class(self):
    #     serializers_dict = {
    #         'client_secret': '',
    #     }
    #     serializer_class = serializers_dict.get(self.action)
    #     return serializer_class

    def get_permissions(self):
        base_permissions = [permissions.IsAuthenticated]
        permissions_dict = {
            'client_secret': [],
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]

    @action(methods=['GET'], detail=False)
    def client_secret(self, request):
        payment_service = PaymentService(self.request.user)
        response = {
            'client_secret': payment_service.get_client_secret_key(),
        }
        return Response(response)
