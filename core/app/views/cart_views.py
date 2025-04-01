from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from ..serializers.cart_serializers import CartSerializer
from ..models import Cart


class CartView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        cart_id = request.query_params.get('id')
        search_query = request.query_params.get('search')
        print(search_query)

        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id)
                serializer = CartSerializer(cart)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Cart.DoesNotExist:
                return Response(
                    {"error": "Cart not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        elif search_query:
            try:
                searched_id = int(search_query)
                cart_items = Cart.objects.filter(consumer=searched_id)
                serializer = CartSerializer(cart_items, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response(
                    {"error": "Invalid searched_id"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            cart_items = Cart.objects.all()
            serializer = CartSerializer(cart_items, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        cart_id = request.query_params.get('id')

        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id)
                cart.delete()
                return Response(
                    {"message": "Cart deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT
                )
            except Cart.DoesNotExist:
                return Response(
                    {"error": "Cart not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"error": "Cart ID is required"},
                status=status.HTTP_404_NOT_FOUND
            )
