from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User  # Using Django's default User model
class Address(models.Model):
    address=models.CharField(max_length=255,blank=True, null=True)
    city = models.CharField(max_length=100,blank=True, null=True)
    state = models.CharField(max_length=100,blank=True, null=True)
    # country = models.CharField(max_length=100,blank=True, null=True)
    # zip_code = models.CharField(max_length=20, blank=True, null=True)

class Amenity(models.Model):
    name = models.CharField(max_length=255, unique=True)
    icon_url = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class ProperType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    icon_url = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name  # Returns the name of the property type
class RoomType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    icon_url = models.TextField(blank=True, null=True)
    description = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name  # Returns the name of the property type
class SecurityType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    icon_url = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name  # Returns the name of the property type

class Listing(models.Model):

    # PROPERTY_TYPES = [
    #     ('apartment', 'Apartment'),
    #     ('house', 'House'),
    #     ('guest_house', 'Guest House'),
    #     ('farmhouse', 'Farmhouse'),
    #     ('hostel', 'Hostel'),
    #     ('hotel', 'Hotel'),
    # ]

    # ROOM_TYPES = [
    #     ('entire_home', 'Entire Home/Apt'),
    #     ('private_room', 'Private Room'),
    #     ('shared_room', 'Shared Room'),
    # ]

    CANCELLATION_POLICIES = [
        ('flexible', 'Flexible'),
        ('moderate', 'Moderate'),
        ('strict', 'Strict'),
    ]

    LISTING_STATUSES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending_approval', 'Pending Approval'),
        ('suspended', 'Suspended'),
    ]
    
    #step2
    title = models.CharField(max_length=35, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True)
    # amenities = models.ManyToManyField('Amenity', through='ListingAmenity', related_name='listings')

    #step1
    property_type = models.ForeignKey(ProperType, on_delete=models.CASCADE, related_name='listings_property', blank=True, null=True)
    # property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, blank=True, null=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='listings_room', blank=True, null=True)
    # room_type = models.CharField(max_length=20, choices=ROOM_TYPES, blank=True, null=True)
    bedrooms = models.PositiveIntegerField(blank=True, null=True)
    beds = models.PositiveIntegerField(blank=True, null=True)
    # bedrooms = models.IntegerField(verbose_name='Number of bedrooms', blank=True, null=True)
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='adress_listing', blank=True, null=True)  # Foreign key to Address model
    accommodates = models.PositiveIntegerField( blank=True, null=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

#step3
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    instant_bookable = models.BooleanField(default=False)
    # security_type = models.ForeignKey(SecurityType, on_delete=models.CASCADE, related_name='listings_security', blank=True, null=True)

    
    cleaning_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    minimum_nights = models.PositiveIntegerField(blank=True, null=True)
    maximum_nights = models.PositiveIntegerField(blank=True, null=True)
    cancellation_policy = models.CharField(max_length=20, blank=True, null=True,choices=CANCELLATION_POLICIES)
    house_rules = models.TextField(blank=True)
    listing_status = models.CharField(max_length=20,blank=True, null=True ,choices=LISTING_STATUSES)
    review_count = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set to now when updated
    check_in_start_time = models.TimeField(blank=True, null=True)
    check_in_end_time = models.TimeField(blank=True, null=True)
    check_out_time = models.TimeField(blank=True, null=True)

    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings', blank=True, null=True)
  

    def __str__(self):
        return str(self.property_type) if self.property_type else "Listing without property type"

    def get_images(self):
        """Retrieve all images associated with this listing."""
        return Image.objects.filter(imageable_id=self.id, imageable_type='listing')
class ListingSecurity(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    security = models.ForeignKey(SecurityType, on_delete=models.CASCADE)
    # is_highlighted = models.BooleanField(default=False)


class ListingAmenity(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)
    is_highlighted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('listing', 'amenity')
        verbose_name = 'Listing Amenity'
        verbose_name_plural = 'Listing Amenities'

    def __str__(self):
        return f"{self.listing.title} - {self.amenity.name} (Highlighted: {self.is_highlighted})"

    def __str__(self):
        return f"{self.listing.title} - {self.security.name} "

class Image(models.Model):
    IMAGEABLE_TYPES = [
        ('user', 'User'),
        ('listing', 'Listing'),
    ]
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images',blank=True, null=True)  # Foreign key to Listing
    imageable_type = models.CharField(max_length=20, choices=IMAGEABLE_TYPES,blank=True, null=True)  # Type of entity (e.g., 'listing')
    image_url = models.TextField()  # URL of the image file
    caption = models.TextField(blank=True, null=True)  # Optional caption
    is_primary = models.BooleanField(default=False)  # Indicates if the image is primary
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when uploaded
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp of last update

    def __str__(self):
        return f"Image {self.id} ({self.imageable_type})"

    class Meta:
        verbose_name_plural = "Images"
class Favorite(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='favorites', 
        blank=True, 
        null=True
    )
    def __str__(self):
        return f"{self.user.username} favorited {self.listing.title}"
# class Booking(models.Model):
#     listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
#     check_in_date = models.DateField()
#     check_out_date = models.DateField()

#     def __str__(self):
#         return f"Booking for {self.listing.title} by {self.user.username}"


# class Image(models.Model):
#     listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
#     image_url = models.TextField()

#     def __str__(self):
#         return f"Image for {self.listing.title}"


# class Availability(models.Model):
#     listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='availability_records')
#     date = models.DateField()
#     is_available = models.BooleanField()

#     def __str__(self):
#         return f"Availability for {self.listing.title} on {self.date}"


# class CalendarEvent(models.Model):
#     EVENT_TYPES = [
#         ('booking', 'Booking'),
#         ('blocked', 'Blocked'),
#         ('other', 'Other'),
#     ]

#     listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='calendar_events')
#     event_date = models.DateField()
#     event_type = models.CharField(max_length=10, choices=EVENT_TYPES)

#     def __str__(self):
#         return f"{self.event_type} event for {self.listing.title} on {self.event_date}"


# class Discount(models.Model):
#     listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='discounts')
#     discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
#     start_date = models.DateField()
#     end_date = models.DateField()

#     def __str__(self):
#         return f"Discount for {self.listing.title} ({self.discount_percentage}%)"


# class ListingAmenity(models.Model):
#     listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
#     amenity_id = models.IntegerField()  # Reference to the amenity ID, consider creating an Amenity model

#     class Meta:
#         unique_together = ('listing', 'amenity_id')

#     def __str__(self):
#         return f"Amenity {self.amenity_id} for {self.listing.title}"


# class Wishlist(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
#     listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='wishlists')

#     def __str__(self):
#         return f"{self.user.username}'s wishlist for {self.listing.title}"
