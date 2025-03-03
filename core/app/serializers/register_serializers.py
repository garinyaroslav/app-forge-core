from rest_framework import serializers
from ..models import Consumer


class ConsumerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Consumer
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = Consumer.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user
