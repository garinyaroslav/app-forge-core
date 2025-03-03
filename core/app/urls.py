from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views.register_views import RegisterView
from .views.consumer_views import ConsumerView


urlpatterns = [
    # register routes
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),

    # consumer
    path('consumer/', ConsumerView.as_view(), name='consumer'),
]
