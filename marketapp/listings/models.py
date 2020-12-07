from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import make_aware
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.validators import MinValueValidator, MaxValueValidator

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

    #Property to return number of unread messages for a user
    @property
    def unread_message_count(self):
        unread_count = 0

        #Get ids of conversation the user is related with
        conversation_ids = [
            conversation.id for conversation
            in Conversation.objects.all()
            if conversation.sender == self
            or conversation.recipient == self
        ]

        #Filter our the conversations that match the obtained ids
        conversations = Conversation.objects.filter(id__in=conversation_ids)

        if conversations.count() > 0:
            for conversation in conversations:
                if conversation.messages.filter(unread=True).exclude(author=self):
                    unread_count = unread_count + 1

        return unread_count

    #Property to return number of unread notifications for a user
    @property
    def unread_notification_count(self):
        unread_count = 0

        notifications_ids = [notification.id for notification
            in Notification.objects.all()
            if (notification.active == True
            and notification.user == self)]
        notifications = Notification.objects.filter(id__in=notifications_ids)

        if notifications:
            for notification in notifications:
                if notification.unread:
                    unread_count = unread_count + 1

        return unread_count

#model for Portfolios, where users can learn about one another and leave feedback
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=1000, blank=True, verbose_name="Biography",
        help_text="A biography for your profile so others can know you better.", default="None")
    country = models.TextField(max_length=50, default="None") #ideally should be obtained when the user shares ther location
    state = models.TextField(max_length=50, default="None") #ideally should be obtained when the user shares ther location
    city = models.TextField(max_length=50, default="None") #ideally should be obtained when the user shares ther location
    zipCode = models.TextField(max_length=10, verbose_name="Zip Code", default="None") #ideally should be obtained when the user shares ther location
    latitude = models.DecimalField(default=0.0000, max_digits=6, decimal_places=4)
    longitude = models.DecimalField(default=0.0000, max_digits=7, decimal_places=4)
    delivery = models.BooleanField(help_text="Check this if you are able to deliver items.", default=False)
    deliveryAddress = models.TextField(max_length=100, verbose_name="Delivery Address",
        help_text="Submit an delivery address that you pick up items from.",
        default="None")

    #Creates a profile object for the user when they are created
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    #Saves the profile object that was created when the user was made
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def get_absolute_url(self):
        """Returns the url to access a particular instance of Profile."""
        return reverse('profile-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Profile object."""
        return f"{self.user}'s Profile"

#Model for Warnings, used for tracking users after breaking rules (NOT USED)
#Fields needed: User, warningCount, reason, actionsTaken
class Warning(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
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
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender",
        null=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="recipient", null=True)
    topic = models.TextField(max_length=100, help_text="Topic of the Conversation")

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Conversation.
        return reverse('conversation-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Conversation object.
        return f'Conversation between {self.sender} & {self.recipient}'

#Model for Message, containing content to be read
#Fields needed: Conversation, author, content, dateSent, unread
class Message(models.Model):
    #Fields for Message
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE,
        null=True, related_name="messages")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
        null=True)
    content = models.TextField(max_length=500, default="None")
    dateSent = models.DateTimeField(auto_now_add=True, verbose_name="Date Sent")
    unread = models.BooleanField(default=True)

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Message.
        return reverse('message-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Message object.
        return f'Message from: {self.author}'

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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="images", width_field='width', height_field='height')
    name = models.TextField(max_length=50, verbose_name="Name of Image")
    tags = models.ManyToManyField(Tag, verbose_name="Item Tags",
        help_text="Qualities of the item in the photo, purpose and where one can find it can be used as tags.",
        blank=True)
    width = models.IntegerField()
    height = models.IntegerField()

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Image.
        return reverse('image-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Image object.
        return f'{self.name}'

#Model for Items, which can be listed in an offerListing, offered, searched for
#in a searchListing or added to a wishlist
#Fields needed: User, images, name, description
class Item(models.Model):
    #Fields for Item
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="items")
    images = models.ManyToManyField(Image)
    name = models.TextField(max_length=50, verbose_name="Item Name")
    description = models.TextField(max_length=250,
        help_text="A brief description of the item in the image(s).")

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Item.
        return reverse('item-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Item object.
        return f'{self.name}'

#Model for Wishlists, which a user can use to list items they want
#Fields needed: Owner, title, description
class Wishlist(models.Model):
    #Fields for Wishlist
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="wishlist")
    title = models.TextField(max_length=50)
    description = models.TextField(max_length=250,
        help_text="A brief description of your wishlist and what it contains.")
    items = models.ManyToManyField(Item)

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Wishlist.
        return reverse('wishlist-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Wishlist object.
        return f'{self.title}'

#Model for Event, when users want to organize an event with others
#Fields needed: Host, participants, title, context, date, location
class Event(models.Model):
    #Fields for Event
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="host")
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
#Fields needed: Event, receipient
class Invitation(models.Model):
    #Fields for Invitation
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, related_name="event")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="invitation_recipient")

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Invitation.
        return reverse('invite-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Invitation object.
        return f'"Invitation to ", {self.event.title}'

#Model for Listing, which contains a item(s) that users can search for and offer/bid on
#Fields needed: Owner, name, description, endTimeChoice, endTime, listingEnded
class Listing(models.Model):
    #Fields for Listing
    ONEHOUR = '1h'
    TWOHOURS = '2h'
    FOURHOURS = '4h'
    EIGHTHOURS = '8h'
    TWELVEHOURS = '12h'
    ONEDAY = '1d'
    THREEDAYS = '3d'
    SEVENDAYS = '7d'
    END_TIME_CHOICES = (
        (ONEHOUR, 'One Hours'),
        (TWOHOURS, 'Two Hours'),
        (FOURHOURS, 'Four Hours'),
        (EIGHTHOURS, 'Eight Hours'),
        (TWELVEHOURS, 'Twelve Hours'),
        (ONEDAY, 'One Day'),
        (THREEDAYS, 'Three Days'),
        (SEVENDAYS, 'Seven Days'),
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.TextField(max_length=100, verbose_name="Listing Name")
    description = models.TextField(max_length=500, verbose_name="Listing Description",
            help_text="A short description of what the listing obtains.")
    endTimeChoices = models.CharField(max_length=3, choices=END_TIME_CHOICES, default=ONEHOUR)
    endTime = models.DateTimeField(blank=True, null=True)
    items = models.ManyToManyField(Item)
    latitude = models.DecimalField(default=0.0000, max_digits=6, decimal_places=4, null=True)
    longitude = models.DecimalField(default=0.0000, max_digits=7, decimal_places=4, null=True)

    @property
    def listingEnded(self):
        return timezone.localtime(timezone.now()) > self.endTime

#Subclass for OfferListing, a listing that is interested in offers
#Fields needed: openToMoneyOffers, minRange, maxRange, notes, items, listingCompleted
class OfferListing(Listing):
    #Fields for OfferListing
    openToMoneyOffers = models.BooleanField(default=True, verbose_name="Open to Money Offers?",
        help_text="Leave this field unchecked if you're only interested in item offers.")
    minRange = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, null = True,
        verbose_name="Minimum Price Range",
        help_text="Minimum money offers you'll consider.")
    maxRange = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, null = True,
        verbose_name="Maximum Price Range",
        help_text="Maximum money offers you'll consider (leave blank if you don't have a maximum).")
    notes = models.TextField(max_length=500, help_text="Include here what offers you're seeking.")
    listingCompleted = models.BooleanField(default=False, null=True)

    def get_absolute_url(self):
        #Returns the url to access a particular instance of OfferListing.
        return reverse('offer-listing-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the OfferListing object.
        return f'{self.name}'

    #Create receipt for listing upon creation
    def save(self, *args, **kwargs):
        is_new = True if not self.id else False
        super(OfferListing, self).save(*args, **kwargs)
        if is_new and Receipt.objects.filter(listing=self).exists() != True:
            Receipt.objects.create(listing=self)

#Subclass for WishlistListing, a listing that is looking for item(s)
#Fields needed: MoneyOffer, ItemsOffer, notes
class WishlistListing(Listing):
    #Fields for WishlistListing
    moneyOffer = models.DecimalField(max_digits=9, decimal_places=2,
        verbose_name="Money Offer",
        help_text="Amount that you are offering for the items you're seeking.",
        null=True)
    itemsOffer = models.ManyToManyField(Item, verbose_name="Items You're Offering",
        help_text="Items that you would like to offer for the items you're seeking.")
    notes = models.TextField(max_length=500,
        help_text="Include here any details about the item(s) you're seeking.")

    def get_absolute_url(self):
        #Returns the url to access a particular instance of WishlistListing.
        return reverse('wishlist-listing-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the WishlistListing object.
        return f'{self.name}'


#Subclass for AuctionListing, a listing that is interested in bids (should this contain Item field?)
#Fields needed: StartingBid, minimumIncrement, autobuy
class AuctionListing(Listing):
    #Fields for AuctionListing
    startingBid = models.DecimalField(max_digits=9, decimal_places=2,
        verbose_name="Starting Bid",
        help_text="Money amount bidding should start at for auction.")
    minimumIncrement = models.DecimalField(max_digits=9, decimal_places=2,
        verbose_name="Minimum Increment",
        help_text="Minimum increment bid that can be placed on the auction, that cannot be greater than the starting bid (maximum increment bid will be x3 this value).")
    autobuy = models.DecimalField(default=None, max_digits=9, decimal_places=2, null=True,
        help_text="If a user bids the amount you set in this field, the auction will close and they will win the auction.")

    def get_absolute_url(self):
        #Returns the url to access a particular instance of AuctionListing.
        return reverse('auction-listing-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the AuctionListing object.
        return f'{self.name}'

    #Create receipt for listing upon creation
    def save(self, *args, **kwargs):
        is_new = True if not self.id else False
        super(AuctionListing, self).save(*args, **kwargs)
        if is_new and Receipt.objects.filter(listing=self).exists() != True:
            Receipt.objects.create(listing=self)

#Model for Bids, which is a money amount offered by a user on an auction
#Fields needed: AuctionListing, bidder, amount, winningBid
class Bid(models.Model):
    #Fields for Bid
    auctionListing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, null=True, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="bidder")
    amount = models.DecimalField(max_digits=9, decimal_places=2,
        verbose_name="Bid Amount",
        help_text="Amount of cash you'd like to bid on listing (Cannot be more than 3x the minimum bid value).")
    winningBid = models.BooleanField(default=False) #May need to make this a property

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Bid.
        return reverse('bid-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Bid object.
        return f'{self.id}'

#Model for Offers, which are items offered on an OfferListing (should this contain Item field?)
#Fields needed: OfferListing, owner, items, amount, offerAccepted
class Offer(models.Model):
    #Fields for Offer
    offerListing = models.ForeignKey(OfferListing, on_delete=models.CASCADE, null=True, related_name="offerlisting")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="owner")
    items = models.ManyToManyField(Item, help_text="Items you'd like to offer on listing (do not select anything if you do not wanna offer items).")
    amount = models.DecimalField(max_digits=9, decimal_places=2,
        verbose_name="Cash Offer",
        help_text="Amount of cash you'd like to offer on listing (leave blank if you do not want to offer cash).")
    offerAccepted = models.BooleanField(default=False, null=True)

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Offer.
        return reverse('offer-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Offer object.
        return f'"Offer by ", {self.owner}'

#Model for Ratings, where users can leave feedback for other users after exchanges
#Fields needed: Profile, reviewer, ratingValue, feedback, listingName
class Rating(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL,
        related_name="reviewer", null=True)
    ratingValue = models.IntegerField(default=1,
        verbose_name="Rating",
        help_text="Rating for user from 1 to 5, 5 being the best.",
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback = models.TextField(max_length=500,
        help_text="Leave feedback for the user you're rating.")
    listingName = models.TextField(max_length=100, verbose_name="Listing Name",
        null=True)

    def __str__(self):
        #String for representing the Rating object.
        return f'"Feedback from ", {self.reviewer}'

#Model for RatingTicket, created after a listing is completed between two user
#Fields needed: Rater, recevingUser, listing
class RatingTicket(models.Model):
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rating_ticket")
    receivingUser = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        #String for representing the RatingTicket object.
        return f'{self.listing.name}'

#Model for Reports, when users want admins to take notice of something against
#TOS or is inappropriate
#Fields needed: Reason, description
class Report(models.Model):
    #Fields for Report
    description = models.TextField(max_length=250, help_text=("Tell us more " +
        "in depth about the reason for reporting"))
    dateMade = models.DateTimeField(auto_now_add=True)
    reportType =  models.TextField(max_length=50, null=True)
    actionTaken = models.BooleanField(default=False, null=True)

#Subclass for ListingReport, when reporting an listing
#Fields needed: Listing
class ListingReport(Report):
    #Fields for ListingReport
    MC = 'Malicious Content'
    IC = 'Inappropriate Content'
    FA = 'False Advertising'
    ATS = 'Attempt to Scam'
    MI = 'Misleading Items'
    OT = 'Other'
    REASON_CHOICES = (
        (MC, 'Malicious Content'),
        (IC, 'Inappropriate Content'),
        (FA, 'False Advertising'),
        (ATS, 'Attempt to Scam'),
        (MI, 'Misleading Items'),
        (OT, 'Other'),
    )
    reason = models.TextField(max_length=150, choices=REASON_CHOICES,
        help_text="Reason for the report", null=True, default=MC)
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True,
        related_name="reports")

    def __str__(self):
        #String for representing the Report object.
        return f'"Report for Listing: ", {self.listing.name}'

#Subclass for EventReport, when reporting an event
#Fields needed: Event
class EventReport(Report):
    #Fields for EventReport
    ME = 'Malicious Event'
    IE = 'Inappropriate Event'
    ATSP = 'Attempt to Scam Paticipants'
    MDAE = 'Misleading Details About Event'
    OT = 'Other'
    REASON_CHOICES = (
        (ME, 'Malicious Event'),
        (IE, 'Inappropriate Event'),
        (ATSP, 'Attempt to Scam Paticipants'),
        (MDAE, 'Misleading Details About Event'),
        (OT, 'Other'),
    )
    reason = models.TextField(max_length=150, choices=REASON_CHOICES,
        help_text="Reason for the report", null=True, default=ME)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True,
        related_name="reports")

    def __str__(self):
        #String for representing the Report object.
        return f'"Report for Event: ", {self.event.title}'

#Subclass for UserReport, when reporting a user
#Fields needed: User
class UserReport(Report):
    #Fields for UserReport
    MU = 'Malicious User'
    ATS = 'Attempts to Scam'
    IM = 'Inappropriate Messaging'
    HA = 'Harassment'
    IP = 'Inappropriate Profile'
    OT = 'Other'
    REASON_CHOICES = (
        (MU, 'Malicious User'),
        (ATS, 'Attempts to Scam'),
        (IM, 'Inappropriate Messaging'),
        (HA, 'Harassment'),
        (IP, 'Inappropriate Profile'),
        (OT, 'Other'),
    )
    reason = models.TextField(max_length=150, choices=REASON_CHOICES,
        help_text="Reason for the report", null=True, default=MU)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
        related_name="reports")

    def __str__(self):
        #String for representing the Report object.
        return f'"Report for User: ", {self.user}'

#Subclass for RatingReport, when reporting a rating
#Fields needed: Rating
class RatingReport(Report):
    #Fields for RatingReport
    FR = 'False Rating'
    IR = 'Inappropriate Rating'
    ATS = 'Attempt to Slander'
    HA = 'Harassment'
    OT = 'Other'
    REASON_CHOICES = (
        (FR, 'False Rating'),
        (IR, 'Inappropriate Rating'),
        (ATS, 'Attempt to Slander'),
        (HA, 'Harassment'),
        (OT, 'Other'),
    )
    reason = models.TextField(max_length=150, choices=REASON_CHOICES,
        help_text="Reason for the report", null=True, default=FR)
    rating = models.ForeignKey(Rating, on_delete=models.SET_NULL, null=True,
        related_name="reports")

    def __str__(self):
        #String for representing the Report object.
        return f'"Report for Rating By: ", {self.rating.reviewer}'

#Subclass for WishlistReport, when reporting an wishlist
#Fields needed: Wishlist
class WishlistReport(Report):
    #Fields for WishlistReport
    MC = 'Malicious Content'
    IC = 'Inappropriate Content'
    OT = 'Other'
    REASON_CHOICES = (
        (MC, 'Malicious Content'),
        (IC, 'Inappropriate Content'),
        (OT, 'Other'),
    )
    reason = models.TextField(max_length=150, choices=REASON_CHOICES,
        help_text="Reason for the report", null=True, default=MC)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.SET_NULL, null=True,
        related_name="reports")

    def __str__(self):
        #String for representing the Report object.
        return f'"Report for Wishlist: ", {self.wishlist.title}'

#Subclass for ImageReport, when reporting an image
#Fields needed: Image
class ImageReport(Report):
    #Fields for ImageReport
    MI = 'Malicious Image'
    II = 'Inappropriate Image'
    FA = 'False Advertising'
    OT = 'Other'
    REASON_CHOICES = (
        (MI, 'Malicious Image'),
        (II, 'Inappropriate Image'),
        (FA, 'False Advertising'),
        (OT, 'Other'),
    )
    reason = models.TextField(max_length=150, choices=REASON_CHOICES,
        help_text="Reason for the report", null=True, default=MI)
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True,
        related_name="reports")

    def __str__(self):
        #String for representing the Report object.
        return f'"Report for Image: ", {self.image.name}'

#Model for Favorites, so a user can save a listing and come back to it
#Fields needed: listingType, listing, user
class Favorite(models.Model):
    #Fields for Favorite
    listingType = models.TextField(max_length=50, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="favorites", null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,
        null=True)

    def __str__(self):
        #String for representing the Favorite object.
        return f'{self.listing.name}'

#Model for Receipts, made after a transaction between users is completed
#Fields needed: Owner, exchangee, listing
class Receipt(models.Model):
    #Fields for Receipt
    owner = models.ForeignKey(User, on_delete=models.SET_NULL,
        related_name="listing_owner", null=True)
    exchangee = models.ForeignKey(User, on_delete=models.SET_NULL,
        related_name="listing_exchangee", null=True)
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE,
        related_name="receipt", null=True)

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Receipt.
        return reverse('receipt-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the Receipt object.
        return f'Receipt for {self.listing}'

#Model for PaymentReceipts, made after a paypal/online payment is made
#Fields needed: Receipt, orderID, status, amountPaid, fees, netAmount, paymentDate
class PaymentReceipt(models.Model):
    #Fields for PaymentReceipt
    receipt = models.OneToOneField(Receipt, on_delete=models.CASCADE,
        related_name="payment_receipt")
    orderID = models.TextField(max_length=100)
    status = models.TextField(max_length=100)
    amountPaid = models.DecimalField(max_digits=9, decimal_places=2)
    paymentDate = models.TextField(max_length=250)

    def get_absolute_url(self):
        #Returns the url to access a particular instance of PaymentReceipt.
        return reverse('payment-receipt-detail', args=[str(self.id)])

    def __str__(self):
        #String for representing the PaymentReceipt object.
        return f'Payment receipt for {self.receipt.listing.name}'

#Model for Notifications, made when most actions occur on site
#Fields needed: Content, creationDate
class Notification(models.Model):
    #Fields for ModelName
    user = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="notification", null=True)
    content = models.TextField(max_length=250)
    type = models.TextField(max_length=50, null=True)
    creationDate = models.DateTimeField()
    unread = models.BooleanField(default=True)

    @property
    def active(self):
        return timezone.localtime(timezone.now()) > self.creationDate

    def __str__(self):
        #String for representing the ModelName object.
        return f'{self.content}'

#Subclass for RatingNotification, a notification made when a user leaves feedback
#on another user's profile
#Fields needed: Profile, rater
class RatingNotification(Notification):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rater = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

#Subclass for WarningNotification, a notification made when a user receives a
#warning
#Fields needed: Warning
class WarningNotification(Notification):
    warning = models.ForeignKey(Warning, on_delete=models.CASCADE)

#Subclass for EventNotification, a notification made when a user joins or leaves
#an event
#Fields needed: Event, participant
class EventNotification(Notification):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

#Subclass for InvitationNotification, a notification made when a user receives
#an invitation to an event
#Fields needed: Invitation, participant
class InvitationNotification(Notification):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE)

#Subclass for ListingNotification, a notification made when a listing ends
#is deleted, or an offer is made or rejected
#Fields needed: Listing
class ListingNotification(Notification):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,
        null=True)

#Subclass for OfferNotification, a notification made when an offer is made,
#edited, retracted/rejected or accepted
#Fields needed: Listing, offer
class OfferNotification(Notification):
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL,
        null=True)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL,
        null=True)

#Subclass for BidNotification, a notification made when a bid is succeeded by
#a higher bid.  One is created for winning bid upon auction listing creation
#Fields needed: Listing, bid
class BidNotification(Notification):
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL,
        null=True)
    bid = models.ForeignKey(Bid, on_delete=models.SET_NULL,
        null=True)

#Subclass for PaymentNotification, a notification made when a user makes a
#payment to another user
#Fields needed: Receipt
class PaymentNotification(Notification):
    receipt = models.ForeignKey(Receipt, on_delete=models.SET_NULL,
        null=True)
