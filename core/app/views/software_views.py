from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from ..serializers.software_serializers import SoftwareSerializer
from ..models import SoftwareProduct


class GerneView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        products = SoftwareProduct.objects.all()
        serializer = SoftwareProduct(products, many=True)
        return Response(serializer.data)
        # genre_id = request.query_params.get('id')
        # search_query = request.query_params.get('search')
        #
        # if genre_id:
        #     try:
        #         genre = Genre.objects.get(id=genre_id)
        #         serializer = GenreSerializer(genre)
        #         return Response(serializer.data, status=status.HTTP_200_OK)
        #     except Genre.DoesNotExist:
        #         return Response(
        #             {"error": "Genre not found"},
        #             status=status.HTTP_404_NOT_FOUND
        #         )
        # elif search_query:
        #     genres = Genre.objects.filter(
        #         models.Q(name__icontains=search_query)
        #     )
        #     serializer = GenreSerializer(genres, many=True)
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # else:
        #     genres = Genre.objects.all()
        #     serializer = GenreSerializer(genres, many=True)
        #     return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = SoftwareSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, *args, **kwargs):
    #     genre_id = request.query_params.get('id')
    #
    #     if genre_id:
    #         try:
    #             genre = Genre.objects.get(id=genre_id)
    #             genre .delete()
    #             return Response(
    #                 {"message": "Genre deleted successfully"},
    #                 status=status.HTTP_204_NO_CONTENT
    #             )
    #         except Genre.DoesNotExist:
    #             return Response(
    #                 {"error": "Genre not found"},
    #                 status=status.HTTP_404_NOT_FOUND
    #             )
    #     else:
    #         return Response(
    #             {"error": "Genre ID is required"},
    #             status=status.HTTP_404_NOT_FOUND
    #         )
    #
    # def put(self, request, *args, **kwargs):
    #     genre_id = request.query_params.get('id')
    #
    #     if not genre_id:
    #         return Response(
    #             {"error": "Genre ID is required"},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #
    #     try:
    #         genre = Genre.objects.get(id=genre_id)
    #     except Genre.DoesNotExist:
    #         return Response(
    #             {"error": "Genre not found"},
    #             status=status.HTTP_404_NOT_FOUND
    #         )
    #
    #     serializer = GenreSerializer(
    #         genre, data=request.data, partial=True)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
