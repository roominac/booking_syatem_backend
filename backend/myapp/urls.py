# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('listings/create/', ListingCreateView.as_view(), name='listing-create'),
    # path('create-listing/', ListingCreateView.as_view(), name='create-listing'),
    path('listings/<int:pk>/', ListingGetView.as_view(), name='listing-detail'),  # For retrieving a listing by ID
    path('listings/step2/create/', ListingUpdateAPIView.as_view(), name='listing-create'),
    path('list/<int:id>/', ListingDetailView.as_view(), name='listing-detail'),  # URL to fetch listing by ID
    path('listings/step3/create/', Listing3UpdateAPIView.as_view(), name='listing-create'),

    path('listings/step1/save', ListingCreateView.as_view(), name='listing-create'),
    path('listings/step2/save/', ListingUpdateAPIView.as_view(), name='listing-create'),
    # path('listings/step3/save/', Listing3UpdateAPIView.as_view(), name='listing-create'),
    path('listings/favorite/', FavoriteListingView.as_view(), name='favorite-listing'),
    path('favorites/', UserFavoritesView.as_view(), name='user-favorites'),  # Endpoint for fetching user favorites

]
