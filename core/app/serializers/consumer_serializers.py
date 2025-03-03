from rest_framework import serializers
from ..models import Consumer


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ['id',
                  'email',
                  'first_name',
                  'last_name',
                  'password',
                  # 'last_login',
                  # 'is_superuser',
                  'is_staff',
                  # 'is_active',
                  'date_joined',
                  ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
