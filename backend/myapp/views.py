# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import ListingCreateSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Listing
from .serializers import *

class ListingCreateView(APIView):
    def post(self, request):
        serializer = ListingCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# views.py

class ListingGetView(APIView):
    def get(self, request, pk):
        try:
            listing = Listing.objects.get(pk=pk)  # Fetch listing by primary key (ID)
            serializer = ListingCreateSerializer(listing)  # Use your existing serializer
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Listing.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
class UserFavoritesView(APIView):
    def get(self, request):
        user_id =request.data.get('user_id')

        if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the user's favorite listings
        favorites = Favorite.objects.filter(user__id=user_id)

        # Serialize the favorite listings
        serializer = FavoriteSerializer(favorites, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Listing  # Import your Listing model
from .serializers import ListingSerializer  # Import your ListingSerializer


class ListingUpdateAPIView(APIView):
    def patch(self, request, *args, **kwargs):
        # Retrieve user_id and listing_id from request.data
        user_id = request.data.get('user_id')
        listing_id = request.data.get('listing_id')
        amenities_ids = request.data.get('amenities', [])

        try:
            # Ensure the listing exists and belongs to the user
            listing = Listing.objects.get(id=listing_id, host=user_id)

            # Update the listing with the new data
            serializer = ListingSerializer(listing, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Handle amenities - Clear existing and add new ones
            if amenities_ids:
                # Clear existing amenities for the listing
                ListingAmenity.objects.filter(listing=listing).delete()

                # Add new amenities
                for amenity_id in amenities_ids:
                    amenity = Amenity.objects.get(id=amenity_id)
                    ListingAmenity.objects.create(listing=listing, amenity=amenity)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Listing.DoesNotExist:
            return Response({"error": "Listing not found."}, status=status.HTTP_404_NOT_FOUND)
        except Amenity.DoesNotExist:
            return Response({"error": "One or more amenities not found."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import generics
from .models import Listing
from .serializers import ListingDetailSerializer
class ListingDetailView(generics.RetrieveAPIView):
    queryset = Listing.objects.all()  # Retrieve all listings
    serializer_class = ListingDetailSerializer  # Use the detailed serializer for response
    lookup_field = 'id'  # Look up by ID

class Listing3UpdateAPIView(APIView):
    def patch(self, request, *args, **kwargs):
        # Retrieve user_id and listing_id from request.data
        user_id = request.data.get('user_id')
        listing_id = request.data.get('listing_id')
        security_ids = request.data.get('security_id', [])

        # Retrieve the listing if it exists
        try:
            # Ensure the listing belongs to the user
            listing = Listing.objects.get(id=listing_id, host=user_id)

            # Update the listing with the new data
            serializer = ListingStep3erializer(listing, data=request.data, partial=True)  # Use partial=True to allow partial updates
            serializer.is_valid(raise_exception=True)
            serializer.save()

            if security_ids:
                # Clear existing security for the listing
                ListingSecurity.objects.filter(listing=listing).delete()

                # Add new securities
                for security_id in security_ids:
                    security = SecurityType.objects.get(id=security_id)
                    ListingSecurity.objects.create(listing=listing, security=security)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Listing.DoesNotExist:
            return Response({"error": "Listing not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
class FavoriteListingView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')  # Get user_id from the request data
        listing_id = request.data.get('listing_id')

        # Ensure that the user_id and listing_id are provided
        if user_id is None or listing_id is None:
            return Response({"error": "User ID and Listing ID are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            listing = Listing.objects.get(id=listing_id)
        except Listing.DoesNotExist:
            return Response({"error": "Listing not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has already favorited the listing
        if Favorite.objects.filter(user_id=user_id, listing=listing).exists():
            return Response({"message": "Listing is already favorited"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new favorite
        favorite = Favorite.objects.create(user_id=user_id, listing=listing)  # Use the provided user_id
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)