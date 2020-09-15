from django.test import TestCase
from listings.models import (User, Profile, Rating, Warning, Conversation,
    Message, Image, Tag, Wishlist, Event, Listing, OfferListing, AuctionListing,
    Item, Offer, Bid)
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
from django.utils.timezone import make_aware
from django.conf import settings

# Create your tests here.
class MyTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True) #profile is created when the user is created
        user2 = User.objects.create(username="mike3", password="example",
            email="example3@text.com", paypalEmail="example3@text.com",
            invitesOpen=True, inquiriesOpen=True)
        self.global_user1 = user1
        self.global_user2 = user2
        test_image = SimpleUploadedFile(name='art1.png', content=open('listings/imagetest/art1.png', 'rb').read(), content_type='image/png')
        self.global_image = Image.objects.create(owner=self.global_user1,
            image=test_image, name="Test Image")
        self.tag = Tag.objects.create(name="Test Tag")
        self.global_image.tags.add(self.tag)
        self.global_image.save
        self.global_item = Item.objects.create(name="Global Item",
            description="A global item for testing")
        self.global_item.images.add(self.global_image)
        self.global_item.save

        date = datetime.today()
        settings.TIME_ZONE
        aware_date = make_aware(date)

        self.global_offer_listing = OfferListing.objects.create(owner=user1,
            name="My Items For Offers", description="A few items up for offers",
            openToMoneyOffers=True, minRange=5.00, maxRange=10.00, notes="Just offer",
            endTime=aware_date)
        self.global_offer_listing.items.add = self.global_item
        self.global_offer_listing.save

        self.global_auction_listing = AuctionListing.objects.create(owner=user1,
            name="My Test Auction", description="Just a test auction please ignore.",
            startingBid = 5.00, minimumIncrement = 0.25, autobuy = 25.00,
            endTime=aware_date)
        self.global_auction_listing.items.add = self.global_item
        self.global_auction_listing.save

#Tests for User class
class UserModelTest(MyTestCase):

    #Checks to ensure that an email max length is 100
    def text_email_length(self):
        user = self.global_user1
        max_length = user._meta.get_field('email').max_length
        self.assertEqual(max_length, 100)

    #Checks to ensure that an email must not be blank
    def text_email_blank(self):
        user = self.global_user1
        blank = user._meta.get_field('email').blank
        self.assertEqual(blank, False)

    #Checks to ensure that an email must be unique
    def text_email_unique(self):
        user = self.global_user1
        unique = user._meta.get_field('email').unique
        self.assertEqual(unique, True)

    #Checks to ensure that the paypalEmail field verbose text is correct
    def test_paypal_email_label(self):
        user = self.global_user1
        field_label = user._meta.get_field('paypalEmail').verbose_name
        self.assertEqual(field_label, 'Paypal Email')

    #Checks to ensure that an paypal email max length is 100
    def test_paypal_email_length(self):
        user = self.global_user1
        max_length = user._meta.get_field('paypalEmail').max_length
        self.assertEqual(max_length, 100)

    #Checks to ensure that the paypalEmail field help text is correct
    def test_paypal_email_help_text(self):
        user = self.global_user1
        help_text = user._meta.get_field('paypalEmail').help_text
        self.assertEqual(help_text, 'E-mail that is connected to your PayPal account')

    #Checks to ensure that an paypalEmail must not be blank
    def text_paypal_email_blank(self):
        user = self.global_user1
        blank = user._meta.get_field('paypalEmail').blank
        self.assertEqual(blank, False)

    #Checks to ensure that an paypaLEmail must be unique
    def text_paypal_email_unique(self):
        user = self.global_user1
        unique = user._meta.get_field('paypalEmail').unique
        self.assertEqual(unique, True)

    #Checks to ensure that invitesOpen defaults to true
    def test_invites_open_default(self):
        user = self.global_user1
        default = user._meta.get_field('invitesOpen').default
        self.assertEqual(default, True)

    #Checks to ensure that the invitesOpen field verbose text is correct
    def test_invites_open_label(self):
        user = self.global_user1
        field_label = user._meta.get_field('invitesOpen').verbose_name
        self.assertEqual(field_label, 'Allow Invites for Events')

    #Checks to ensure that the invitesOpen field help text is correct
    def test_invites_open_help_text(self):
        user = self.global_user1
        help_text = user._meta.get_field('invitesOpen').help_text
        self.assertEqual(help_text, 'Leave this field checked if you are interested in being invited to events.')

    #Checks to ensure that invitesOpen defaults to true
    def test_inquiries_open_default(self):
        user = self.global_user1
        default = user._meta.get_field('inquiriesOpen').default
        self.assertEqual(default, True)

    #Checks to ensure that the inquiriesOpen field verbose text is correct
    def test_invites_open_label(self):
        user = self.global_user1
        field_label = user._meta.get_field('inquiriesOpen').verbose_name
        self.assertEqual(field_label, 'Allow Users to Contact You Through Profile')

    #Checks to ensure that the inquiriesOpen field help text is correct
    def test_invites_open_help_text(self):
        user = self.global_user1
        help_text = user._meta.get_field('inquiriesOpen').help_text
        self.assertEqual(help_text, 'Leave this field checked if you are interested in being contacted by users through your profile.  If unchecked, users will only be able to contact you after you accept their offer or bid or you contact them.')

#Tests for Profile Class
class ProfileModelTest(MyTestCase):

    #Checks to ensure that bio has a max length of 1000
    def test_bio_max_length(self):
        profile = self.global_user1.profile
        max_length = profile._meta.get_field('bio').max_length
        self.assertEqual(max_length, 1000)

    #Checks to ensure that the bio field verbose text is correct
    def test_bio_label(self):
        profile = self.global_user1.profile
        field_label = profile._meta.get_field('bio').verbose_name
        self.assertEqual(field_label, "Biography")

    #Checks to ensure that the bio field help text is correct
    def test_bio_help_text(self):
        profile = self.global_user1.profile
        help_text = profile._meta.get_field('bio').help_text
        self.assertEqual(help_text, "A biography for your profile so others can know you better.")

    #Checks to ensure that country has a max length of 50
    def test_country_length(self):
        profile = self.global_user1.profile
        max_length = profile._meta.get_field('country').max_length
        self.assertEqual(max_length, 50)

    #Checks to ensure that state has a max length of 50
    def test_state_length(self):
        profile = self.global_user1.profile
        max_length = profile._meta.get_field('state').max_length
        self.assertEqual(max_length, 50)

    #Checks to ensure that city has a max length of 50
    def test_city_length(self):
        profile = self.global_user1.profile
        max_length = profile._meta.get_field('city').max_length
        self.assertEqual(max_length, 50)

    #Checks to ensure that zipCode has a max length of 50
    def test_zip_code_max_length(self):
        profile = self.global_user1.profile
        max_length = profile._meta.get_field('zipCode').max_length
        self.assertEqual(max_length, 10)

    #Checks to ensure that the zipCode field verbose text is correct
    def test_zip_code_label(self):
        profile = self.global_user1.profile
        field_label = profile._meta.get_field('zipCode').verbose_name
        self.assertEqual(field_label, "Zip Code")

    #Checks to ensure that the delivery field help text is correct
    def test_delivery_help_text(self):
        profile = self.global_user1.profile
        help_text = profile._meta.get_field('delivery').help_text
        self.assertEqual(help_text, "Check this if you are able to deliver items.")

    #Checks to ensure that deliveryAddress has a max length of 50
    def test_delivery_address_max_length(self):
        profile = self.global_user1.profile
        max_length = profile._meta.get_field('deliveryAddress').max_length
        self.assertEqual(max_length, 100)

    #Checks to ensure that the deliveryAddress field verbose text is correct
    def test_delivery_address_label(self):
        profile = self.global_user1.profile
        field_label = profile._meta.get_field('deliveryAddress').verbose_name
        self.assertEqual(field_label, "Delivery Address")

    #Checks to ensure that the deliveryAddress field help text is correct
    def test_delivery_address_help_text(self):
        profile = self.global_user1.profile
        help_text = profile._meta.get_field('deliveryAddress').help_text
        self.assertEqual(help_text, "Submit an delivery address that you pick up items from.")

#Tests for Rating Class
class RatingModelTest(MyTestCase):
    def setUp(self):
        #Set up rating record for testing
        super(RatingModelTest, self).setUp()
        self.rating = Rating.objects.create(profile=self.global_user1.profile, reviewer=self.global_user2,
            ratingValue=1, feedback="You're awful.")

    #Checks to ensure that the ratingValue field verbose text is correct
    def test_rating_value_verbose_text(self):
        rating = self.rating
        verbose_text = rating._meta.get_field('ratingValue').verbose_name
        self.assertEqual(verbose_text, "Rating")

    #Checks to ensure that the ratingValue field help text is correct
    def test_rating_value_help_text(self):
        rating = self.rating
        help_text = rating._meta.get_field('ratingValue').help_text
        self.assertEqual(help_text, "Rating for user from 1 to 5, 5 being the best.")

    #Checks to ensure that the feedback field help text is correct
    def test_feedback_help_text(self):
        rating = self.rating
        help_text = rating._meta.get_field('feedback').help_text
        self.assertEqual(help_text, "Leave feedback for the user you're rating.")

#Tests for Warning Class
class WarningModelTest(MyTestCase):
    def setUp(self):
        #Set up warning record for testing
        super(WarningModelTest, self).setUp()
        self.warning = Warning.objects.create(user=self.global_user1,
            warningCount=1, reason="For testing", actionsTaken="None")

    #Checks to ensure that warningCount field verbose text is correct
    def test_warning_count_label(self):
        warning = self.warning
        field_label = warning._meta.get_field('warningCount').verbose_name
        self.assertEqual(field_label, "Warning Count")

    #Checks to ensure that reason field length is correct
    def test_reason_max_length(self):
        warning = self.warning
        max_length = warning._meta.get_field('reason').max_length
        self.assertEqual(max_length, 250)

    #Checks to ensure that reason field verbose text is correct
    def test_reason_label(self):
        warning = self.warning
        field_label = warning._meta.get_field('reason').verbose_name
        self.assertEqual(field_label, "Reason for Warning")

    #Checks to ensure that the reason field help text is correct
    def test_reason_help_text(self):
        warning = self.warning
        help_text = warning._meta.get_field('reason').help_text
        self.assertEqual(help_text, "Submit reasoning for why you warned this user.")

    #Checks to ensure that actionsTaken length is correct
    def test_actions_taken_max_length(self):
        warning = self.warning
        max_length = warning._meta.get_field('actionsTaken').max_length
        self.assertEqual(max_length, 500)

    #Checks to ensure that actionsTaken field verbose text is correct
    def test_actions_taken_label(self):
        warning = self.warning
        field_label = warning._meta.get_field('actionsTaken').verbose_name
        self.assertEqual(field_label, "Actions Taken")

    #Checks to ensure that the actionsTaken field help text is correct
    def test_actions_taken_help_text(self):
        warning = self.warning
        help_text = warning._meta.get_field('actionsTaken').help_text
        self.assertEqual(help_text, "What actions were made regarding this user?")

#Tests for Conversation Class
class ConversationModelTest(MyTestCase):
    def setUp(self):
        #Set up conversation record for testing
        super(ConversationModelTest, self).setUp()
        self.conversation = Conversation.objects.create(sender=self.global_user1,
            recipient=self.global_user2, topic="Nothing.")

    #Checks to ensure that topic field length is correct
    def test_topic_max_length(self):
        conversation = self.conversation
        max_length = conversation._meta.get_field('topic').max_length
        self.assertEqual(max_length, 100)

    #Checks to ensure that topic field help text is correct
    def test_topic_help_text_length(self):
        conversation = self.conversation
        help_text = conversation._meta.get_field('topic').help_text
        self.assertEqual(help_text, "Topic of the Conversation")

    #Checks to ensure that unread field defaults to true
    def test_unread_eaault(self):
        conversation = self.conversation
        default = conversation._meta.get_field('unread').default
        self.assertEqual(default, True)

#Tests for Message Class
class MessageModelTest(MyTestCase):
    def setUp(self):
        #Set up conversation and message record for testing
        super(MessageModelTest, self).setUp()
        self.conversation = Conversation.objects.create(sender=self.global_user1,
            recipient=self.global_user2, topic="Nothing.")
        self.message = Message.objects.create(author=self.global_user1,
            content="Nothing")

    #Checks to ensure that content length is correct
    def test_content_max_length(self):
        message = self.message
        max_length = message._meta.get_field('content').max_length
        self.assertEqual(max_length, 500)

    #Checks to ensure that dateSent field verbose text is correct
    def test_date_sent_label(self):
        message = self.message
        field_label = message._meta.get_field('dateSent').verbose_name
        self.assertEqual(field_label, "Date Sent")

#Tests for Image Class
class ImageAndTagsModelTest(MyTestCase):
    #Checks to ensure that Image name length is correct
    def test_image_name_max_length(self):
        image = self.global_image
        max_length = image._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    #Checks to ensure that name field for Image verbose text is correct
    def test_image_name_label(self):
        image = self.global_image
        verbose_name = image._meta.get_field('name').verbose_name
        self.assertEqual(verbose_name, "Name of Image")

    #Checks to ensure that tags field verbose text is correct
    def test_image_tag_label(self):
        image = self.global_image
        verbose_name = image._meta.get_field('tags').verbose_name
        self.assertEqual(verbose_name, "Item Tags")

    #Checks to ensure that tags field help text is correct
    def test_image_tag_help_text(self):
        image = self.global_image
        help_text = image._meta.get_field('tags').help_text
        self.assertEqual(help_text, "Qualities of the item in the photo, purpose and where one can find it can be used as tags.")

    #Checks to ensure that Tag name length is correct
    def test_tag_name_max_length(self):
        tag = self.tag
        max_length = tag._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    #Checks to ensure that name field for Tag verbose text is correct
    def test_image_name_label(self):
        tag = self.tag
        verbose_name = tag._meta.get_field('name').verbose_name
        self.assertEqual(verbose_name, "Tag Name")

#Tests for Wishlist Class
class WishlistModelTest(MyTestCase):
    def setUp(self):
        #Set up wishlist record for testing
        super(WishlistModelTest, self).setUp()
        self.wishlist = Wishlist.objects.create(owner=self.global_user1,
            title="My Boring Wishlist", description="Nothing.")

    #Checks to ensure that Wishlist title length is correct
    def test_wishlist_title_max_length(self):
        wishlist = self.wishlist
        max_length = wishlist._meta.get_field('title').max_length
        self.assertEqual(max_length, 50)

    #Checks to ensure that Wishlist description length is correct
    def test_wishlist_description_max_length(self):
        wishlist = self.wishlist
        max_length = wishlist._meta.get_field('description').max_length
        self.assertEqual(max_length, 250)

    #Checks to ensure that Wishlist description help text is correct
    def test_wishlist_description_max_length(self):
        wishlist = self.wishlist
        help_text = wishlist._meta.get_field('description').help_text
        self.assertEqual(help_text, "A brief description of your wishlist and what it contains.")

#Tests for WishlistItem Class
"""class WishlistItemModelTest(MyTestCase):
    def setUp(self):
        #Set up wishlist item record for testing
        super(WishlistItemModelTest, self).setUp()
        self.wishlist = Wishlist.objects.create(owner=self.global_user1,
            title="My Boring Wishlist", description="Nothing.")
        self.wishlist_item = WishlistItem.objects.create(wishlist=self.wishlist,
            name="My Boring Wishlist Item", description="Nothing.")
        self.wishlist_item.images.add = self.global_image
        self.wishlist_item.save

    #Checks to ensure that WishlistItem name length is correct
    def test_wishlist_item_name_max_length(self):
        wishlist_item = self.wishlist_item
        max_length = wishlist_item._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    #Checks to ensure that WishlistItem name verbose text is correct
    def test_wishlist_item_name_label(self):
        wishlist_item = self.wishlist_item
        verbose_name = wishlist_item._meta.get_field('name').verbose_name
        self.assertEqual(verbose_name, "Item Name")

    #Checks to ensure that WishlistItem description length is correct
    def test_wishlist_item_description_max_length(self):
        wishlist_item = self.wishlist_item
        max_length = wishlist_item._meta.get_field('description').max_length
        self.assertEqual(max_length, 250)

    #Checks to ensure that WishlistItem name help text is correct
    def test_wishlist_item_description_help_text(self):
        wishlist_item = self.wishlist_item
        help_text = wishlist_item._meta.get_field('description').help_text
        self.assertEqual(help_text, "A brief description of the item in the image(s).")"""

#Tests for Event Class
class EventModelTest(MyTestCase):
    def setUp(self):
        #Set up event record for testing
        super(EventModelTest, self).setUp()
        date = datetime.today()
        settings.TIME_ZONE
        aware_date = make_aware(date)
        self.event = Event.objects.create(host=self.global_user1,
            title="My Boring Event", context="Nothing.", date=aware_date,
            location="Potsdam, NY")
        self.event.participants.add = self.global_user2
        self.event.save

    #Checks to ensure that Event title max length is correct
    def test_event_title_max_length(self):
        event = self.event
        max_length = event._meta.get_field('title').max_length
        self.assertEqual(max_length, 50)

    #Checks to ensure that Event title verbose name is correct
    def test_event_title_verbose_name(self):
        event = self.event
        verbose_name = event._meta.get_field('title').verbose_name
        self.assertEqual(verbose_name, "Title of Event")

    #Checks to ensure that Event context max length is correct
    def test_event_context_max_length(self):
        event = self.event
        max_length = event._meta.get_field('context').max_length
        self.assertEqual(max_length, 250)

    #Checks to ensure that Event context help text is correct
    def test_event_context_help_text(self):
        event = self.event
        help_text = event._meta.get_field('context').help_text
        self.assertEqual(help_text, "What is the event for?  What will happen/be accomplished?")

    #Checks to ensure that Event date verbose name is correct
    def test_event_date_max_length(self):
        event = self.event
        verbose_name = event._meta.get_field('date').verbose_name
        self.assertEqual(verbose_name, "Date and Time of Event")

    #Checks to ensure that Event location max length is correct
    def test_event_location_max_length(self):
        event = self.event
        max_length = event._meta.get_field('location').max_length
        self.assertEqual(max_length, 100)

    #Checks to ensure that Event location verbose name is correct
    def test_event_location_max_length(self):
        event = self.event
        verbose_name = event._meta.get_field('location').verbose_name
        self.assertEqual(verbose_name, "Address where Event is Held")


#Test for Invitation Class

#Tests for Report Class

#Tests for ListingReport subclass

#Tests for EventReport subclass

#Tests for UserReport subclass

#Tests for RatingReport subclass

#Tests for WishlistReport subclass

#Tests for ImageReport subclass

#Tests for Item class
class ItemModelTest(MyTestCase):
    #Checks to ensure that Item name max length is correct
    def test_item_name_max_length(self):
        item = self.global_item
        max_length = item._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    #Checks to ensure that Item name verbose name is correct
    def test_item_name_label(self):
        item = self.global_item
        verbose_name = item._meta.get_field('name').verbose_name
        self.assertEqual(verbose_name, "Item Name")

    #Checks to ensure that Item description max length is correct
    def test_item_description_max_length(self):
        item = self.global_item
        max_length = item._meta.get_field('description').max_length
        self.assertEqual(max_length, 250)

    #Checks to ensure that Item description help text is correct
    def test_item_description_help_text(self):
        item = self.global_item
        help_text = item._meta.get_field('description').help_text
        self.assertEqual(help_text, "A brief description of the item in the image(s).")

#Tests for Listing Class
class ListingsModelTest(MyTestCase):
    def setUp(self):
        #Set up records for OfferListing and AuctionListing for testing
        #SearchListing tests will be added later
        super(ListingsModelTest, self).setUp()
        date = datetime.today()
        settings.TIME_ZONE
        aware_date = make_aware(date)
        self.offerListing = self.global_offer_listing
        self.auctionListing = AuctionListing.objects.create(owner=self.global_user1,
            name="My Items for Bids", description="A few items up for bids",
            startingBid=5.00, minimumIncrement=1.00, autobuy=50.00,
            endTime=aware_date)
        self.auctionListing.items.add = self.global_item
        self.auctionListing.save

    #Checks to ensure that Listing name max length is correct
    def test_listing_name_max_length(self):
        listing = self.offerListing
        max_length = listing._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    #Checks to ensure that Listing name verbose name is correct
    def test_listing_name_label(self):
        listing = self.offerListing
        verbose_name = listing._meta.get_field('name').verbose_name
        self.assertEqual(verbose_name, "Listing Name")

    #Checks to ensure that Listing description max length is correct
    def test_listing_description_max_length(self):
        listing = self.offerListing
        max_length = listing._meta.get_field('description').max_length
        self.assertEqual(max_length, 500)

    #Checks to ensure that Listing description verbose name is correct
    def test_listing_description_label(self):
        listing = self.offerListing
        verbose_name = listing._meta.get_field('description').verbose_name
        self.assertEqual(verbose_name, "Listing Description")

    #Checks to ensure that Listing description help text is correct
    def test_listing_description_help_text(self):
        listing = self.offerListing
        help_text = listing._meta.get_field('description').help_text
        self.assertEqual(help_text, "A short description of what the listing obtains.")

    #Checks to ensure that Listing endTimeChoices max length is correct
    def test_listing_end_time_max_length(self):
        listing = self.offerListing
        max_length = listing._meta.get_field('endTimeChoices').max_length
        self.assertEqual(max_length, 3)

    #Checks to ensure that Listing endTimeChoices default is correct
    def test_listing_end_time_default(self):
        listing = self.offerListing
        default = listing._meta.get_field('endTimeChoices').default
        self.assertEqual(default, '1h')

    #Checks to ensure that OfferListing openToMoneyOffers default is correct
    def test_offer_listing_open_default(self):
        offer_listing = self.offerListing
        default = offer_listing._meta.get_field('openToMoneyOffers').default
        self.assertEqual(default, True)

    #Checks to ensure that OfferListing openToMoneyOffers verbose name is correct
    def test_offer_listing_open_label(self):
        offer_listing = self.offerListing
        verbose_name = offer_listing._meta.get_field('openToMoneyOffers').verbose_name
        self.assertEqual(verbose_name, "Open to Money Offers?")

    #Checks to ensure that OfferListing openToMoneyOffers help text is correct
    def test_offer_listing_open_help_text(self):
        offer_listing = self.offerListing
        help_text = offer_listing._meta.get_field('openToMoneyOffers').help_text
        self.assertEqual(help_text, "Leave this field unchecked if you're only interested in item offers.")

    #Checks to ensure that OfferListing minRange max digits is correct
    def test_offer_listing_min_range_digits(self):
        offer_listing = self.offerListing
        max_digits = offer_listing._meta.get_field('minRange').max_digits
        self.assertEqual(max_digits, 9)

    #Checks to ensure that OfferListing minRange decimal places is correct
    def test_offer_listing_min_range_decimals(self):
        offer_listing = self.offerListing
        decimal_places = offer_listing._meta.get_field('minRange').decimal_places
        self.assertEqual(decimal_places, 2)

    #Checks to ensure that OfferListing minRange verbose name is correct
    def test_offer_listing_min_range_verbose_name(self):
        offer_listing = self.offerListing
        verbose_name = offer_listing._meta.get_field('minRange').verbose_name
        self.assertEqual(verbose_name, "Minimum Price Range")

    #Checks to ensure that OfferListing minRange help text is correct
    def test_offer_listing_min_range_help_text(self):
        offer_listing = self.offerListing
        help_text = offer_listing._meta.get_field('minRange').help_text
        self.assertEqual(help_text, "Minimum money offers you'll consider.")

    #Checks to ensure that OfferListing maxRange max digits is correct
    def test_offer_listing_max_range_digits(self):
        offer_listing = self.offerListing
        max_digits = offer_listing._meta.get_field('maxRange').max_digits
        self.assertEqual(max_digits, 9)

    #Checks to ensure that OfferListing maxRange decimal places is correct
    def test_offer_listing_max_range_decimals(self):
        offer_listing = self.offerListing
        decimal_places = offer_listing._meta.get_field('maxRange').decimal_places
        self.assertEqual(decimal_places, 2)

    #Checks to ensure that OfferListing maxRange verbose name is correct
    def test_offer_listing_max_range_verbose_name(self):
        offer_listing = self.offerListing
        verbose_name = offer_listing._meta.get_field('maxRange').verbose_name
        self.assertEqual(verbose_name, "Maximum Price Range")

    #Checks to ensure that OfferListing maxRange help text is correct
    def test_offer_listing_max_range_help_text(self):
        offer_listing = self.offerListing
        help_text = offer_listing._meta.get_field('maxRange').help_text
        self.assertEqual(help_text, "Maximum money offers you'll consider (leave blank if you don't have a maximum).")

    #Checks to ensure that OfferListing notes max length is correct
    def test_offer_listing_notes_max_length(self):
        offer_listing = self.offerListing
        max_length = offer_listing._meta.get_field('notes').max_length
        self.assertEqual(max_length, 500)

    #Checks to ensure that OfferListing notes help text is correct
    def test_offer_listing_notes_help_text(self):
        offer_listing = self.offerListing
        help_text = offer_listing._meta.get_field('notes').help_text
        self.assertEqual(help_text, "Include here what offers you're seeking.")

    #Checks to ensure that AuctionListing startingBid max digits is correct
    def test_auction_listing_starting_bid_digits(self):
        auction_listing = self.auctionListing
        max_digits = auction_listing._meta.get_field('startingBid').max_digits
        self.assertEqual(max_digits, 9)

    #Checks to ensure that AuctionListing startingBid decimal places is correct
    def test_auction_listing_starting_bid_decimals(self):
        auction_listing = self.auctionListing
        decimal_places = auction_listing._meta.get_field('startingBid').decimal_places
        self.assertEqual(decimal_places, 2)

    #Checks to ensure that AuctionListing startingBid verbose name is correct
    def test_auction_listing_starting_bid_verbose_name(self):
        auction_listing = self.auctionListing
        verbose_name = auction_listing._meta.get_field('startingBid').verbose_name
        self.assertEqual(verbose_name, "Starting Bid")

    #Checks to ensure that AuctionListing startingBid help text is correct
    def test_auction_listing_starting_bid_help_text(self):
        auction_listing = self.auctionListing
        help_text = auction_listing._meta.get_field('startingBid').help_text
        self.assertEqual(help_text, "Money amount bidding should start at for auction.")

    #Checks to ensure that AuctionListing minimumIncrement max digits is correct
    def test_auction_listing_minimum_increment_digits(self):
        auction_listing = self.auctionListing
        max_digits = auction_listing._meta.get_field('minimumIncrement').max_digits
        self.assertEqual(max_digits, 9)

    #Checks to ensure that AuctionListing minimumIncrement decimal places is correct
    def test_auction_listing_minimum_increment_decimals(self):
        auction_listing = self.auctionListing
        decimal_places = auction_listing._meta.get_field('minimumIncrement').decimal_places
        self.assertEqual(decimal_places, 2)

    #Checks to ensure that AuctionListing minimumIncrement verbose name is correct
    def test_auction_listing_minimum_increment_verbose_name(self):
        auction_listing = self.auctionListing
        verbose_name = auction_listing._meta.get_field('minimumIncrement').verbose_name
        self.assertEqual(verbose_name, "Minimum Increment")

    #Checks to ensure that AuctionListing minimumIncrement help text is correct
    def test_auction_listing_minimum_increment_help_text(self):
        auction_listing = self.auctionListing
        help_text = auction_listing._meta.get_field('minimumIncrement').help_text
        self.assertEqual(help_text, "Minimum increment bid that can be placed on the auction, that cannot be greater than the starting bid (maximum increment bid will be x3 this value).")

    #Checks to ensure that AuctionListing autobuy max digits is correct
    def test_auction_listing_autobuy_digits(self):
        auction_listing = self.auctionListing
        max_digits = auction_listing._meta.get_field('autobuy').max_digits
        self.assertEqual(max_digits, 9)

    #Checks to ensure that AuctionListing autobuy decimal places is correct
    def test_auction_listing_autobuy_decimals(self):
        auction_listing = self.auctionListing
        decimal_places = auction_listing._meta.get_field('autobuy').decimal_places
        self.assertEqual(decimal_places, 2)

    #Checks to ensure that AuctionListing autobuy help text is correct
    def test_auction_listing_autobuy_help_text(self):
        auction_listing = self.auctionListing
        help_text = auction_listing._meta.get_field('autobuy').help_text
        self.assertEqual(help_text, "If a user bids the amount you set in this field, the auction will close and they will win the auction.")

#Tests for SearchListing subclass

#Tests for Offer class
class OfferModelTest(MyTestCase):
    def setUp(self):
        #Set up records for Offer for testing
        super(OfferModelTest, self).setUp()
        self.offer = Offer.objects.create(offerListing=self.global_offer_listing,
            owner=self.global_user2, amount=5.00)
        self.offer.items.add(self.global_item)
        self.offer.save

    #Checks to ensure that Offer items field help text is correct
    def test_offer_items_help_text(self):
        offer = self.offer
        help_text = offer._meta.get_field('items').help_text
        self.assertEqual(help_text, "Items you'd like to offer on listing (do not select anything if you do not wanna offer items).")

    #Checks to ensure that Offer amount field verbose name is correct
    def test_offer_amount_verbose_name(self):
        offer = self.offer
        verbose_name = offer._meta.get_field('amount').verbose_name
        self.assertEqual(verbose_name, "Cash Offer")

    #Checks to ensure that Offer amount field help text is correct
    def test_offer_amount_help_text(self):
        offer = self.offer
        help_text = offer._meta.get_field('amount').help_text
        self.assertEqual(help_text, "Amount of cash you'd like to offer on listing (leave blank if you do not want to offer cash).")

    #Checks to ensure that Offer amount max digits is correct
    def test_offer_amount_max_digits(self):
        offer = self.offer
        max_digits = offer._meta.get_field('amount').max_digits
        self.assertEqual(max_digits, 9)

    #Checks to ensure that Offer amount decimal places is correct
    def test_offer_amount_decimals(self):
        offer = self.offer
        decimal_places = offer._meta.get_field('amount').decimal_places
        self.assertEqual(decimal_places, 2)

#Tests for Bid class
class BidModelTest(MyTestCase):
    def setUp(self):
        #Set up records for Offer for testing
        super(BidModelTest, self).setUp()
        self.bid = Bid.objects.create(auctionListing=self.global_auction_listing,
            bidder=self.global_user2, amount=5.00, winningBid=False)

    #Checks to ensure that Auction amount field help text is correct
    def test_bid_amount_help_text(self):
        bid = self.bid
        help_text = bid._meta.get_field('amount').help_text
        self.assertEqual(help_text, "Amount of cash you'd like to bid on listing (Cannot be more than 3x the minimum bid value).")

    #Checks to ensure that Auction amount field max digits is correct
    def test_bid_amount_max_digits(self):
        bid = self.bid
        max_digits = bid._meta.get_field('amount').max_digits
        self.assertEqual(max_digits, 9)

    #Checks to ensure that Auction amount field decimal places is correct
    def test_bid_amount_decimal_places(self):
        bid = self.bid
        decimal_places = bid._meta.get_field('amount').decimal_places
        self.assertEqual(decimal_places, 2)

    #Checks to ensure that Auction winningBid field defaults to false
    #Checks to ensure that Auction amount field decimal places is correct
    def test_bid_winning_bid_default(self):
        bid = self.bid
        default = bid._meta.get_field('winningBid').default
        self.assertEqual(default, False)

#Tests for Favorites class

#Tests for Receipts class
