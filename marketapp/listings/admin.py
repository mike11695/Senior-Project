from django.contrib import admin
from listings.models import (User, Admin, Profile, Rating, Warning, Conversation,
    Message, Image, Tag, Wishlist, Event, Listing, OfferListing, AuctionListing,
    Item)

# Register your models here.
#admin.site.register(User)
#admin.site.register(Admin)
admin.site.register(Profile)
admin.site.register(Rating)
admin.site.register(Warning)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(Wishlist)
admin.site.register(Event)
#admin.site.register(Listing)
admin.site.register(OfferListing)
admin.site.register(AuctionListing)
admin.site.register(Item)

# Define the user admin class
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')

# Register the user admin class with the associated model
admin.site.register(User, UserAdmin)

# Define the admin admin class
class AdminAdmin(admin.ModelAdmin):
    list_display = ['superAdmin']

# Register the admin admin class with the associated model
admin.site.register(Admin, AdminAdmin)

# Define the Listing admin class
class ListingAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'endTime', 'listingEnded')
    list_filter = ['listingEnded']
    fields = ('owner', 'name', 'endTime', 'listingEnded', 'items')

# Register the admin admin class with the associated model
admin.site.register(Listing, ListingAdmin)
