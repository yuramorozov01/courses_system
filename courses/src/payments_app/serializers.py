from base_app.serializers import CustomUserSerializer
from payments_app.models import Card
from rest_framework import serializers


class CardShortDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for cards
    This serializer provides short information about card.
    """

    user = CustomUserSerializer(read_only=True)
    funding = serializers.CharField(source='get_funding_display')

    class Meta:
        model = Card
        exclude = ['country', 'fingerprint', 'created', 'customer']
        read_only_fields = ['user', 'pm_id', 'name', 'brand', 'exp_month', 'exp_year', 'funding', 'last4']
