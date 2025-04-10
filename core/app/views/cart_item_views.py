from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..serializers.cart_item_serializers import CartItemSerializer
from ..models import CartItem, Cart
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Subquery


class CartItemView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        cart_item_id = request.query_params.get('id')
        search_query = request.query_params.get('search')

        if cart_item_id:
            try:
                cart_item = CartItem.objects.get(id=cart_item_id)
                serializer = CartItemSerializer(cart_item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except CartItem.DoesNotExist:
                return Response(
                    {"error": "CartItem not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        elif search_query:
            try:
                searched_id = int(search_query)
                libraries = CartItem.objects.filter(cart_id=searched_id)
                serializer = CartItemSerializer(libraries, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response(
                    {"error": "Invalid searched_id"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            libraries = CartItem.objects.all()
            serializer = CartItemSerializer(libraries, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        cart_item_id = request.query_params.get('id')

        if cart_item_id:
            try:
                cart_item = CartItem.objects.get(id=cart_item_id)
                cart_item.delete()
                return Response(
                    {"message": "CartItem deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT
                )
            except CartItem.DoesNotExist:
                return Response(
                    {"error": "CartItem not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"error": "CartItem ID is required"},
                status=status.HTTP_404_NOT_FOUND
            )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_my_cart_item(request):
    user_id = request.user.id
    cart_item_id = request.query_params.get('id')

    if cart_item_id:
        try:
            # DELETE FROM app_cartitem WHERE cart_id = (SELECT id FROM app_cart WHERE consumer_id = $1) AND id = $2;
            cart_subquery = Cart.objects.filter(
                consumer_id=user_id).values('id')

            deleted_count, _ = CartItem.objects.filter(
                cart_id__in=Subquery(cart_subquery),
                id=cart_item_id
            ).delete()

            return Response(
                {"message": f"Deleted {deleted_count} cart items"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        return Response(
            {"error": "CartItem ID is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
