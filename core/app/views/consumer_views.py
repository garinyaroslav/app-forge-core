from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.db import models
from ..serializers.consumer_serializers import ConsumerSerializer
from ..models import Consumer


class ConsumerView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        consumer_id = request.query_params.get('id')
        search_query = request.query_params.get('search')

        if consumer_id:
            try:
                consumer = Consumer.objects.get(id=consumer_id)
                serializer = ConsumerSerializer(consumer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Consumer.DoesNotExist:
                return Response(
                    {"error": "Consumer not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        elif search_query:
            consumers = Consumer.objects.filter(
                models.Q(username__icontains=search_query) |
                models.Q(email__icontains=search_query)
            )
            serializer = ConsumerSerializer(consumers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            consumers = Consumer.objects.all()
            serializer = ConsumerSerializer(consumers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        request.data['password'] = make_password(request.data.get('password'))

        serializer = ConsumerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        consumer_id = request.query_params.get('id')

        if consumer_id:
            try:
                consumer = Consumer.objects.get(id=consumer_id)
                consumer.delete()
                return Response(
                    {"message": "Consumer deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT
                )
            except Consumer.DoesNotExist:
                return Response(
                    {"error": "Consumer not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"error": "Consumer ID is required"},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        consumer_id = request.query_params.get('id')

        if not consumer_id:
            return Response(
                {"error": "Consumer ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            consumer = Consumer.objects.get(id=consumer_id)
        except Consumer.DoesNotExist:
            return Response(
                {"error": "Consumer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if 'password' in request.data:
            request.data['password'] = make_password(request.data['password'])

        serializer = ConsumerSerializer(
            consumer, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
