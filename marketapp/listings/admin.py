from django.contrib import admin
from django.contrib.auth.models import AbstractUser, User
from listings.models import (User, Profile, Rating, Warning, Conversation,
    Message, Image, Tag, Wishlist, Event, Listing, OfferListing, AuctionListing,
    Item, WishlistListing, Offer, Bid)

# Register your models here.
#admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Rating)
admin.site.register(Warning)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(Wishlist)
admin.site.register(Event)
admin.site.register(WishlistListing)
admin.site.register(OfferListing)
admin.site.register(AuctionListing)
admin.site.register(Item)
admin.site.register(Offer)
admin.site.register(Bid)

# Define the user admin class
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    fields = ['username', 'password', ('is_superuser', 'is_staff'), 'groups',
        'user_permissions', 'first_name', 'last_name', 'email', 'paypalEmail',
        'invitesOpen', 'inquiriesOpen']

# Register the user admin class with the associated model
admin.site.register(User, UserAdmin)

# Define the Listing admin class
class ListingAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'endTime', 'listingEnded')
    fields = ('owner', 'name', 'endTime', 'listingEnded', 'items')

# Register the admin admin class with the associated model
admin.site.register(Listing, ListingAdmin)
