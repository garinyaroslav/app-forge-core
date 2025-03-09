from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views.register_views import RegisterView
from .views.consumer_views import ConsumerView
from .views.genre_views import GerneView
from .views.software_views import SoftwareView, get_products_list
from .views.review_views import ReviewView

urlpatterns = [
    # register routes
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),

    # consumer
    path('consumer/', ConsumerView.as_view(), name='consumer'),

    # genre
    path('genre/', GerneView.as_view(), name='genre'),

    # software
    path('software/', SoftwareView.as_view(), name='software'),
    path('software/list/', get_products_list, name='products_list'),

    # review
    path('review/', ReviewView.as_view(), name='review'),
]
