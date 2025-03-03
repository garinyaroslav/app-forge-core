# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics, status
from rest_framework.response import Response
from ..serializers.register_serializers import ConsumerSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = ConsumerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = TokenObtainPairSerializer.get_token(user)
        access_token = refresh.access_token

        return Response({
            'user': ConsumerSerializer(user).data,
            'refresh': str(refresh),
            'access': str(access_token),
        }, status=status.HTTP_201_CREATED)


# class ProtectedView(APIView):
#     permission_classes = [IsAdminUser]
#     # permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         content = {
#             'message': 'Это защищенный эндпоинт!',
#             'user': str(request.user),
#         }
#         return Response(content)
