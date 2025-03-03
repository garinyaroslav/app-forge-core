
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


class ConsumerView(APIView):
    permission_classes = [IsAdminUser]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        content = {
            'message': 'Это защищенный эндпоинт!',
            'user': str(request.user),
        }
        return Response(content)

    # def get(self, request):
    #     content = {
    #         'message': 'Это защищенный эндпоинт!',
    #         'user': str(request.user),
    #     }
    #     return Response(content)
