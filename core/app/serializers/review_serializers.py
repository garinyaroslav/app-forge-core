from rest_framework import serializers
from ..models import Review


class ReviewSerializer(serializers.ModelSerializer):
    rating = serializers.DecimalField(
        max_digits=3,
        decimal_places=2,
        coerce_to_string=False
    )

    class Meta:
        model = Review
        fields = "__all__"
