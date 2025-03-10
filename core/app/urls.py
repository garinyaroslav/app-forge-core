from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views.register_views import RegisterView
from .views.consumer_views import ConsumerView
from .views.genre_views import GerneView
from .views.software_views import SoftwareView, get_products_list
from .views.review_views import ReviewView
from .views.library_views import LibraryView
from .views.cart_views import CartView
from .views.cart_item_views import CartItemView

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

    # library
    path('library/', LibraryView.as_view(), name='library'),

    # cart
    path('cart/', CartView.as_view(), name='cart'),

    # cart_item
    path('cart_item/', CartItemView.as_view(), name='cart_item'),
]
