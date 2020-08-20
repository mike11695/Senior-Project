from django.test import TestCase
from listings.models import User, Admin, Profile, Rating

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

#Tests for Profile Class
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
