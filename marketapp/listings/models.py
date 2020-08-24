from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
# Model template
"""
class ModelName(models.Model):
    #Fields for ModelName

    def get_absolute_url(self):
        #Returns the url to access a particular instance of ModelName.
        return reverse('ModelName-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the ModelName object.
        return f'{self.something}'
"""

#Extends the user model to added extra needed fields for the site
class User(AbstractUser):
    #added fields for the User class
    email = models.EmailField(max_length=100, unique=True)
    paypalEmail = models.EmailField(max_length=100,
        verbose_name="Paypal Email",
        help_text="E-mail that is connected to your PayPal account",
        unique=True)
    invitesOpen = models.BooleanField(default=True,
        verbose_name="Allow Invites for Events",
        help_text="Leave this field checked if you are interested in being invited to events.")
    inquiriesOpen = models.BooleanField(default=True,
        verbose_name="Allow Users to Contact You Through Profile",
        help_text="Leave this field checked if you are interested in being contacted by users through your profile.  If unchecked, users will only be able to contact you after you accept their offer or bid or you contact them.")

#Admin class that will be responsible for the site running smoothly
#Admins will be in charge of different responsiblities
class Admin(User):
    #potential extra fields will be added here
    superAdmin = models.BooleanField(default=False, verbose_name="Super Admin",
        help_text="Admin that is able to set, remove and configure other Admin accounts.")
    handleListings = models.BooleanField(default=False,
        verbose_name="Can Handle Listings",
        help_text="Admin is able to manage user listings.")
    handleEvents = models.BooleanField(default=False,
        verbose_name="Can Handle Events",
        help_text="Admin is able to manage user events.")
    handleWishlists = models.BooleanField(default=False,
        verbose_name="Can Handle Wishlists",
        help_text="Admin is able to manage user wishlists.")
    handleImages = models.BooleanField(default=False,
        verbose_name="Can Handle Images",
        help_text="Admin is able to manage user images.")
    handleRatings = models.BooleanField(default=False,
        verbose_name="Can Handle Ratings",
        help_text="Admin is able to manage user ratings.")

#model for Portfolios, where users can learn about one another and leave feedback
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1000, blank=True, verbose_name="Biography",
        help_text="A biography for your profile so others can know you better.", default="None")
    name = models.TextField(max_length=50, verbose_name="Full Name", default="None")
    country = models.TextField(max_length=50, default="None") #ideally should be obtained when the user shares ther location
    state = models.TextField(max_length=50, default="None") #ideally should be obtained when the user shares ther location
    city = models.TextField(max_length=50, default="None") #ideally should be obtained when the user shares ther location
    zipCode = models.TextField(max_length=10, verbose_name="Zip Code", default="None") #ideally should be obtained when the user shares ther location
    delivery = models.BooleanField(help_text="Check this if you are able to deliver items.", default=False)
    deliveryAddress = models.TextField(max_length=100, verbose_name="Delivery Address",
        help_text="Submit an delivery address that you pick up items from.",
        default="None")

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def get_absolute_url(self):
        """Returns the url to access a particular instance of Profile."""
        return reverse('profile-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Profile object."""
        return f'{self.user}, "s Profile"'

#Model for Ratings, where users can leave feedback for other users after exchanges
class Rating(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    reviewer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="reviewer")
    ratingValue = models.IntegerField(default=1,
        verbose_name="Rating",
        help_text="Rating for user from 1 to 5, 5 being the best.")
    feedback = models.TextField(max_length=500,
        help_text="Leave feedback for the user you're rating.")

    def get_absolute_url(self):
        """Returns the url to access a particular instance of Rating."""
        return reverse('rating-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Rating object."""
        return f'"Feedback from ", {self.reviewer}'

#Model for Warnings, used for tracking users after breaking rules
#Fields needed: Admin, user, warningCount, reason, actionsTaken
class Warning(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    admin = models.ForeignKey(Admin, on_delete=models.DO_NOTHING, related_name="admin")
    warningCount = models.IntegerField(verbose_name="Warning Count")
    reason = models.TextField(max_length=250, verbose_name="Reason for Warning",
        help_text="Submit reasoning for why you warned this user.")
    actionsTaken = models.TextField(max_length=500, verbose_name="Actions Taken",
        help_text="What actions were made regarding this user?")

    def get_absolute_url(self):
        """Returns the url to access a particular instance of Warning."""
        return reverse('warning-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Warning object."""
        return f'"Warning No. ", {self.warningCount}'

#Model for Conversations, which will hold messages sent between two users
#Fields needed: Sender, recipient, topic, unread
class Conversation(models.Model):
    #Fields for Conversation
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipient")
    topic = models.TextField(max_length=100, help_text="Topic of the Conversation")
    unread = models.BooleanField(default=True)

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Conversation.
        return reverse('conversation-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Conversation object.
        return f'"Conversation between", {self.sender}, " & ", {self.recipient}'

#Model for Message, containing content to be read
#Fields needed: Author, content, dateSent
class Message(models.Model):
    #Fields for Message
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500, default="None")
    dateSent = models.DateTimeField(auto_now_add=True, verbose_name="Date Sent")

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Message.
        return reverse('message-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Message object.
        return f'"Mesage from: ", {self.author}'

#Model for Tags, used to catagorize images
#Fields needed: Name
class Tag(models.Model):
    #Fields for Tag
    name = models.TextField(max_length=50, verbose_name="Tag Name")

    def __str__(self):
        #String for representing the Tag object.
        return f'{self.name}'

#Model for Images, used in wishlists and listings
#Fields needed: Owner, image, name, type
class Image(models.Model):
    #Fields for Image
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="marketapp\listings\images")
    name = models.TextField(max_length=50, verbose_name="Name of Image")
    tags = models.ManyToManyField(Tag, verbose_name="Item Tags",
        help_text="Qualities of the item in the photo, purpose and where one can find it can be used as tags.")

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Image.
        return reverse('image-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Image object.
        return f'{self.name}'

#Model for Wishlists, which a user can use to list items they want
#Fields needed: Owner, title, description
class Wishlist(models.Model):
    #Fields for Wishlist
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(max_length=50)
    description = models.TextField(max_length=250,
        help_text="A brief description of your wishlist and what it contains.")

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Wishlist.
        return reverse('wishlist-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Wishlist object.
        return f'{self.title}'

#Model for WishlistItem, an item found in wishlists (Should this be replaced by item class?)
#Fields needed: Image, name, description
class WishlistItem(models.Model):
    #Fields for WishlistItem
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    images = models.ManyToManyField(Image)
    name = models.TextField(max_length=50, verbose_name="Item Name")
    description = models.TextField(max_length=250,
        help_text="A brief description of the item in the image(s).")

    def get_absolute_url(self):
        #Returns the url to access a particular instance of WishlistItem.
        return reverse('wishlistitem-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the WishlistItem object.
        return f'{self.name}'

#Model for Event, when users want to organize an event with others
#Fields needed: Host, participants, title, context, date, location
class Event(models.Model):
    #Fields for Event
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="host")
    participants = models.ManyToManyField(User, related_name="participants")
    title = models.TextField(max_length=50, verbose_name="Title of Event")
    context = models.TextField(max_length=250,
        help_text="What is the event for?  What will happen/be accomplished?")
    date = models.DateTimeField(blank=False, verbose_name="Date and Time of Event")
    location = models.TextField(max_length=100, verbose_name="Address where Event is Held")

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Event.
        return reverse('event-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Event object.
        return f'{self.title}'

#Model for Invitations, so hosts can invite participants to events
#Fields needed: Sender, receipients, event, topic, context
"""class Invitation(models.Model):
    #Fields for Invitation

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Invitation.
        return reverse('ModelName-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Invitation object.
        return f'"Invitation to ", {self.event.title}'"""

#Model for Reports, when users want admins to take notice of something against
#TOS or is inappropriate
#Fields needed: Reason, description
"""class Report(models.Model):
    #Fields for Report

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Report.
        return reverse('report-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Report object.
        return f'"Report ", {self.id}'"""

#Subclass for ListingReport, when reporting an listing
#Fields needed: Listing
"""class LitingReport(Report):
    #Fields for LitingReport"""

#Subclass for EventReport, when reporting an event
#Fields needed: Event
"""class EventReport(Report):
    #Fields for EventReport"""

#Subclass for UserReport, when reporting a user
#Fields needed: User
"""class UserReport(Report):
    #Fields for UserReport"""

#Subclass for RatingReport, when reporting a rating
#Fields needed: Rating
"""class RatingReport(Report):
    #Fields for RatingReport"""

#Subclass for WishlistReport, when reporting an wishlist
#Fields needed: Wishlist
"""class WishlistReport(Report):
    #Fields for WishlistReport"""

#Subclass for ImageReport, when reporting an image
#Fields needed: Image
"""class ImageReport(Report):
    #Fields for ImageReport"""

#Model for Listing, which contains a item(s) that users can search for and offer/bid on
#Fields needed: Name, images, description, attributes
"""class Listing(models.Model):
    #Fields for Listing

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Listing.
        return reverse('listing-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Listing object.
        return f'{self.name}'"""

#Subclass for OfferListing, a listing that is interested in offers
#Fields needed: Price, notes, items
"""class OfferListing(Report):
    #Fields for OfferListing"""

#Subclass for SearchListing, a listing that is looking for item(s)
#Fields needed: PriceOffer, itemsOffer, notes
"""class SearchListing(Report):
    #Fields for SearchListing"""

#Subclass for AuctionListing, a listing that is interested in bids (should this contain Item field?)
#Fields needed: StartingBid, endTime, startingBid, currentBid, autobuy
"""class AuctionListing(Report):
    #Fields for AuctionListing"""

#Model for Bids, which is a money amount offered by a user on an auction
#Fields needed: Bidder, bidAmount
"""class Bid(models.Model):
    #Fields for Bid

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Bid.
        return reverse('bid-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Bid object.
        return f'{self.id}'"""

#Model for Offers, which are items offered on an OfferListing (should this contain Item field?)
#Fields needed: offerUser, items, amount
"""class Offer(models.Model):
    #Fields for Offer

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Offer.
        return reverse('offer-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Offer object.
        return f'"Offer by ", {self.something}'"""

#Model for Items, which can be offered in an offerListing or
#searched for in a searchListing
#Fields needed: Image, name
"""class Item(models.Model):
    #Fields for Item

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Item.
        return reverse('item-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Item object.
        return f'{self.name}'"""

#Model for Favorites, so a user can save a listing and come back to it
#Fields needed: Category, listing
"""class Favorite(models.Model):
    #Fields for Favorite

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Favorite.
        return reverse('favorite-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Favorite object.
        return f'{self.listing.name}'"""

#Model for Receipts, made after a transaction between users is completed
#Fields needed: Owner, buyer, listing
"""class Receipt(models.Model):
    #Fields for Receipt

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Receipt.
        return reverse('receipt-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Receipt object.
        return f'"Receipt for ", {self.listing.name}'"""
