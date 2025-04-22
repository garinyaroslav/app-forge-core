from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views.register_views import RegisterView
from .views.consumer_views import ConsumerView
from .views.genre_views import GerneView
from .views.software_views import SoftwareView, genre_sales_stats, export_products_to_excel, buy, get_products_list, SoftwareReviewView, get_cart_products_by_user_id, get_library_item, get_library_items, ProductUserCart, get_rewiews_by_product_id
from .views.review_views import ReviewView
from .views.library_views import LibraryView
from .views.cart_views import CartView
from .views.profile_views import ProfileViews
from .views.cart_item_views import CartItemView, delete_my_cart_item
from .views.token_obtain_views import MyTokenObtainPairView

urlpatterns = [
    # register routes
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),

    # consumer
    path('consumer/', ConsumerView.as_view(), name='consumer'),

    # profile
    path('profile/', ProfileViews.as_view(), name='profile'),

    # genre
    path('genre/', GerneView.as_view(), name='genre'),

    # software
    path('software/', SoftwareView.as_view(), name='software'),
    path('software/list/', get_products_list, name='products_list'),
    path('software/cart/', get_cart_products_by_user_id, name='products_cart'),
    path('software/library_item/', get_library_item,
         name='get_library_item'),
    path('software/library_items/', get_library_items,
         name='get_library_items'),
    path('software/user/cart/', ProductUserCart.as_view(),
         name='user_cart'),
    path('software/reviews/', get_rewiews_by_product_id,
         name='get_reviews'),
    path('software/review/', SoftwareReviewView.as_view(),
         name='software_review'),
    path('software/buy/', buy, name='buy'),
    path('software/export/', export_products_to_excel, name="export_products"),
    path('software/top_genres/', genre_sales_stats, name="genre_sales_stats"),

    # review
    path('review/', ReviewView.as_view(), name='review'),

    # library
    path('library/', LibraryView.as_view(), name='library'),

    # cart
    path('cart/', CartView.as_view(), name='cart'),

    # cart_item
    path('cart_item/', CartItemView.as_view(), name='cart_item'),
    path('cart_item/my/', delete_my_cart_item, name='delete_my_cart_item'),
]
