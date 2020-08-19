from django.test import TestCase
from listings.models import User

# Create your tests here.
class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Create a record of User for testing
        user1 = User.objects.create(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)
        user1

    #Checks to ensure that an email max length is 100
    def text_email_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('email').max_length
        self.assertEquals(max_length, 100)

    #Checks to ensure that the paypalEmail field verbose text is correct
    def test_paypal_email_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('paypalEmail').verbose_name
        self.assertEquals(field_label, 'Paypal Email')

    #Checks to ensure that an paypal email max length is 100
    def test_paypal_email_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('paypalEmail').max_length
        self.assertEquals(max_length, 100)

    #Checks to ensure that the paypalEmail field help text is correct
    def test_paypal_email_help_text(self):
        user = User.objects.get(id=1)
        help_text = user._meta.get_field('paypalEmail').help_text
        self.assertEquals(help_text, 'E-mail that is connected to your PayPal account')

    #Checks to ensure that invitesOpen defaults to true
    def test_invites_open_default(self):
        user = User.objects.get(id=1)
        default = user._meta.get_field('invitesOpen').default
        self.assertEquals(default, True)

    #Checks to ensure that the invitesOpen field verbose text is correct
    def test_invites_open_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('invitesOpen').verbose_name
        self.assertEquals(field_label, 'Allow Invites for Events')

    #Checks to ensure that the invitesOpen field help text is correct
    def test_invites_open_help_text(self):
        user = User.objects.get(id=1)
        help_text = user._meta.get_field('invitesOpen').help_text
        self.assertEquals(help_text, 'Leave this field checked if you are interested in being invited to events.')

    #Checks to ensure that invitesOpen defaults to true
    def test_inquiries_open_default(self):
        user = User.objects.get(id=1)
        default = user._meta.get_field('inquiriesOpen').default
        self.assertEquals(default, True)

    #Checks to ensure that the inquiriesOpen field verbose text is correct
    def test_invites_open_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('inquiriesOpen').verbose_name
        self.assertEquals(field_label, 'Allow Users to Contact You Through Profile')

    #Checks to ensure that the inquiriesOpen field help text is correct
    def test_invites_open_help_text(self):
        user = User.objects.get(id=1)
        help_text = user._meta.get_field('inquiriesOpen').help_text
        self.assertEquals(help_text, 'Leave this field checked if you are interested in being contacted by users through your profile.  If unchecked, users will only be able to contact you after you accept their offer or bid or you contact them.')
