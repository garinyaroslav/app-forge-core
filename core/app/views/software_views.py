import base64
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from ..serializers.software_serializers import SoftwareSerializer
from ..models import SoftwareProduct, Cart, CartItem, Library
from rest_framework.decorators import api_view, permission_classes
from django.db.models import F, OuterRef, Subquery


class SoftwareView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        software_id = request.query_params.get('id')
        search_query = request.query_params.get('search')

        if software_id:
            try:
                product = SoftwareProduct.objects.get(id=software_id)
                serializer = SoftwareSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except SoftwareProduct.DoesNotExist:
                return Response(
                    {"error": "SoftwareProduct not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        elif search_query:
            products = SoftwareProduct.objects.filter(
                models.Q(title__icontains=search_query) |
                models.Q(description__icontains=search_query)
            )
            serializer = SoftwareSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            products = SoftwareProduct.objects.all()
            serializer = SoftwareSerializer(products, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        if 'image' in request.FILES:
            try:
                image_file = request.FILES['image']
                image_data = image_file.read()
                request.data['image'] = base64.b64encode(
                    image_data).decode('utf-8')
            except Exception as e:
                return Response(
                    {"detail": f"Error processing image file: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = SoftwareSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        product_id = request.query_params.get('id')

        if product_id:
            try:
                product = SoftwareProduct.objects.get(id=product_id)
                product.delete()
                return Response(
                    {"message": "SoftwareProduct deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT
                )
            except SoftwareProduct.DoesNotExist:
                return Response(
                    {"error": "SoftwareProduct not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"error": "SoftwareProduct ID is required"},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        product_id = request.query_params.get('id')

        if not product_id:
            return Response(
                {"error": "SoftwareProduct ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = SoftwareProduct.objects.get(id=product_id)
        except SoftwareProduct.DoesNotExist:
            return Response(
                {"error": "SoftwareProduct not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if 'image' in request.FILES:
            try:
                image_file = request.FILES['image']
                image_data = image_file.read()
                request.data['image'] = base64.b64encode(
                    image_data).decode('utf-8')
            except Exception as e:
                return Response(
                    {"detail": f"Error processing image file: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = SoftwareSerializer(
            product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_products_list(request):
    product_id = request.query_params.get('id')

    if product_id:
        try:
            # SELECT product.*, genre.name FROM app_softwareproduct AS product JOIN app_genre AS genre ON genre.id = product.genre_id where product.id = 9;
            product = SoftwareProduct.objects.select_related(
                'genre').get(id=product_id)

            result = {
                'id': product.id,
                'title': product.title,
                'description': product.description,
                'developer_name': product.developer_name,
                'rel_date': product.rel_date,
                'image': product.image,
                'price': product.price,
                'copies_sold': product.copies_sold,
                'rating': product.rating,
                'genre_id': product.genre_id,
                'genre_name': product.genre.name,
            }

            return Response(result, status=status.HTTP_200_OK)

        except SoftwareProduct.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )
    else:
        try:
            # SELECT product.*, genre.name FROM app_softwareproduct AS product JOIN app_genre AS genre ON genre.id = product.genre_id;
            products = SoftwareProduct.objects.annotate(
                genre_name=F('genre__name')
            ).values(
                'id', 'title', 'description', 'developer_name', 'rel_date',
                'image', 'price', 'copies_sold', 'rating', 'genre_id', 'genre_name'
            )

            result = list(products)

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_cart_products_by_user_id(request):
    user_id = request.query_params.get('id')

    try:
        # SELECT product.*, app_cartitem.id AS cart_item_id FROM app_softwareproduct AS product JOIN app_cartitem ON product.id = app_cartitem.product_id WHERE app_cartitem.cart_id = (SELECT id FROM app_cart WHERE consumer_id=$1);

        cart_subquery = Cart.objects.filter(consumer_id=user_id).values('id')

        products_with_cart_items = SoftwareProduct.objects.filter(
            cartitem__cart_id__in=Subquery(cart_subquery)
        ).annotate(
            cart_item_id=Subquery(
                CartItem.objects.filter(
                    product_id=OuterRef('id'),
                    cart_id__in=Subquery(cart_subquery)
                ).values('id')[:1]
            )
        ).values(
            'id', 'title', 'description', 'developer_name', 'rel_date', 'image', 'copies_sold', 'rating', 'cart_item_id'
        )

        return Response(products_with_cart_items, status=status.HTTP_200_OK)

    except SoftwareProduct.DoesNotExist:
        return Response(
            {"error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_cart_items_by_user_id(request):
    user_id = request.query_params.get('id')

    try:
        # DELETE FROM app_cartitem WHERE cart_id = (SELECT id FROM app_cart WHERE consumer_id = $1);
        cart_subquery = Cart.objects.filter(consumer_id=user_id).values('id')

        deleted_count, _ = CartItem.objects.filter(
            cart_id__in=Subquery(cart_subquery)).delete()

        return Response(
            {"message": f"Deleted {deleted_count} cart items"},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_library_item(request):
    consumer_id = request.query_params.get('consumer_id')
    product_id = request.query_params.get('product_id')

    if not consumer_id or not product_id:
        return Response(
            {"error": "Both consumer_id and product_id are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        library_items = Library.objects.filter(
            consumer_id=consumer_id, product_id=product_id)

        results = [
            {
                "id": item.id,
                "consumer_id": item.consumer_id,
                "product_id": item.product_id,
                "added_date": item.added_date,
            }
            for item in library_items
        ]

        return Response(results, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
