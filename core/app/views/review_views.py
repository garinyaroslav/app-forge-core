from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from ..serializers.review_serializers import ReviewSerializer
from ..models import Review


class ReviewView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        review_id = request.query_params.get('id')
        search_query = request.query_params.get('search')

        if review_id:
            try:
                review = Review.objects.get(id=review_id)
                serializer = ReviewSerializer(review)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Review.DoesNotExist:
                return Response(
                    {"error": "Review not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        elif search_query:
            reviews = Review.objects.filter(
                models.Q(text_comment__icontains=search_query)
            )
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            reviews = Review.objects.all()
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        review_id = request.query_params.get('id')

        if review_id:
            try:
                review = Review.objects.get(id=review_id)
                review.delete()
                return Response(
                    {"message": "Review deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT
                )
            except Review.DoesNotExist:
                return Response(
                    {"error": "Review not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"error": "Review ID is required"},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        review_id = request.query_params.get('id')

        if not review_id:
            return Response(
                {"error": "Review ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return Response(
                {"error": "Review not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ReviewSerializer(
            review, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
