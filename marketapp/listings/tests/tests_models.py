from django.test import TestCase
from listings.models import User, Admin

# Create your tests here.
#Tests for User class
class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Create a record of User for testing
        User.objects.create(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

    #Checks to ensure that an email max length is 100
    def text_email_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('email').max_length
        self.assertEquals(max_length, 100)

    #Checks to ensure that an email must not be blank
    def text_email_blank(self):
        user = User.objects.get(id=1)
        blank = user._meta.get_field('email').blank
        self.assertEquals(blank, False)

    #Checks to ensure that an email must be unique
    def text_email_unique(self):
        user = User.objects.get(id=1)
        unique = user._meta.get_field('email').unique
        self.assertEquals(unique, True)

    #Checks to ensure that the paypalEmail field verbose text is correct
    def test_paypal_email_label(self):
        user = User.objects.get(id=2)
        field_label = user._meta.get_field('paypalEmail').verbose_name
        self.assertEquals(field_label, 'Paypal Email')

    #Checks to ensure that an paypal email max length is 100
    def test_paypal_email_length(self):
        user = User.objects.get(id=2)
        max_length = user._meta.get_field('paypalEmail').max_length
        self.assertEquals(max_length, 100)

    #Checks to ensure that the paypalEmail field help text is correct
    def test_paypal_email_help_text(self):
        user = User.objects.get(id=2)
        help_text = user._meta.get_field('paypalEmail').help_text
        self.assertEquals(help_text, 'E-mail that is connected to your PayPal account')

    #Checks to ensure that an paypalEmail must not be blank
    def text_paypal_email_blank(self):
        user = User.objects.get(id=2)
        blank = user._meta.get_field('paypalEmail').blank
        self.assertEquals(blank, False)

    #Checks to ensure that an paypaLEmail must be unique
    def text_paypal_email_unique(self):
        user = User.objects.get(id=2)
        unique = user._meta.get_field('paypalEmail').unique
        self.assertEquals(unique, True)

    #Checks to ensure that invitesOpen defaults to true
    def test_invites_open_default(self):
        user = User.objects.get(id=2)
        default = user._meta.get_field('invitesOpen').default
        self.assertEquals(default, True)

    #Checks to ensure that the invitesOpen field verbose text is correct
    def test_invites_open_label(self):
        user = User.objects.get(id=2)
        field_label = user._meta.get_field('invitesOpen').verbose_name
        self.assertEquals(field_label, 'Allow Invites for Events')

    #Checks to ensure that the invitesOpen field help text is correct
    def test_invites_open_help_text(self):
        user = User.objects.get(id=2)
        help_text = user._meta.get_field('invitesOpen').help_text
        self.assertEquals(help_text, 'Leave this field checked if you are interested in being invited to events.')

    #Checks to ensure that invitesOpen defaults to true
    def test_inquiries_open_default(self):
        user = User.objects.get(id=2)
        default = user._meta.get_field('inquiriesOpen').default
        self.assertEquals(default, True)

    #Checks to ensure that the inquiriesOpen field verbose text is correct
    def test_invites_open_label(self):
        user = User.objects.get(id=2)
        field_label = user._meta.get_field('inquiriesOpen').verbose_name
        self.assertEquals(field_label, 'Allow Users to Contact You Through Profile')

    #Checks to ensure that the inquiriesOpen field help text is correct
    def test_invites_open_help_text(self):
        user = User.objects.get(id=2)
        help_text = user._meta.get_field('inquiriesOpen').help_text
        self.assertEquals(help_text, 'Leave this field checked if you are interested in being contacted by users through your profile.  If unchecked, users will only be able to contact you after you accept their offer or bid or you contact them.')

#Tests for Admin class
class AdminModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Create a record of User for testing
        Admin.objects.create(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            superAdmin=True, handleListings=True,
            handleEvents=True, handleWishlists=True, handleImages=True,
            handleRatings=True)

    #Checks to ensure that superAdmin defaults to False
    def test_super_admin_default(self):
        admin = Admin.objects.get(id=1)
        default = admin._meta.get_field('superAdmin').default
        self.assertEquals(default, False)

    #Checks to ensure that the superAdmin field verbose text is correct
    def test_super_admin_label(self):
        admin = Admin.objects.get(id=1)
        field_label = admin._meta.get_field('superAdmin').verbose_name
        self.assertEquals(field_label, 'Super Admin')

    #Checks to ensure that the superAdmin field help text is correct
    def test_super_admin_help_text(self):
        admin = Admin.objects.get(id=1)
        help_text = admin._meta.get_field('superAdmin').help_text
        self.assertEquals(help_text, 'Admin that is able to set, remove and configure other Admin accounts.')

    #Checks to ensure that handleListings defaults to False
    def test_handle_listings_default(self):
        admin = Admin.objects.get(id=1)
        default = admin._meta.get_field('handleListings').default
        self.assertEquals(default, False)

    #Checks to ensure that the handleListings field verbose text is correct
    def test_handle_listings_label(self):
        admin = Admin.objects.get(id=1)
        field_label = admin._meta.get_field('handleListings').verbose_name
        self.assertEquals(field_label, 'Can Handle Listings')

    #Checks to ensure that the handleListings field help text is correct
    def test_handle_listings_help_text(self):
        admin = Admin.objects.get(id=1)
        help_text = admin._meta.get_field('handleListings').help_text
        self.assertEquals(help_text, 'Admin is able to manage user listings.')

    #Checks to ensure that handleEvents defaults to False
    def test_handle_events_default(self):
        admin = Admin.objects.get(id=1)
        default = admin._meta.get_field('handleEvents').default
        self.assertEquals(default, False)

    #Checks to ensure that the handleEvents field verbose text is correct
    def test_handle_events_label(self):
        admin = Admin.objects.get(id=1)
        field_label = admin._meta.get_field('handleEvents').verbose_name
        self.assertEquals(field_label, 'Can Handle Events')

    #Checks to ensure that the handleEvents field help text is correct
    def test_handle_events_help_text(self):
        admin = Admin.objects.get(id=1)
        help_text = admin._meta.get_field('handleEvents').help_text
        self.assertEquals(help_text, 'Admin is able to manage user events.')

    #Checks to ensure that handleWishlists defaults to False
    def test_handle_wishlists_default(self):
        admin = Admin.objects.get(id=1)
        default = admin._meta.get_field('handleWishlists').default
        self.assertEquals(default, False)

    #Checks to ensure that the handleWishlists field verbose text is correct
    def test_handle_wishlists_label(self):
        admin = Admin.objects.get(id=1)
        field_label = admin._meta.get_field('handleWishlists').verbose_name
        self.assertEquals(field_label, 'Can Handle Wishlists')

    #Checks to ensure that the handleWishlists field help text is correct
    def test_handle_wishlists_help_text(self):
        admin = Admin.objects.get(id=1)
        help_text = admin._meta.get_field('handleWishlists').help_text
        self.assertEquals(help_text, 'Admin is able to manage user wishlists.')

    #Checks to ensure that handleImages defaults to False
    def test_handle_images_default(self):
        admin = Admin.objects.get(id=1)
        default = admin._meta.get_field('handleImages').default
        self.assertEquals(default, False)

    #Checks to ensure that the handleImages field verbose text is correct
    def test_handle_images_label(self):
        admin = Admin.objects.get(id=1)
        field_label = admin._meta.get_field('handleImages').verbose_name
        self.assertEquals(field_label, 'Can Handle Images')

    #Checks to ensure that the handleWishlists field help text is correct
    def test_handle_images_help_text(self):
        admin = Admin.objects.get(id=1)
        help_text = admin._meta.get_field('handleImages').help_text
        self.assertEquals(help_text, 'Admin is able to manage user images.')

    #Checks to ensure that handleRatings defaults to False
    def test_handle_ratings_default(self):
        admin = Admin.objects.get(id=1)
        default = admin._meta.get_field('handleRatings').default
        self.assertEquals(default, False)

    #Checks to ensure that the handleImages field verbose text is correct
    def test_handle_ratings_label(self):
        admin = Admin.objects.get(id=1)
        field_label = admin._meta.get_field('handleRatings').verbose_name
        self.assertEquals(field_label, 'Can Handle Ratings')

    #Checks to ensure that the handleWishlists field help text is correct
    def test_handle_ratings_help_text(self):
        admin = Admin.objects.get(id=1)
        help_text = admin._meta.get_field('handleRatings').help_text
        self.assertEquals(help_text, 'Admin is able to manage user ratings.')
