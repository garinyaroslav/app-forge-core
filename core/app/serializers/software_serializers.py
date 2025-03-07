

from rest_framework import serializers
from ..models import SoftwareProduct


class SoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareProduct
        fields = "__all__"
