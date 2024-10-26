from django.contrib import admin
from .models import *
# Register the models with the admin site
admin.site.register(Listing )
admin.site.register(Image)  # You can choose to register or not depending on your needs
admin.site.register(Amenity)
admin.site.register(Address)
admin.site.register(ListingAmenity)

admin.site.register(ProperType)
admin.site.register(RoomType)
admin.site.register(SecurityType)
admin.site.register(ListingSecurity)

admin.site.register(Favorite)
