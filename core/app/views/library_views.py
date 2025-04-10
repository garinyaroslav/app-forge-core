
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..serializers.library_serializers import LibrarySerializer
from rest_framework.decorators import api_view, permission_classes
from ..models import Library, SoftwareProduct
from django.utils import timezone


class LibraryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        library_id = request.query_params.get('id')
        search_query = request.query_params.get('search')

        if library_id:
            try:
                library = Library.objects.get(id=library_id)
                serializer = LibrarySerializer(library)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Library.DoesNotExist:
                return Response(
                    {"error": "Library not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        elif search_query:
            try:
                searched_id = int(search_query)
                libraries = Library.objects.filter(product_id=searched_id)
                serializer = LibrarySerializer(libraries, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response(
                    {"error": "Invalid consumer_id"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            libraries = Library.objects.all()
            serializer = LibrarySerializer(libraries, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LibrarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        library_id = request.query_params.get('id')

        if library_id:
            try:
                library = Library.objects.get(id=library_id)
                library.delete()
                return Response(
                    {"message": "Library deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT
                )
            except Library.DoesNotExist:
                return Response(
                    {"error": "Library not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"error": "Library ID is required"},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        library_id = request.query_params.get('id')

        if not library_id:
            return Response(
                {"error": "Library ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            library = Library.objects.get(id=library_id)
        except Library.DoesNotExist:
            return Response(
                {"error": "Library not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LibrarySerializer(
            library, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_my_library(request):
    user = request.user
    product_id = request.data.get('product_id')

    if not product_id:
        return Response(
            {"error": "product_id is required in the request body"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        product = SoftwareProduct.objects.get(id=product_id)
    except SoftwareProduct.DoesNotExist:
        return Response(
            {"error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if Library.objects.filter(consumer=user, product=product).exists():
        return Response(
            {"error": "This product is already in your library"},
            status=status.HTTP_400_BAD_REQUEST
        )

    library_item = Library.objects.create(
        consumer=user,
        product=product,
        added_date=timezone.now()
    )

    serializer = LibrarySerializer(library_item)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
