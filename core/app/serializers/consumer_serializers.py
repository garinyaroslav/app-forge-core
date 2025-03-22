from rest_framework import serializers
from ..models import Consumer


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ['id',
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  'password',
                  'is_staff',
                  'date_joined',
                  ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
