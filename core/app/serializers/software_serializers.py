from rest_framework import serializers
from ..models import SoftwareProduct


class SoftwareSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )
    rating = serializers.DecimalField(
        max_digits=3,
        decimal_places=2,
        coerce_to_string=False
    )

    class Meta:
        model = SoftwareProduct
        fields = "__all__"
