from rest_framework import generics, status
from rest_framework.response import Response
from ..serializers.register_serializers import ConsumerSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models import Cart


class RegisterView(generics.CreateAPIView):
    serializer_class = ConsumerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        Cart.objects.create(consumer=user)

        refresh = TokenObtainPairSerializer.get_token(user)
        access_token = refresh.access_token

        return Response({
            'userId': user.id,
            'username': user.username,
            'refresh': str(refresh),
            'access': str(access_token),
        }, status=status.HTTP_201_CREATED)
