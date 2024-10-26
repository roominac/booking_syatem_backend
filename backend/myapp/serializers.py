# serializers.py
from rest_framework import serializers
from .models import *

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address', 'city', 'state']  # Include necessary fields for the address

class ListingCreateSerializer(serializers.ModelSerializer):
    address = serializers.CharField(write_only=True)  # Full address from frontend
    city = serializers.CharField(write_only=True)     # City from frontend
    state = serializers.CharField(write_only=True)    # State from frontend
    address_details = AddressSerializer(source='address_id', read_only=True)  # Address details in the response

    class Meta:
        model = Listing
        fields = [
            'host',
            'property_type',
            'room_type',
            'bedrooms',
            'beds',
            'bathrooms',
            'address',
            'city',
            'state',
            'accommodates',
            'address_details',  # Add address details to the response
        ]

    def create(self, validated_data):
        # Extract address, city, and state from the validated data
        address_input = validated_data.pop('address')
        city_input = validated_data.pop('city')
        state_input = validated_data.pop('state')

        # Check if address already exists
        address_obj, created = Address.objects.get_or_create(
            address=address_input,
            city=city_input,
            state=state_input
        )

        # Assign the address object to the listing and create the listing
        listing = Listing.objects.create(address_id=address_obj, **validated_data)
        return listing

    # Optionally override to_representation if you want to customize the output further
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # You can customize what else you want to include in the response
        return representation

















from rest_framework import serializers
from .models import Listing, Amenity, Image
from rest_framework import serializers
from .models import Listing, Amenity, Image

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'icon_url']

class ListingAmenitySerializer(serializers.ModelSerializer):
    amenity = AmenitySerializer()  # Include the related Amenity details

    class Meta:
        model = ListingAmenity
        fields = ['amenity', 'is_highlighted']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image_url', 'caption', 'is_primary']

class ListingSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=False)
    # security = SecurityTypeSerializer()  # Include the related Amenity details

    class Meta:
        model = Listing
        fields = ['id', 'title', 'description', 'images']

    def update(self, instance, validated_data):
        # Update title and description
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # Handle images (similar logic as before)
        images_data = validated_data.pop('images', [])
        for image_data in images_data:
            image_id = image_data.get('id')
            if image_id:
                try:
                    image = Image.objects.get(id=image_id, listing=instance)
                    image.image_url = image_data.get('image_url', image.image_url)
                    image.caption = image_data.get('caption', image.caption)
                    image.is_primary = image_data.get('is_primary', image.is_primary)
                    image.save()
                except Image.DoesNotExist:
                    Image.objects.create(listing=instance, **image_data)
            else:
                Image.objects.create(listing=instance, **image_data)

        # Handle primary image logic
        if images_data:
            primary_images = [img_data.get('is_primary') for img_data in images_data if img_data.get('is_primary')]
            if primary_images and len(primary_images) > 1:
                raise serializers.ValidationError("Only one image can be marked as primary.")

        return instance

class ListingDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=False)  # Handle a list of images
    amenities = serializers.SerializerMethodField()  # Custom method to get amenities
    security = serializers.SerializerMethodField()  # Custom method to get security information

    class Meta:
        model = Listing
        fields = '__all__'

    def get_amenities(self, obj):
        # Get the amenities related to this listing through the ListingAmenity relationship
        listing_amenities = ListingAmenity.objects.filter(listing=obj)
        return ListingAmenitySerializer(listing_amenities, many=True).data

    def get_security(self, obj):
        # Get security data related to this listing
        listing_securities = ListingSecurity.objects.filter(listing=obj)
        return ListingSecuritySerializer(listing_securities, many=True).data
class SecurityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityType
        fields = ['id', 'name', 'icon_url']

class ListingSecuritySerializer(serializers.ModelSerializer):
    security_name = serializers.CharField(source='security.name', read_only=True)  # Directly access the name

    class Meta:
        model = ListingSecurity
        fields = ['listing', 'security_name']  # No need to include SecurityTypeSerializer



class ListingStep3erializer(serializers.ModelSerializer):
    security_details = ListingSecuritySerializer(source='listingsecurity_set', many=True, read_only=True)  # Correct source to 'listingsecurity_set'

    class Meta:
        model = Listing
        fields = ['id', 'price_per_night', 'instant_bookable', 'security_details']
class FavoriteSerializer(serializers.ModelSerializer):
    listing=ListingDetailSerializer()
    class Meta:
        model = Favorite
        fields = ['id', 'listing', 'user']
        read_only_fields = ['user']
