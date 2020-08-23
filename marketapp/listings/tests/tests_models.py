from django.test import TestCase
from listings.models import (User, Admin, Profile, Rating, Warning, Conversation,
    Message, Image, Tag, Wishlist, WishlistItem)
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.
class MyTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True) #profile is created when the user is created
        admin = Admin.objects.create(username="mike2", password="example",
            email="example2@text.com", paypalEmail="example2@text.com",
            superAdmin=True, handleListings=True,
            handleEvents=True, handleWishlists=True, handleImages=True,
            handleRatings=True)
        user2 = User.objects.create(username="mike3", password="example",
            email="example3@text.com", paypalEmail="example3@text.com",
            invitesOpen=True, inquiriesOpen=True)
        self.global_user1 = user1
        self.global_admin = admin
        self.global_user2 = user2
        test_image = SimpleUploadedFile(name='art1.png', content=open('listings/imagetest/art1.png', 'rb').read(), content_type='image/png')
        self.global_image = Image.objects.create(owner=self.global_user1,
            image=test_image, name="Test Image")
        self.tag = Tag.objects.create(name="Test Tag")
        self.global_image.tags.add(self.tag)
        self.global_image.save

#Tests for User class
class UserModelTest(MyTestCase):

    #Checks to ensure that an email max length is 100
    def text_email_length(self):
        user = self.global_user1
        max_length = user._meta.get_field('email').max_length
        self.assertEquals(max_length, 100)

    #Checks to ensure that an email must not be blank
    def text_email_blank(self):
        user = self.global_user1
        blank = user._meta.get_field('email').blank
        self.assertEquals(blank, False)

    #Checks to ensure that an email must be unique
    def text_email_unique(self):
        user = self.global_user1
        unique = user._meta.get_field('email').unique
        self.assertEquals(unique, True)

    #Checks to ensure that the paypalEmail field verbose text is correct
    def test_paypal_email_label(self):
        user = self.global_user1
        field_label = user._meta.get_field('paypalEmail').verbose_name
        self.assertEquals(field_label, 'Paypal Email')

    #Checks to ensure that an paypal email max length is 100
    def test_paypal_email_length(self):
        user = self.global_user1
        max_length = user._meta.get_field('paypalEmail').max_length
        self.assertEquals(max_length, 100)

    #Checks to ensure that the paypalEmail field help text is correct
    def test_paypal_email_help_text(self):
        user = self.global_user1
        help_text = user._meta.get_field('paypalEmail').help_text
        self.assertEquals(help_text, 'E-mail that is connected to your PayPal account')

    #Checks to ensure that an paypalEmail must not be blank
    def text_paypal_email_blank(self):
        user = self.global_user1
        blank = user._meta.get_field('paypalEmail').blank
        self.assertEquals(blank, False)

    #Checks to ensure that an paypaLEmail must be unique
    def text_paypal_email_unique(self):
        user = self.global_user1
        unique = user._meta.get_field('paypalEmail').unique
        self.assertEquals(unique, True)

    #Checks to ensure that invitesOpen defaults to true
    def test_invites_open_default(self):
        user = self.global_user1
        default = user._meta.get_field('invitesOpen').default
        self.assertEquals(default, True)

    #Checks to ensure that the invitesOpen field verbose text is correct
    def test_invites_open_label(self):
        user = self.global_user1
        field_label = user._meta.get_field('invitesOpen').verbose_name
        self.assertEquals(field_label, 'Allow Invites for Events')

    #Checks to ensure that the invitesOpen field help text is correct
    def test_invites_open_help_text(self):
        user = self.global_user1
        help_text = user._meta.get_field('invitesOpen').help_text
        self.assertEquals(help_text, 'Leave this field checked if you are interested in being invited to events.')

    #Checks to ensure that invitesOpen defaults to true
    def test_inquiries_open_default(self):
        user = self.global_user1
        default = user._meta.get_field('inquiriesOpen').default
        self.assertEquals(default, True)

    #Checks to ensure that the inquiriesOpen field verbose text is correct
    def test_invites_open_label(self):
        user = self.global_user1
        field_label = user._meta.get_field('inquiriesOpen').verbose_name
        self.assertEquals(field_label, 'Allow Users to Contact You Through Profile')

    #Checks to ensure that the inquiriesOpen field help text is correct
    def test_invites_open_help_text(self):
        user = self.global_user1
        help_text = user._meta.get_field('inquiriesOpen').help_text
        self.assertEquals(help_text, 'Leave this field checked if you are interested in being contacted by users through your profile.  If unchecked, users will only be able to contact you after you accept their offer or bid or you contact them.')

#Tests for Admin class
class AdminModelTest(MyTestCase):

    #Checks to ensure that superAdmin defaults to False
    def test_super_admin_default(self):
        admin = self.global_admin
        default = admin._meta.get_field('superAdmin').default
        self.assertEquals(default, False)

    #Checks to ensure that the superAdmin field verbose text is correct
    def test_super_admin_label(self):
        admin = self.global_admin
        field_label = admin._meta.get_field('superAdmin').verbose_name
        self.assertEquals(field_label, 'Super Admin')

    #Checks to ensure that the superAdmin field help text is correct
    def test_super_admin_help_text(self):
        admin = self.global_admin
        help_text = admin._meta.get_field('superAdmin').help_text
        self.assertEquals(help_text, 'Admin that is able to set, remove and configure other Admin accounts.')

    #Checks to ensure that handleListings defaults to False
    def test_handle_listings_default(self):
        admin = self.global_admin
        default = admin._meta.get_field('handleListings').default
        self.assertEquals(default, False)

    #Checks to ensure that the handleListings field verbose text is correct
    def test_handle_listings_label(self):
        admin = self.global_admin
        field_label = admin._meta.get_field('handleListings').verbose_name
        self.assertEquals(field_label, 'Can Handle Listings')

    #Checks to ensure that the handleListings field help text is correct
    def test_handle_listings_help_text(self):
        admin = self.global_admin
        help_text = admin._meta.get_field('handleListings').help_text
        self.assertEquals(help_text, 'Admin is able to manage user listings.')

    #Checks to ensure that handleEvents defaults to False
    def test_handle_events_default(self):
        admin = self.global_admin
        default = admin._meta.get_field('handleEvents').default
        self.assertEquals(default, False)

    #Checks to ensure that the handleEvents field verbose text is correct
    def test_handle_events_label(self):
        admin = self.global_admin
        field_label = admin._meta.get_field('handleEvents').verbose_name
        self.assertEquals(field_label, 'Can Handle Events')

    #Checks to ensure that the handleEvents field help text is correct
    def test_handle_events_help_text(self):
        admin = self.global_admin
        help_text = admin._meta.get_field('handleEvents').help_text
        self.assertEquals(help_text, 'Admin is able to manage user events.')

    #Checks to ensure that handleWishlists defaults to False
    def test_handle_wishlists_default(self):
        admin = self.global_admin
        default = admin._meta.get_field('handleWishlists').default
        self.assertEquals(default, False)

    #Checks to ensure that the handleWishlists field verbose text is correct
    def test_handle_wishlists_label(self):
        admin = self.global_admin
        field_label = admin._meta.get_field('handleWishlists').verbose_name
        self.assertEquals(field_label, 'Can Handle Wishlists')

    #Checks to ensure that the handleWishlists field help text is correct
    def test_handle_wishlists_help_text(self):
        admin = self.global_admin
        help_text = admin._meta.get_field('handleWishlists').help_text
        self.assertEquals(help_text, 'Admin is able to manage user wishlists.')

    #Checks to ensure that handleImages defaults to False
    def test_handle_images_default(self):
        admin = self.global_admin
        default = admin._meta.get_field('handleImages').default
        self.assertEquals(default, False)

    #Checks to ensure that the handleImages field verbose text is correct
    def test_handle_images_label(self):
        admin = self.global_admin
        field_label = admin._meta.get_field('handleImages').verbose_name
        self.assertEquals(field_label, 'Can Handle Images')

    #Checks to ensure that the handleWishlists field help text is correct
    def test_handle_images_help_text(self):
        admin = self.global_admin
        help_text = admin._meta.get_field('handleImages').help_text
        self.assertEquals(help_text, 'Admin is able to manage user images.')

    #Checks to ensure that handleRatings defaults to False
    def test_handle_ratings_default(self):
        admin = self.global_admin
        default = admin._meta.get_field('handleRatings').default
        self.assertEquals(default, False)

    #Checks to ensure that the handleImages field verbose text is correct
    def test_handle_ratings_label(self):
        admin = self.global_admin
        field_label = admin._meta.get_field('handleRatings').verbose_name
        self.assertEquals(field_label, 'Can Handle Ratings')

    #Checks to ensure that the handleWishlists field help text is correct
    def test_handle_ratings_help_text(self):
        admin = self.global_admin
        help_text = admin._meta.get_field('handleRatings').help_text
        self.assertEquals(help_text, 'Admin is able to manage user ratings.')

#Tests for Profile Class
class ProfileModelTest(MyTestCase):

    #Checks to ensure that bio has a max length of 1000
    def test_bio_max_length(self):
        profile = self.global_user1.profile
        max_length = profile._meta.get_field('bio').max_length
        self.assertEquals(max_length, 1000)

    #Checks to ensure that the bio field verbose text is correct
    def test_bio_label(self):
        profile = self.global_user1.profile
        field_label = profile._meta.get_field('bio').verbose_name
        self.assertEquals(field_label, "Biography")

    #Checks to ensure that the bio field help text is correct
    def test_bio_help_text(self):
        profile = self.global_user1.profile
        help_text = profile._meta.get_field('bio').help_text
        self.assertEquals(help_text, "A biography for your profile so others can know you better.")

    #Checks to ensure that name has a max length of 50
    def test_name_max_length(self):
        profile = self.global_user1.profile
        max_length = profile._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    #Checks to ensure that the name field verbose text is correct
    def test_name_label(self):
        profile = self.global_user1.profile
        field_label = profile._meta.get_field('name').verbose_name
        self.assertEquals(field_label, "Full Name")

    #Checks to ensure that name has a max length of 50
    def test_name_max_length(self):
        profile = self.global_user1.profile
        max_length = profile._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    #Checks to ensure that the name field verbose text is correct
    def test_name_label(self):
        profile = self.global_user1.profile
        field_label = profile._meta.get_field('name').verbose_name
        self.assertEquals(field_label, "Full Name")

    #Checks to ensure that country has a max length of 50
    def test_country_length(self):
        profile = self.global_user1.profile
        max_length = profile._meta.get_field('country').max_length
        self.assertEquals(max_length, 50)

    #Checks to ensure that state has a max length of 50
    def test_state_length(self):
        profile = self.global_user1.profile
        max_length = profile._meta.get_field('state').max_length
        self.assertEquals(max_length, 50)

    #Checks to ensure that city has a max length of 50
    def test_city_length(self):
        profile = self.global_user1.profile
        max_length = profile._meta.get_field('city').max_length
        self.assertEquals(max_length, 50)

    #Checks to ensure that zipCode has a max length of 50
    def test_zip_code_max_length(self):
        profile = self.global_user1.profile
        max_length = profile._meta.get_field('zipCode').max_length
        self.assertEquals(max_length, 10)

    #Checks to ensure that the zipCode field verbose text is correct
    def test_zip_code_label(self):
        profile = self.global_user1.profile
        field_label = profile._meta.get_field('zipCode').verbose_name
        self.assertEquals(field_label, "Zip Code")

    #Checks to ensure that the delivery field help text is correct
    def test_delivery_help_text(self):
        profile = self.global_user1.profile
        help_text = profile._meta.get_field('delivery').help_text
        self.assertEquals(help_text, "Check this if you are able to deliver items.")

    #Checks to ensure that deliveryAddress has a max length of 50
    def test_delivery_address_max_length(self):
        profile = self.global_user1.profile
        max_length = profile._meta.get_field('deliveryAddress').max_length
        self.assertEquals(max_length, 100)

    #Checks to ensure that the deliveryAddress field verbose text is correct
    def test_delivery_address_label(self):
        profile = self.global_user1.profile
        field_label = profile._meta.get_field('deliveryAddress').verbose_name
        self.assertEquals(field_label, "Delivery Address")

    #Checks to ensure that the deliveryAddress field help text is correct
    def test_delivery_address_help_text(self):
        profile = self.global_user1.profile
        help_text = profile._meta.get_field('deliveryAddress').help_text
        self.assertEquals(help_text, "Submit an delivery address that you pick up items from.")

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
        self.assertEquals(verbose_text, "Rating")

    #Checks to ensure that the ratingValue field help text is correct
    def test_rating_value_help_text(self):
        rating = self.rating
        help_text = rating._meta.get_field('ratingValue').help_text
        self.assertEquals(help_text, "Rating for user from 1 to 5, 5 being the best.")

    #Checks to ensure that the feedback field help text is correct
    def test_feedback_help_text(self):
        rating = self.rating
        help_text = rating._meta.get_field('feedback').help_text
        self.assertEquals(help_text, "Leave feedback for the user you're rating.")

#Tests for Warning Class
class WarningModelTest(MyTestCase):
    def setUp(self):
        #Set up warning record for testing
        super(WarningModelTest, self).setUp()
        self.warning = Warning.objects.create(user=self.global_user1, admin=self.global_admin,
            warningCount=1, reason="For testing", actionsTaken="None")

    #Checks to ensure that warningCount field verbose text is correct
    def test_warning_count_label(self):
        warning = self.warning
        field_label = warning._meta.get_field('warningCount').verbose_name
        self.assertEquals(field_label, "Warning Count")

    #Checks to ensure that reason field length is correct
    def test_reason_max_length(self):
        warning = self.warning
        max_length = warning._meta.get_field('reason').max_length
        self.assertEquals(max_length, 250)

    #Checks to ensure that reason field verbose text is correct
    def test_reason_label(self):
        warning = self.warning
        field_label = warning._meta.get_field('reason').verbose_name
        self.assertEquals(field_label, "Reason for Warning")

    #Checks to ensure that the reason field help text is correct
    def test_reason_help_text(self):
        warning = self.warning
        help_text = warning._meta.get_field('reason').help_text
        self.assertEquals(help_text, "Submit reasoning for why you warned this user.")

    #Checks to ensure that actionsTaken length is correct
    def test_actions_taken_max_length(self):
        warning = self.warning
        max_length = warning._meta.get_field('actionsTaken').max_length
        self.assertEquals(max_length, 500)

    #Checks to ensure that actionsTaken field verbose text is correct
    def test_actions_taken_label(self):
        warning = self.warning
        field_label = warning._meta.get_field('actionsTaken').verbose_name
        self.assertEquals(field_label, "Actions Taken")

    #Checks to ensure that the actionsTaken field help text is correct
    def test_actions_taken_help_text(self):
        warning = self.warning
        help_text = warning._meta.get_field('actionsTaken').help_text
        self.assertEquals(help_text, "What actions were made regarding this user?")

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
        self.assertEquals(max_length, 100)

    #Checks to ensure that topic field help text is correct
    def test_topic_help_text_length(self):
        conversation = self.conversation
        help_text = conversation._meta.get_field('topic').help_text
        self.assertEquals(help_text, "Topic of the Conversation")

    #Checks to ensure that unread field defaults to true
    def test_unread_eaault(self):
        conversation = self.conversation
        default = conversation._meta.get_field('unread').default
        self.assertEquals(default, True)

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
        self.assertEquals(max_length, 500)

    #Checks to ensure that dateSent field verbose text is correct
    def test_date_sent_label(self):
        message = self.message
        field_label = message._meta.get_field('dateSent').verbose_name
        self.assertEquals(field_label, "Date Sent")

#Tests for Image Class
class ImageAndTagsModelTest(MyTestCase):
    #Checks to ensure that Image name length is correct
    def test_image_name_max_length(self):
        image = self.global_image
        max_length = image._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    #Checks to ensure that name field for Image verbose text is correct
    def test_image_name_label(self):
        image = self.global_image
        verbose_name = image._meta.get_field('name').verbose_name
        self.assertEquals(verbose_name, "Name of Image")

    #Checks to ensure that tags field verbose text is correct
    def test_image_tag_label(self):
        image = self.global_image
        verbose_name = image._meta.get_field('tags').verbose_name
        self.assertEquals(verbose_name, "Item Tags")

    #Checks to ensure that tags field help text is correct
    def test_image_tag_help_text(self):
        image = self.global_image
        help_text = image._meta.get_field('tags').help_text
        self.assertEquals(help_text, "Qualities of the item in the photo, purpose and where one can find it can be used as tags.")

    #Checks to ensure that Tag name length is correct
    def test_tag_name_max_length(self):
        tag = self.tag
        max_length = tag._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    #Checks to ensure that name field for Tag verbose text is correct
    def test_image_name_label(self):
        tag = self.tag
        verbose_name = tag._meta.get_field('name').verbose_name
        self.assertEquals(verbose_name, "Tag Name")

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
        self.assertEquals(max_length, 50)

    #Checks to ensure that Wishlist description length is correct
    def test_wishlist_description_max_length(self):
        wishlist = self.wishlist
        max_length = wishlist._meta.get_field('description').max_length
        self.assertEquals(max_length, 250)

    #Checks to ensure that Wishlist description help text is correct
    def test_wishlist_description_max_length(self):
        wishlist = self.wishlist
        help_text = wishlist._meta.get_field('description').help_text
        self.assertEquals(help_text, "A brief description of your wishlist and what it contains.")

#Tests for WishlistItem Class
class WishlistItemModelTest(MyTestCase):
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
        self.assertEquals(max_length, 50)

    #Checks to ensure that WishlistItem name verbose text is correct
    def test_wishlist_item_name_label(self):
        wishlist_item = self.wishlist_item
        verbose_name = wishlist_item._meta.get_field('name').verbose_name
        self.assertEquals(verbose_name, "Item Name")

    #Checks to ensure that WishlistItem description length is correct
    def test_wishlist_item_description_max_length(self):
        wishlist_item = self.wishlist_item
        max_length = wishlist_item._meta.get_field('description').max_length
        self.assertEquals(max_length, 250)

    #Checks to ensure that WishlistItem name help text is correct
    def test_wishlist_item_description_help_text(self):
        wishlist_item = self.wishlist_item
        help_text = wishlist_item._meta.get_field('description').help_text
        self.assertEquals(help_text, "A brief description of the item in the image(s).")


#Tests for Event Class

#Tests for Report Class

#Tests for ListingReport subclass

#Tests for EventReport subclass

#Tests for UserReport subclass

#Tests for RatingReport subclass

#Tests for WishlistReport subclass

#Tests for ImageReport subclass

#Tests for Listing Class

#Tests for OfferListing subclass

#Tests for SearchListing subclass

#Tests for AuctionListing subclass

#Tests for Offer class

#Tests for Bid class

#Tests for Favorites class

#Tests for Receipts class
