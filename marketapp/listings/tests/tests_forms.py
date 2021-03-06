from django.test import TestCase
from listings.forms import (SignUpForm, AddImageForm, ItemForm, OfferListingForm,
    AuctionListingForm, OfferForm, CreateBidForm, EventForm, InvitationForm,
    WishlistForm, WishlistListingForm, ProfileForm, EditAccountForm,
    ConversationForm, MessageForm, ListingReportForm, EventReportForm,
    UserReportForm, WishlistReportForm, ImageReportForm, CreateRatingForm,
    RatingReportForm, TakeActionOnReportForm)
from django.core.files.uploadedfile import SimpleUploadedFile
from listings.models import (User, Image, Tag, Item, Listing, OfferListing,
    AuctionListing, Offer, Bid, Event, Invitation, Wishlist, Rating,
    RatingTicket, ListingReport, EventReport, RatingReport, UserReport,
    WishlistReport, ImageReport, RatingReport)

from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import make_aware
from django.conf import settings

# Create your tests here.
class MyTestCase(TestCase):
    def setUp(self):
        #Create global users for testing
        user1 = User.objects.create_user(username="mike2", password="example",
            email="example4@text.com", paypalEmail="example4@text.com",
            invitesOpen=True, inquiriesOpen=True) #profile is created when the user is created
        user2 = User.objects.create_user(username="mike3", password="example",
            email="example3@text.com", paypalEmail="example3@text.com",
            invitesOpen=True, inquiriesOpen=True)
        self.global_user1 = user1
        self.global_user2 = user2

        #Greate global images and a tag for testing
        test_image1 = SimpleUploadedFile(name='art1.png', content=open('listings/imagetest/art1.png', 'rb').read(), content_type='image/png')
        self.global_image1 = Image.objects.create(owner=self.global_user1,
            image=test_image1, name="Test Image")
        self.tag = Tag.objects.create(name="Test Tag")
        self.global_image1.tags.add(self.tag)
        self.global_image1.save
        test_image2 = SimpleUploadedFile(name='art2.png', content=open('listings/imagetest/art2.png', 'rb').read(), content_type='image/png')
        self.global_image2 = Image.objects.create(owner=self.global_user1,
            image=test_image2, name="Test Image 2")
        self.global_image2.tags.add(self.tag)
        self.global_image2.save
        self.global_test_image1 = test_image1
        self.global_test_image2 = test_image2

        #Create a global item for each user for testing
        self.global_item1 = Item.objects.create(name="Global Item",
            description="A global item for testing", owner=self.global_user1)
        self.global_item1.images.add(self.global_image1)
        self.global_item1.save
        self.global_item2 = Item.objects.create(name="Global Item 2",
            description="Another global item for testing", owner=self.global_user2)
        self.global_item2.images.add(self.global_image2)
        self.global_item2.save
        self.global_non_wishlist_item = Item.objects.create(name="Global Item",
            description="A global item not in wishlist for testing", owner=self.global_user1)
        self.global_non_wishlist_item.images.add(self.global_image1)
        self.global_non_wishlist_item.save

        #Create a global wishlist
        self.global_wishlist = Wishlist.objects.create(owner=self.global_user1,
            title="My Wishlist", description="Stuff I would love to trade for")
        self.global_wishlist.items.add(self.global_item1)
        self.global_wishlist.save

        #Get the current date and time for testing and create active and inactive endtimes
        date_ended = timezone.localtime(timezone.now()) - timedelta(hours=1)
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        #Create a global offer listing that is not active
        self.global_offer_listing1 = OfferListing.objects.create(owner=user1, name='Test Offer Listing',
            description="Just a test listing", openToMoneyOffers=True, minRange=5.00,
            maxRange=10.00, notes="Just offer", endTime=date_ended, latitude=40.0200, longitude=-75.0300)
        self.global_offer_listing1.items.add(self.global_item1)
        self.global_offer_listing1.save

        self.global_rating_ticket = RatingTicket.objects.create(rater=self.global_user2,
            receivingUser=self.global_user1, listing=self.global_offer_listing1)

#Tests for the form to sign up to List.it
class SignUpFormTest(TestCase):
    #Test to ensure a user is able to sign up providing all fields
    def test_valid_signup(self):
        username = "Mikael"
        password1 = "examplepassword8265"
        password2 = "examplepassword8265"
        email = "exampleEmail@gmail.com"
        paypalEmail = "examplePaypalEmail@gmail.com"
        first_name = "Michael"
        last_name = "Lopez"
        data = {'username': username, 'password1': password1, 'password2': password2,
            'email': email, 'paypalEmail': paypalEmail, 'first_name': first_name,
            'last_name': last_name
        }
        form = SignUpForm(data)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to sign up if paypalEmail is missing
    def test_invalid_paypal_email(self):
        username = "Mikael"
        password1 = "examplepassword8265"
        password2 = "examplepassword8265"
        email = "example@gmail.com"
        paypalEmail = "examplegmail.com"
        first_name = "Michael"
        last_name = "Lopez"
        data = {'username': username, 'password1': password1, 'password2': password2,
            'email': email, 'first_name': first_name, 'last_name': last_name
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to sign up if email is missing
    def test_invalid_email(self):
        username = "Mikael"
        password1 = "examplepassword8265"
        password2 = "examplepassword8265"
        email = "examplegmail.com"
        paypalEmail = "example@gmail.com"
        first_name = "Michael"
        last_name = "Lopez"
        data = {'username': username, 'password1': password1, 'password2': password2,
            'paypalEmail': paypalEmail, 'first_name': first_name, 'last_name': last_name
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to sign up if paypalEmail is too long
    def test_invalid_paypal_email_length(self):
        username = "Mikael"
        password1 = "examplepassword8265"
        password2 = "examplepassword8265"
        email = "example@gmail.com"
        paypalEmail = "exampleeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee@gmail.com"
        first_name = "Michael"
        last_name = "Lopez"
        data = {'username': username, 'password1': password1, 'password2': password2,
            'email': email, 'paypalEmail': paypalEmail, 'first_name': first_name,
            'last_name': last_name
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to sign up if email is too long
    def test_invalid_email_length(self):
        username = "Mikael"
        password1 = "examplepassword8265"
        password2 = "examplepassword8265"
        email = "exampleeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee@gmail.com"
        paypalEmail = "example@gmail.com"
        first_name = "Michael"
        last_name = "Lopez"
        data = {'username': username, 'password1': password1, 'password2': password2,
            'email': email, 'paypalEmail': paypalEmail, 'first_name': first_name,
            'last_name': last_name
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to sign up if first name is missing
    def test_first_name_required(self):
        username = "Mikael"
        password1 = "examplepassword8265"
        password2 = "examplepassword8265"
        email = "exampleEmail@gmail.com"
        paypalEmail = "examplePaypalEmail@gmail.com"
        last_name = "Lopez"
        data = {'username': username, 'password1': password1, 'password2': password2,
            'email': email, 'paypalEmail': paypalEmail, 'last_name': last_name
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to sign up if last name is missing
    def test_last_name_required(self):
        username = "Mikael"
        password1 = "examplepassword8265"
        password2 = "examplepassword8265"
        email = "exampleEmail@gmail.com"
        paypalEmail = "examplePaypalEmail@gmail.com"
        first_name = "Michael"
        data = {'username': username, 'password1': password1, 'password2': password2,
            'email': email, 'paypalEmail': paypalEmail, 'first_name': first_name
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to sign up if passwords don't match
    def test_passwords_must_match(self):
        username = "Mikael"
        password1 = "examplepassword8265"
        password2 = "examplepassword8266"
        email = "exampleEmail@gmail.com"
        paypalEmail = "examplePaypalEmail@gmail.com"
        first_name = "Michael"
        last_name = "Lopez"
        data = {'username': username, 'password1': password1, 'password2': password2,
            'email': email, 'paypalEmail': paypalEmail, 'first_name': first_name,
            'last_name': last_name
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

#Tests for the form to edit an account
class EditAccountFormTest(TestCase):
    #Test to ensure a user is able to edit account ptoviding all fields
    def test_valid_account_edit(self):
        paypal_email = "example@gmail.com"
        first_name = "Michael"
        last_name = "Lopez"
        invites_open = True
        inquiries_open = True
        data = {'paypalEmail': paypal_email, 'first_name': first_name,
            'last_name': last_name, 'invitesOpen': invites_open,
            'inquiriesOpen': inquiries_open
        }
        form = EditAccountForm(data)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to edit account if paypalEmail is missing
    def test_invalid_edit_missing_paypal_email(self):
        paypalEmail = "examplePaypalEmail@gmail.com"
        first_name = "Michael"
        last_name = "Lopez"
        invites_open = True
        inquiries_open = True
        data = {'first_name': first_name,
            'last_name': last_name, 'invitesOpen': invites_open,
            'inquiriesOpen': inquiries_open
        }
        form = EditAccountForm(data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to edit account if paypalEmail is too long
    def test_invalid_edit_paypal_email_too_long(self):
        paypalEmail = ("exampleeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee" +
            "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee" +
            "eeeeeeeeeeeeeeeeeeeeeeeeeeeee@gmail.com")
        first_name = "Michael"
        last_name = "Lopez"
        invites_open = True
        inquiries_open = True
        data = {'paypalEmail': paypalEmail, 'first_name': first_name,
            'last_name': last_name, 'invitesOpen': invites_open,
            'inquiriesOpen': inquiries_open
        }
        form = EditAccountForm(data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to edit account if first name is missing
    def test_first_name_required(self):
        paypalEmail = "examplePaypalEmail@gmail.com"
        first_name = "Michael"
        last_name = "Lopez"
        invites_open = True
        inquiries_open = True
        data = {'paypalEmail': paypalEmail, 'last_name': last_name,
            'invitesOpen': invites_open, 'inquiriesOpen': inquiries_open
        }
        form = EditAccountForm(data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to edit account if last name is missing
    def test_last_name_required(self):
        paypalEmail = "examplePaypalEmail@gmail.com"
        first_name = "Michael"
        last_name = "Lopez"
        invites_open = True
        inquiries_open = True
        data = {'paypalEmail': paypalEmail, 'first_name': first_name,
            'invitesOpen': invites_open, 'inquiriesOpen': inquiries_open
        }
        form = EditAccountForm(data)
        self.assertFalse(form.is_valid())

    #Test to ensure that invitesOpen field help text is correct
    def test_invites_open_help_text(self):
        form = EditAccountForm()
        self.assertEqual(form.fields['invitesOpen'].help_text, ("Check " +
            "if you want to be invited to events"))

    #Test to ensure that invitesOpen field label is correct
    def test_invites_open_label(self):
        form = EditAccountForm()
        self.assertEqual(form.fields['invitesOpen'].label,
            "Open to Invitations?")

    #Test to ensure that inquiriesOpen field help text is correct
    def test_inquiries_open_help_text(self):
        form = EditAccountForm()
        self.assertEqual(form.fields['inquiriesOpen'].help_text, ("Check " +
            "if you want users to message you"))

    #Test to ensure that inquiriesOpen field label is correct
    def test_inquiries_open_label(self):
        form = EditAccountForm()
        self.assertEqual(form.fields['inquiriesOpen'].label,
            "Open to Inquiries?")

#Tests for the form to upload an image
class AddImageFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Tag.objects.create(name="Test Tag")
        Tag.objects.create(name="Test Tag 2")

    #Test to ensure a user is able to upload an image providing all fields
    def test_valid_image_upload(self):
        image = SimpleUploadedFile(name='art1.png', content=open('listings/imagetest/art1.png', 'rb').read(), content_type='image/png')
        tag1 = Tag.objects.get(id=1)
        tag2 = Tag.objects.get(id=2)
        name = "My Image"
        data = {'name': name, 'tags': [str(tag1.id), str(tag2.id)]}
        form = AddImageForm(data, {'image': image})
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to upload an image if it's too large
    def test_invalid_image_upload_large_pic(self):
        image = SimpleUploadedFile(name='oversized.png', content=open('listings/imagetest/oversized.png', 'rb').read(), content_type='image/png')
        tag1 = Tag.objects.get(id=1)
        tag2 = Tag.objects.get(id=2)
        name = "My Image"
        data = {'name': name, 'tags': [str(tag1.id), str(tag2.id)]}
        form = AddImageForm(data, {'image': image})
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to upload an image if no image is provided
    def test_invalid_image_upload_missing_pic(self):
        tag1 = Tag.objects.get(id=1)
        tag2 = Tag.objects.get(id=2)
        name = "My Image"
        data = {'name': name, 'tags': [str(tag1.id), str(tag2.id)]}
        form = AddImageForm(data)
        self.assertFalse(form.is_valid())

    #Test to ensure that image field help text is correct
    def test_image_upload_image_help_text(self):
        form = AddImageForm()
        self.assertEqual(form.fields['image'].help_text, "Image must not be larger than 1250x1250.")

    #Test to ensure a user is not able to upload an image if name is missing
    def test_invalid_image_upload_name_missing(self):
        image = SimpleUploadedFile(name='art1.png', content=open('listings/imagetest/art1.png', 'rb').read(), content_type='image/png')
        tag1 = Tag.objects.get(id=1)
        tag2 = Tag.objects.get(id=2)
        data = {'tags': [str(tag1.id), str(tag2.id)]}
        form = AddImageForm(data, {'image': image})
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to upload an image if name is too long
    def test_invalid_image_upload_name_too_long(self):
        image = SimpleUploadedFile(name='art1.png', content=open('listings/imagetest/art1.png', 'rb').read(), content_type='image/png')
        tag1 = Tag.objects.get(id=1)
        tag2 = Tag.objects.get(id=2)
        name = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        data = {'name': name, 'tags': [str(tag1.id), str(tag2.id)]}
        form = AddImageForm(data, {'image': image})
        self.assertFalse(form.is_valid())

#Tests for the form to create/edit an item
class ItemFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="mikel", password="example",
            email="examplel@text.com", paypalEmail="examplel@text.com",
            invitesOpen=True, inquiriesOpen=True)
        image1 = SimpleUploadedFile(name='art1.png', content=open('listings/imagetest/art1.png', 'rb').read(), content_type='image/png')
        image2 = SimpleUploadedFile(name='art2.png', content=open('listings/imagetest/art2.png', 'rb').read(), content_type='image/png')
        tag1 = Tag.objects.create(name="Test Tag")
        tag2 = Tag.objects.create(name="Test Tag 2")
        test_image1 = Image.objects.create(owner=user,
            image=image1, name="Test Image 1")
        test_image1.tags.add(tag1)
        test_image1.tags.add(tag2)
        test_image1.save
        test_image2 = Image.objects.create(owner=user,
            image=image2, name="Test Image 2")
        test_image2.tags.add(tag1)
        test_image2.save

    #Test to ensure a user is able to upload an item providing all fields
    def test_valid_item_upload(self):
        user = User.objects.get(pk=1)
        image1 = Image.objects.get(id=1)
        image2 = Image.objects.get(id=2)
        name = "My Item"
        description = "An Item to test adding items."
        data = {'name': name, 'description': description, 'images': [str(image1.id), str(image2.id)]}
        form = ItemForm(data=data, user=user)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to upload an item if name is missing
    def test_invalid_item_name_missing(self):
        user = User.objects.get(pk=1)
        image1 = Image.objects.get(id=1)
        image2 = Image.objects.get(id=2)
        description = "An Item to test adding items."
        data = {'description': description, 'images': [str(image1.id), str(image2.id)]}
        form = ItemForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to upload an item if name is too long
    def test_invalid_item_upload_name_too_long(self):
        user = User.objects.get(pk=1)
        image1 = Image.objects.get(id=1)
        image2 = Image.objects.get(id=2)
        name = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        description = "An Item to test adding items."
        data = {'name': name, 'description': description, 'images': [str(image1.id), str(image2.id)]}
        form = ItemForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to upload an item if description is too long
    def test_invalid_item_upload_description_too_long(self):
        user = User.objects.get(pk=1)
        image1 = Image.objects.get(id=1)
        image2 = Image.objects.get(id=2)
        name = "My Item"
        description = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        data = {'name': name, 'description': description, 'images': [str(image1.id), str(image2.id)]}
        form = ItemForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to upload an item if image is missing
    def test_invalid_item_image_missing(self):
        user = User.objects.get(pk=1)
        name = "My Item"
        description = "An Item to test adding items."
        data = {'name': name, 'description': description}
        form = ItemForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure that name field help text is correct
    def test_item_upload_name_help_text(self):
        user = User.objects.get(pk=1)
        form = ItemForm(user=user)
        self.assertEqual(form.fields['name'].help_text, "Name for item is required.")

    #Test to ensure that images field help text is correct
    def test_item_upload_image_help_text(self):
        user = User.objects.get(pk=1)
        form = ItemForm(user=user)
        self.assertEqual(form.fields['images'].help_text, "An image is required.")

#Tests for the form to create an offer listing
class OfferListingFormTest(MyTestCase):
    #Test to ensure a user is able to create an offer listing providing all fields
    def test_valid_offer_listing_creation(self):
        user = self.global_user1
        item1 = self.global_item1
        name = "My Offer Listing"
        description = "Please offer anything I'm poor."
        end_time_choice = '1h'
        open_to_money = True
        min_range = 5.00
        max_range = 10.00
        notes = "Test goes here"
        data = {'name': name, 'description': description, 'items': [str(item1.id)],
            'endTimeChoices': end_time_choice, 'openToMoneyOffers': open_to_money,
            'minRange': min_range, 'maxRange': max_range, 'notes': notes}
        form = OfferListingForm(data=data, user=user)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is able to create an offer listing if maxRange is missing
    def test_valid_offer_listing_maxRange_missing(self):
        user = self.global_user1
        item1 = self.global_item1
        name = "My Offer Listing"
        description = "Please offer anything I'm poor."
        end_time_choice = '1h'
        open_to_money = True
        min_range = 15.00
        notes = "Test goes here"
        data = {'name': name, 'description': description, 'items': [str(item1.id)],
            'endTimeChoices': end_time_choice, 'openToMoneyOffers': open_to_money,
            'minRange': min_range, 'notes': notes}
        form = OfferListingForm(data=data, user=user)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to create an offer listing if minRange > maxRange and maxRange !=0
    def test_invalid_offer_listing_minRange_greater(self):
        user = self.global_user1
        item1 = self.global_item1
        name = "My Offer Listing"
        description = "Please offer anything I'm poor."
        end_time_choice = '1h'
        open_to_money = True
        min_range = 15.00
        max_range = 10.00
        notes = "Test goes here"
        data = {'name': name, 'description': description, 'items': [str(item1.id)],
            'endTimeChoices': end_time_choice, 'openToMoneyOffers': open_to_money,
            'minRange': min_range, 'maxRange': max_range, 'notes': notes}
        form = OfferListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is able to create an offer listing if minRange > maxRange and maxRange == 0
    def test_invalid_offer_listing_minRange_greater_zero(self):
        user = self.global_user1
        item1 = self.global_item1
        name = "My Offer Listing"
        description = "Please offer anything I'm poor."
        end_time_choice = '1h'
        open_to_money = True
        min_range = 15.00
        max_range = 0.00
        notes = "Test goes here"
        data = {'name': name, 'description': description, 'items': [str(item1.id)],
            'endTimeChoices': end_time_choice, 'openToMoneyOffers': open_to_money,
            'minRange': min_range, 'maxRange': max_range, 'notes': notes}
        form = OfferListingForm(data=data, user=user)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to create an offer listing if minRange = maxRange=
    def test_invalid_offer_listing_minRange_maxRange_equal(self):
        user = self.global_user1
        item1 = self.global_item1
        name = "My Offer Listing"
        description = "Please offer anything I'm poor."
        end_time_choice = '1h'
        open_to_money = True
        min_range = 15.00
        max_range = 15.00
        notes = "Test goes here"
        data = {'name': name, 'description': description, 'items': [str(item1.id)],
            'endTimeChoices': end_time_choice, 'openToMoneyOffers': open_to_money,
            'minRange': min_range, 'maxRange': max_range, 'notes': notes}
        form = OfferListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an offer listing if minRange & maxRange are negative
    def test_invalid_offer_listing_minRange_maxRange_negative(self):
        user = self.global_user1
        item1 = self.global_item1
        name = "My Offer Listing"
        description = "Please offer anything I'm poor."
        end_time_choice = '1h'
        open_to_money = True
        min_range = -15.00
        max_range = -15.00
        notes = "Test goes here"
        data = {'name': name, 'description': description, 'items': [str(item1.id)],
            'endTimeChoices': end_time_choice, 'openToMoneyOffers': open_to_money,
            'minRange': min_range, 'maxRange': max_range, 'notes': notes}
        form = OfferListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a listing using someone elses item
    def test_invalid_offer_listing_creation_unowned_item(self):
        user = self.global_user1
        item2 = self.global_item2
        name = "My Offer Listing"
        description = "Please offer anything I'm poor."
        end_time_choice = '1h'
        open_to_money = True
        min_range = 5.00
        max_range = 10.00
        notes = "Test goes here"
        data = {'name': name, 'description': description, 'items': [str(item2.id)],
            'endTimeChoices': end_time_choice, 'openToMoneyOffers': open_to_money,
            'minRange': min_range, 'maxRange': max_range, 'notes': notes}
        form = OfferListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a listing if name is missing
    def test_invalid_offer_listing_creation_name_missing(self):
        user = self.global_user1
        item2 = self.global_item2
        description = "Please offer anything I'm poor."
        end_time_choice = '1h'
        open_to_money = True
        min_range = 5.00
        max_range = 10.00
        notes = "Test goes here"
        data = {'description': description, 'items': [str(item2.id)],
            'endTimeChoices': end_time_choice, 'openToMoneyOffers': open_to_money,
            'minRange': min_range, 'maxRange': max_range, 'notes': notes}
        form = OfferListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a listing if name is too long
    def test_invalid_offer_listing_creation_name_too_long(self):
        user = self.global_user1
        item2 = self.global_item2
        name = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        description = "Please offer anything I'm poor."
        end_time_choice = '1h'
        open_to_money = True
        min_range = 5.00
        max_range = 10.00
        notes = "Test goes here"
        data = {'name': name, 'description': description, 'items': [str(item2.id)],
            'endTimeChoices': end_time_choice, 'openToMoneyOffers': open_to_money,
            'minRange': min_range, 'maxRange': max_range, 'notes': notes}
        form = OfferListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a listing if item is missing
    def test_invalid_offer_listing_creation_item_missing(self):
        user = self.global_user1
        name = "My Offer Listing"
        description = "Please offer anything I'm poor."
        end_time_choice = '1h'
        open_to_money = True
        min_range = 5.00
        max_range = 10.00
        notes = "Test goes here"
        data = {'name': name, 'description': description, 'endTimeChoices': end_time_choice,
            'openToMoneyOffers': open_to_money, 'minRange': min_range, 'maxRange': max_range,
            'notes': notes}
        form = OfferListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a listing if end time choice is missing
    def test_invalid_offer_listing_creation_endtime_choice_missing(self):
        user = self.global_user1
        item2 = self.global_item2
        name = "My Offer Listing"
        description = "Please offer anything I'm poor."
        open_to_money = True
        min_range = 5.00
        max_range = 10.00
        notes = "Test goes here"
        data = {'name': name, 'description': description, 'items': [str(item2.id)],
            'openToMoneyOffers': open_to_money, 'minRange': min_range,
            'maxRange': max_range, 'notes': notes}
        form = OfferListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure that name field help text is correct
    def test_offer_listing_name_help_text(self):
        user = self.global_user1
        form = OfferListingForm(user=user)
        self.assertEqual(form.fields['name'].help_text, "Name for listing is required.")

    #Test to ensure that items field help text is correct
    def test_offer_listing_image_help_text(self):
        user = self.global_user1
        form = OfferListingForm(user=user)
        self.assertEqual(form.fields['items'].help_text, "An item is required.")

    #Test to ensure that minRange field help text is correct
    def test_offer_listing_min_range_help_text(self):
        user = self.global_user1
        form = OfferListingForm(user=user)
        self.assertEqual(form.fields['minRange'].help_text, "Minimum money offers you'll consider.")

    #Test to ensure that maxRange field help text is correct
    def test_offer_listing_max_range_help_text(self):
        user = self.global_user1
        form = OfferListingForm(user=user)
        self.assertEqual(form.fields['maxRange'].help_text, "Maximum money offers you'll consider (leave blank if you don't have a maximum).")

#Tests for the form to create an auction listing
class CreateAuctionListingFormTest(MyTestCase):
    #Test to ensure a user is able to create an auction listing providing all fields
    def test_valid_auction_listing_creation(self):
        user = self.global_user1
        item1 = self.global_item1
        name = "My Auction Listing"
        description = "Just a test auction please ignore."
        end_time_choice = '1h'
        starting_bid = 1.00
        minimum_increment = 0.25
        autobuy = 5.00
        data = {'name': name, 'description': description, 'items': [str(item1.id)],
            'endTimeChoices': end_time_choice, 'startingBid': starting_bid,
            'minimumIncrement': minimum_increment, 'autobuy': autobuy}
        form = AuctionListingForm(data=data, user=user)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to create an auction listing if name is too long
    def test_invalid_auction_listing_name_too_long(self):
        user = self.global_user1
        item1 = self.global_item1
        name = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        description = "Just a test auction please ignore."
        end_time_choice = '1h'
        starting_bid = 1.00
        minimum_increment = 0.25
        autobuy = 5.00
        data = {'name': name, 'description': description, 'items': [str(item1.id)],
            'endTimeChoices': end_time_choice, 'startingBid': starting_bid,
            'minimumIncrement': minimum_increment, 'autobuy': autobuy}
        form = AuctionListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an auction listing if name is missing
    def test_invalid_auction_listing_name_missing(self):
        user = self.global_user1
        item1 = self.global_item1
        description = "Just a test auction please ignore."
        end_time_choice = '1h'
        starting_bid = 1.00
        minimum_increment = 0.25
        autobuy = 5.00
        data = {'description': description, 'items': [str(item1.id)],
            'endTimeChoices': end_time_choice, 'startingBid': starting_bid,
            'minimumIncrement': minimum_increment, 'autobuy': autobuy}
        form = AuctionListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an auction listing if description is missing
    def test_invalid_auction_listing_description_missing(self):
        user = self.global_user1
        item1 = self.global_item1
        name = "My Auction Listing"
        end_time_choice = '1h'
        starting_bid = 1.00
        minimum_increment = 0.25
        autobuy = 5.00
        data = {'name': name, 'items': [str(item1.id)], 'endTimeChoices': end_time_choice,
            'startingBid': starting_bid, 'minimumIncrement': minimum_increment,
            'autobuy': autobuy}
        form = AuctionListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an auction listing if item is missing
    def test_invalid_auction_listing_item_missing(self):
        user = self.global_user1
        name = "My Auction Listing"
        description = "Just a test auction please ignore."
        end_time_choice = '1h'
        starting_bid = 1.00
        minimum_increment = 0.25
        autobuy = 5.00
        data = {'name': name, 'description': description, 'endTimeChoices': end_time_choice,
            'startingBid': starting_bid, 'minimumIncrement': minimum_increment, 'autobuy': autobuy}
        form = AuctionListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an auction listing if item is not owned by current user
    def test_invalid_auction_listing_item_not_owned(self):
        user = self.global_user1
        item2 = self.global_item2
        name = "My Auction Listing"
        description = "Just a test auction please ignore."
        end_time_choice = '1h'
        starting_bid = 1.00
        minimum_increment = 0.25
        autobuy = 5.00
        data = {'name': name, 'description': description, 'items': [str(item2.id)],
            'endTimeChoices': end_time_choice, 'startingBid': starting_bid,
            'minimumIncrement': minimum_increment, 'autobuy': autobuy}
        form = AuctionListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an auction listing if starting bid is missing
    def test_invalid_auction_listing_start_bid_missing(self):
        user = self.global_user1
        item1 = self.global_item1
        name = "My Auction Listing"
        description = "Just a test auction please ignore."
        end_time_choice = '1h'
        minimum_increment = 0.25
        autobuy = 5.00
        data = {'name': name, 'description': description, 'items': [str(item1.id)],
            'endTimeChoices': end_time_choice, 'minimumIncrement': minimum_increment,
            'autobuy': autobuy}
        form = AuctionListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an auction listing if starting bid is less than 0.01
    def test_invalid_auction_listing_low_starting_bid(self):
        user = self.global_user1
        item1 = self.global_item1
        name = "My Auction Listing"
        description = "Just a test auction please ignore."
        end_time_choice = '1h'
        starting_bid = -1.00
        minimum_increment = 0.25
        autobuy = 5.00
        data = {'name': name, 'description': description, 'items': [str(item1.id)],
            'endTimeChoices': end_time_choice, 'startingBid': starting_bid,
            'minimumIncrement': minimum_increment, 'autobuy': autobuy}
        form = AuctionListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an auction listing if minimum increment is missing
    def test_invalid_auction_listing_minimum_increment_missing(self):
        user = self.global_user1
        item1 = self.global_item1
        name = "My Auction Listing"
        description = "Just a test auction please ignore."
        end_time_choice = '1h'
        starting_bid = 1.00
        autobuy = 5.00
        data = {'name': name, 'description': description, 'items': [str(item1.id)],
            'endTimeChoices': end_time_choice, 'startingBid': starting_bid,
            'autobuy': autobuy}
        form = AuctionListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an auction listing if minimum increment is negative
    def test_invalid_auction_listing_negative_minimum_increment(self):
        user = self.global_user1
        item1 = self.global_item1
        name = "My Auction Listing"
        description = "Just a test auction please ignore."
        end_time_choice = '1h'
        starting_bid = 1.00
        minimum_increment = -0.25
        autobuy = 5.00
        data = {'name': name, 'description': description, 'items': [str(item1.id)],
            'endTimeChoices': end_time_choice, 'startingBid': starting_bid,
            'minimumIncrement': minimum_increment, 'autobuy': autobuy}
        form = AuctionListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an auction listing if minimum increment is greater than starting bid
    def test_invalid_auction_listing_greater_minimum_increment(self):
        user = self.global_user1
        item1 = self.global_item1
        name = "My Auction Listing"
        description = "Just a test auction please ignore."
        end_time_choice = '1h'
        starting_bid = -1.00
        minimum_increment = 1.25
        autobuy = 5.00
        data = {'name': name, 'description': description, 'items': [str(item1.id)],
            'endTimeChoices': end_time_choice, 'startingBid': starting_bid,
            'minimumIncrement': minimum_increment, 'autobuy': autobuy}
        form = AuctionListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is able to create an auction listing if autobuy is missing
    def test_valid_auction_listing_missing_autobuy(self):
        user = self.global_user1
        item1 = self.global_item1
        name = "My Auction Listing"
        description = "Just a test auction please ignore."
        end_time_choice = '1h'
        starting_bid = 1.00
        minimum_increment = 0.25
        data = {'name': name, 'description': description, 'items': [str(item1.id)],
            'endTimeChoices': end_time_choice, 'startingBid': starting_bid,
            'minimumIncrement': minimum_increment}
        form = AuctionListingForm(data=data, user=user)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to create an auction listing if autobuy is equal to or less than starting bid
    def test_invalid_auction_listing_autobuy_equals_or_less_start_bid(self):
        user = self.global_user1
        item1 = self.global_item1
        name = "My Auction Listing"
        description = "Just a test auction please ignore."
        end_time_choice = '1h'
        starting_bid = 1.00
        minimum_increment = 0.25
        autobuy = 1.00
        data = {'name': name, 'description': description, 'items': [str(item1.id)],
            'endTimeChoices': end_time_choice, 'startingBid': starting_bid,
            'minimumIncrement': minimum_increment, 'autobuy': autobuy}
        form = AuctionListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an auction listing if autobuy is negative
    def test_invalid_auction_listing_negative_autobuy(self):
        user = self.global_user1
        item1 = self.global_item1
        name = "My Auction Listing"
        description = "Just a test auction please ignore."
        end_time_choice = '1h'
        starting_bid = 1.00
        minimum_increment = 0.25
        autobuy = -5.00
        data = {'name': name, 'description': description, 'items': [str(item1.id)],
            'endTimeChoices': end_time_choice, 'startingBid': starting_bid,
            'minimumIncrement': minimum_increment, 'autobuy': autobuy}
        form = AuctionListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure that name field help text is correct
    def test_auction_listing_name_help_text(self):
        user = self.global_user1
        form = AuctionListingForm(user=user)
        self.assertEqual(form.fields['name'].help_text, "Name for listing is required.")

    #Test to ensure that items field help text is correct
    def test_auction_listing_image_help_text(self):
        user = self.global_user1
        form = AuctionListingForm(user=user)
        self.assertEqual(form.fields['items'].help_text, "An item is required.")

    #Test to ensure that startingBid field help text is correct
    def test_auction_listing_start_bid_help_text(self):
        user = self.global_user1
        form = AuctionListingForm(user=user)
        self.assertEqual(form.fields['startingBid'].help_text, "Money amount bidding should start at for auction.")

    #Test to ensure that minimumIncrement field help text is correct
    def test_auction_listing_start_bid_help_text(self):
        user = self.global_user1
        form = AuctionListingForm(user=user)
        self.assertEqual(form.fields['minimumIncrement'].help_text, "Minimum increment bid that can be placed on the auction, that cannot be greater than the starting bid (maximum increment bid will be x3 this value).")

    #Test to ensure that autobuy field help text is correct
    def test_auction_listing_autobuy_help_text(self):
        user = self.global_user1
        form = AuctionListingForm(user=user)
        self.assertEqual(form.fields['autobuy'].help_text, "A bid greater than the starting bid that will automatically win the auction if placed. (Leave blank if not interested in having an autobuy price)")

#Tests for the form to create an offer
class CreateOfferFormTest(MyTestCase):
    def setUp(self):
        super(CreateOfferFormTest, self).setUp()
        user1 = self.global_user1
        user2 = self.global_user2

        date_ended = timezone.localtime(timezone.now()) - timedelta(hours=1)
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        #An active listing that is open to money offers
        self.offer_listing1 = OfferListing.objects.create(owner=user1, name="Test Listing",
            description="Just a test", openToMoneyOffers=True, minRange=5.00, maxRange=10.00,
            notes="Just offer.", endTime=date_active)
        self.offer_listing1.items.add(self.global_item1)
        self.offer_listing1.save

        #An active listing that is not open to money offers
        self.offer_listing2 = OfferListing.objects.create(owner=user1, name="Test Listing 2",
            description="Just a test", openToMoneyOffers=False, minRange=0.00, maxRange=0.00,
            notes="Just offer.", endTime=date_active)
        self.offer_listing2.items.add(self.global_item1)
        self.offer_listing2.save

        #An inactive listing that has ended
        self.offer_listing3 = OfferListing.objects.create(owner=user1, name="Ended Listing",
            description="This has ended", openToMoneyOffers=True, minRange=5.00, maxRange=10.00,
            notes="Just offer.", endTime=date_ended)
        self.offer_listing3.items.add(self.global_item1)
        self.offer_listing3.save

    #Test to ensure a user is able to create an offer for a listing open to money providing all fields
    def test_valid_offer_creation_open_to_money(self):
        user = self.global_user2
        listing = self.offer_listing1
        amount = 5.00
        data = {'items': [str(self.global_item2.id)], 'amount': amount}
        form = OfferForm(data=data, user=user, instance=listing, initial={'offerListing': listing})
        self.assertTrue(form.is_valid())

    #Test to ensure a user is able to create an offer for a listing open to money without an item
    def test_valid_offer_creation_open_to_money_no_item(self):
        user = self.global_user2
        listing = self.offer_listing1
        amount = 5.00
        data = {'amount': amount}
        form = OfferForm(data=data, user=user, instance=listing, initial={'offerListing': listing})
        self.assertTrue(form.is_valid())

    #Test to ensure a user is able to create an offer for a listing open to money without offering money
    def test_valid_offer_creation_open_to_money_no_money(self):
        user = self.global_user2
        listing = self.offer_listing1
        amount = 5.00
        data = {'items': [str(self.global_item2.id)]}
        form = OfferForm(data=data, user=user, instance=listing, initial={'offerListing': listing})
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to create an offer for a listing open to money offering below minimum
    def test_invalid_offer_creation_open_to_money_below_min(self):
        user = self.global_user2
        listing = self.offer_listing1
        amount = 4.00
        data = {'items': [str(self.global_item2.id)], 'amount': amount}
        form = OfferForm(data=data, user=user, instance=listing, initial={'offerListing': listing})
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an offer for a listing open to money offering above maximum
    def test_invalid_offer_creation_open_to_money_above_max(self):
        user = self.global_user2
        listing = self.offer_listing1
        amount = 11.00
        data = {'items': [str(self.global_item2.id)], 'amount': amount}
        form = OfferForm(data=data, user=user, instance=listing, initial={'offerListing': listing})
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an offer for a listing open to money without an item or cash
    def test_invalid_offer_creation_open_to_money_nothing_offer(self):
        user = self.global_user2
        listing = self.offer_listing1
        data = {}
        form = OfferForm(data=data, user=user, instance=listing, initial={'offerListing': listing})
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an offer for a listing not open to money offering cash
    def test_invalid_offer_creation_not_open_to_money_offering_cash(self):
        user = self.global_user2
        listing = self.offer_listing2
        amount = 5.00
        data = {'items': [str(self.global_item2.id)], 'amount': amount}
        form = OfferForm(data=data, user=user, instance=listing, initial={'offerListing': listing})
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an offer for a listing open to money without an item
    def test_invalid_offer_creation_not_open_to_money_nothing_offered(self):
        user = self.global_user2
        listing = self.offer_listing2
        amount = 5.00
        data = {}
        form = OfferForm(data=data, user=user, instance=listing, initial={'offerListing': listing})
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an offer for a listing using an item they dont own
    def test_invalid_offer_creation_item_not_owned(self):
        user = self.global_user2
        listing = self.offer_listing1
        amount = 5.00
        data = {'items': [str(self.global_item1.id)], 'amount': amount}
        form = OfferForm(data=data, user=user, instance=listing, initial={'offerListing': listing})
        self.assertFalse(form.is_valid())

    #Test to ensure that a user cannot place an offer on a listing that has ended
    def test_invalid_offer_creation_listing_ended(self):
        user = self.global_user2
        listing = self.offer_listing3
        amount = 5.00
        data = {'items': [str(self.global_item2.id)], 'amount': amount}
        form = OfferForm(data=data, user=user, instance=listing, initial={'offerListing': listing})
        self.assertFalse(form.is_valid())

#Tests for the form to create a bid
class CreateBidFormTest(MyTestCase):
    def setUp(self):
        super(CreateBidFormTest, self).setUp()
        user1 = self.global_user1
        user2 = self.global_user2
        user3 = User.objects.create(username="mikey", password="example",
            email="example5@text.com", paypalEmail="examplepassword5@text.com",
            invitesOpen=True, inquiriesOpen=True)

        date_ended = timezone.localtime(timezone.now()) - timedelta(hours=1)
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        #An active auction listing with no bids currently
        self.auction_listing1 = AuctionListing.objects.create(owner=user1, name="Test Auction",
            description="Just a test", startingBid=1.00, minimumIncrement=0.25, autobuy=5.00,
            endTime=date_active)
        self.auction_listing1.items.add(self.global_item1)
        self.auction_listing1.save

        #An active auction listing that has at least one bid
        self.auction_listing2 = AuctionListing.objects.create(owner=user1, name="Test Auction",
            description="Just a test", startingBid=1.00, minimumIncrement=0.25, autobuy=5.00,
            endTime=date_active)
        self.auction_listing2.items.add(self.global_item1)
        self.auction_listing2.save
        self.bid1 = Bid.objects.create(auctionListing=self.auction_listing2, bidder=user3,
            amount=1.00, winningBid=False)

        #An active auction listing that has a current bid from the user bidding
        self.auction_listing3 = AuctionListing.objects.create(owner=user1, name="Test Auction",
            description="Just a test", startingBid=1.00, minimumIncrement=0.25, autobuy=5.00,
            endTime=date_active)
        self.auction_listing3.items.add(self.global_item1)
        self.auction_listing3.save
        self.bid2 = Bid.objects.create(auctionListing=self.auction_listing3, bidder=user2,
            amount=1.00, winningBid=False)

        #An inactive auction listing that has ended
        self.auction_listing4 = AuctionListing.objects.create(owner=user1, name="Test Auction",
            description="Just a test", startingBid=1.00, minimumIncrement=0.25, autobuy=5.00,
            endTime=date_ended)
        self.auction_listing4.items.add(self.global_item1)
        self.auction_listing4.save

        #An active auction listing that has at least one bid greater than starting bid
        self.auction_listing5 = AuctionListing.objects.create(owner=user1, name="Test Auction",
            description="Just a test", startingBid=1.00, minimumIncrement=0.25, autobuy=5.00,
            endTime=date_active)
        self.auction_listing5.items.add(self.global_item1)
        self.auction_listing5.save
        self.bid3 = Bid.objects.create(auctionListing=self.auction_listing5, bidder=user3,
            amount=1.50, winningBid=False)

    #Test to ensure a user is able to create an bid for a listing that's active
    def test_valid_bid_creation_active_auction(self):
        user = self.global_user2
        listing = self.auction_listing1
        amount = 1.00
        data = {'amount': amount}
        form = CreateBidForm(data=data, instance=listing, initial={'auctionListing': listing,
            'bidder': user})
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to create an bid without an amount
    def test_invalid_bid_creation_active_auction_no_amount(self):
        user = self.global_user2
        listing = self.auction_listing1
        amount = 1.00
        data = {}
        form = CreateBidForm(data=data, instance=listing, initial={'auctionListing': listing,
            'bidder': user})
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an bid for a listing that's inactive
    def test_invalid_bid_creation_inactive_auction(self):
        user = self.global_user2
        listing = self.auction_listing4
        amount = 1.00
        data = {'amount': amount}
        form = CreateBidForm(data=data, instance=listing, initial={'auctionListing': listing,
            'bidder': user})
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to bid starting bid on an auction that has a starting bid already
    def test_invalid_bid_creation_same_as_starting_bid(self):
        user = self.global_user2
        listing = self.auction_listing2
        amount = 1.00
        data = {'amount': amount}
        form = CreateBidForm(data=data, instance=listing, initial={'auctionListing': listing,
            'bidder': user})
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to bid below the starting bid
    def test_invalid_bid_creation_active_auction_bid_lower_than_starting_bid(self):
        user = self.global_user2
        listing = self.auction_listing1
        amount = 0.75
        data = {'amount': amount}
        form = CreateBidForm(data=data, instance=listing, initial={'auctionListing': listing,
            'bidder': user})
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to bid below the minimum increment
    def test_invalid_bid_creation_active_auction_bid_lower_than_minimum_increment(self):
        user = self.global_user2
        listing = self.auction_listing1
        amount = 1.15
        data = {'amount': amount}
        form = CreateBidForm(data=data, instance=listing, initial={'auctionListing': listing,
            'bidder': user})
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to bid below the current bid
    def test_invalid_bid_creation_active_auction_bid_lower_than_current_bid(self):
        user = self.global_user2
        listing = self.auction_listing5
        amount = 1.25
        data = {'amount': amount}
        form = CreateBidForm(data=data, instance=listing, initial={'auctionListing': listing,
            'bidder': user})
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to bid more than 3x the minimum increment
    def test_invalid_bid_creation_active_auction_bid_greater_than_x3(self):
        user = self.global_user2
        listing = self.auction_listing1
        amount = 2.00
        data = {'amount': amount}
        form = CreateBidForm(data=data, instance=listing, initial={'auctionListing': listing,
            'bidder': user})
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to bid when they have the current highest bid already
    def test_invalid_bid_creation_active_auction_already_current_highest_bid(self):
        user = self.global_user2
        listing = self.auction_listing3
        amount = 1.25
        data = {'amount': amount}
        form = CreateBidForm(data=data, instance=listing, initial={'auctionListing': listing,
            'bidder': user})
        self.assertFalse(form.is_valid())

    #Test to ensure a user is able to bid the autobuy amount
    def test_valid_bid_creation_autobuy_bid(self):
        user = self.global_user2
        listing = self.auction_listing1
        amount = 5.00
        data = {'amount': amount}
        form = CreateBidForm(data=data, instance=listing, initial={'auctionListing': listing,
            'bidder': user})
        self.assertTrue(form.is_valid())

#Tests for the form to create/edit an event
class EventFormTest(MyTestCase):
    #Test to ensure a user is able to create an event providing all fields
    def test_valid_event_creation(self):
        title = "My Test Event"
        context = "Come to my event please, I'm lonely."
        date = "2020-11-06 15:00"
        location = "1234 Sesame Street"
        data = {'title': title, 'context': context, 'date': date, 'location': location}
        form = EventForm(data)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to create an event if title is too long
    def test_invalid_event_creation_title_too_long(self):
        title = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        context = "Come to my event please, I'm lonely."
        date = "2020-11-06 15:00"
        location = "1234 Sesame Street"
        data = {'title': title, 'context': context, 'date': date, 'location': location}
        form = EventForm(data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an event if context is too long
    def test_invalid_event_creation_context_too_long(self):
        title = "My Test Event"
        context = ("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" +
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" +
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" +
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" +
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" +
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        date = "2020-11-06 15:00"
        location = "1234 Sesame Street"
        data = {'title': title, 'context': context, 'date': date, 'location': location}
        form = EventForm(data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an event if date is invalid
    def test_invalid_event_creation_invalid_date(self):
        title = "My Test Event"
        context = "Come to my event please, I'm lonely."
        date = "220-11-06 15:00"
        location = "1234 Sesame Street"
        data = {'title': title, 'context': context, 'date': date, 'location': location}
        form = EventForm(data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an event if location is too long
    def test_invalid_event_creation_invalid_date(self):
        title = "My Test Event"
        context = "Come to my event please, I'm lonely."
        date = "220-11-06 15:00"
        location = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        data = {'title': title, 'context': context, 'date': date, 'location': location}
        form = EventForm(data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an event if title is missing
    def test_invalid_event_creation_title_missing(self):
        title = "My Test Event"
        context = "Come to my event please, I'm lonely."
        date = "2020-11-06 15:00"
        location = "1234 Sesame Street"
        data = {'context': context, 'date': date, 'location': location}
        form = EventForm(data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an event without context given
    def test_valid_event_creation_no_context(self):
        title = "My Test Event"
        context = "Come to my event please, I'm lonely."
        date = "2020-11-06 15:00"
        location = "1234 Sesame Street"
        data = {'title': title, 'date': date, 'location': location}
        form = EventForm(data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an event if date is missing
    def test_invalid_event_creation_date_missing(self):
        title = "My Test Event"
        context = "Come to my event please, I'm lonely."
        date = "2020-11-06 15:00"
        location = "1234 Sesame Street"
        data = {'title': title, 'context': context, 'location': location}
        form = EventForm(data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an event if location is missing
    def test_invalid_event_creation_location_missing(self):
        title = "My Test Event"
        context = "Come to my event please, I'm lonely."
        date = "2020-11-06 15:00"
        location = "1234 Sesame Street"
        data = {'title': title, 'context': context, 'date': date}
        form = EventForm(data)
        self.assertFalse(form.is_valid())

    #Test to ensure that title field help text is correct
    def test_event_title_help_text(self):
        form = EventForm()
        self.assertEqual(form.fields['title'].help_text, "Title For the Event Required.")

    #Test to ensure that date field help text is correct
    def test_event_date_help_text(self):
        form = EventForm()
        self.assertEqual(form.fields['date'].help_text, "Date/Time for Event ('YY-MM-DD' format or 'YY-MM-DD H:M' format).")

    #Test to ensure that location field help text is correct
    def test_event_location_help_text(self):
        form = EventForm()
        self.assertEqual(form.fields['location'].help_text, "Address Where Event is Held.")

#Tests for the form to create invitations
class InvitationFormTest(MyTestCase):
    def setUp(self):
        super(InvitationFormTest, self).setUp()

        #Create some users to submit for the invitation form
        self.user1 = User.objects.create(username="mikey", password="example",
            email="exampley@text.com", paypalEmail="exampley@text.com",
            invitesOpen=True, inquiriesOpen=True)
        self.user2 = User.objects.create(username="mikel", password="example",
            email="examplel@text.com", paypalEmail="examplel@text.com",
            invitesOpen=True, inquiriesOpen=True)
        self.user3 = User.objects.create(username="mikes", password="example",
            email="examples@text.com", paypalEmail="examples@text.com",
            invitesOpen=False, inquiriesOpen=True)
        self.user4 = User.objects.create(username="mikea", password="example",
            email="examplea@text.com", paypalEmail="examplea@text.com",
            invitesOpen=True, inquiriesOpen=True)
        self.user5 = User.objects.create(username="miken", password="example",
            email="examplen@text.com", paypalEmail="examplen@text.com",
            invitesOpen=True, inquiriesOpen=True)

        #Set the locations of the global users and new user
        self.user1.profile.latitude = 40.0000
        self.user1.profile.longitude = -75.0000
        self.user1.profile.save()

        self.user2.profile.latitude = 40.1000
        self.user2.profile.longitude = -75.1000
        self.user2.profile.save()

        self.user3.profile.latitude = 40.2000
        self.user3.profile.longitude = -75.2000
        self.user3.profile.save()

        self.user4.profile.latitude = 40.3000
        self.user4.profile.longitude = -75.3000
        self.user4.profile.save()

        self.user5.profile.latitude = 41.0000
        self.user5.profile.longitude = -76.0000
        self.user5.profile.save()

        #Create an event that users will receive invitstion to
        self.event = Event.objects.create(host=self.global_user1,
            title="My Awesome Event", context="Please come to my event.",
            date="2020-11-06 15:00", location="1234 Sesame Street")

        #Set location for event host
        self.global_user1.profile.latitude = 40.0000
        self.global_user1.profile.longitude = -75.0000
        self.global_user1.profile.save()

        #Create an invitation for user4
        Invitation.objects.create(event=self.event, recipient=self.user4)

    #Test to ensure a user is able to submit invitation form providing all fields
    def test_valid_invitation_form_submission(self):
        event = self.event
        data = {'users': [str(self.user1.id), str(self.user2.id)]}
        form = InvitationForm(data=data, instance=event, initial={'event': event})
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to submit invitation form if users ar enot given
    def test_invalid_invitation_form_submission_no_users_selected(self):
        event = self.event
        data = {}
        form = InvitationForm(data=data, instance=event, initial={'event': event})
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to submit invitation form if user is not accepting invites
    def test_invalid_invitation_form_submission_user_not_accepting_invites(self):
        event = self.event
        data = {'users': [str(self.user3.id)]}
        form = InvitationForm(data=data, instance=event, initial={'event': event})
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to submit invitation form if one user is not accepting invites
    def test_invalid_invitation_form_submission_one_user_not_accepting_invites(self):
        event = self.event
        data = {'users': [str(self.user1.id), str(self.user3.id)]}
        form = InvitationForm(data=data, instance=event, initial={'event': event})
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to submit invitation form if user already received an invite
    def test_invalid_invitation_form_user_already_has_invitation(self):
        event = self.event
        data = {'users': [str(self.user4.id)]}
        form = InvitationForm(data=data, instance=event, initial={'event': event})
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to submit invitation form if they invite themselves
    def test_invalid_invitation_form_submission_host_cant_invite_self(self):
        event = self.event
        data = {'users': [str(self.global_user1.id)]}
        form = InvitationForm(data=data, instance=event, initial={'event': event})
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to submit invitation form if a invited user
    #is not within 50m of host
    def test_invalid_invitation_form_submission_user_not_in_range(self):
        event = self.event
        data = {'users': [str(self.user5.id)]}
        form = InvitationForm(data=data, instance=event, initial={'event': event})
        self.assertFalse(form.is_valid())

    #Test to ensure that users field label is correct
    def test_invitation_form_users_label(self):
        event = self.event
        form = InvitationForm(instance=event)
        self.assertEqual(form.fields['users'].label, "Users to Invite")

    #Test to ensure that users field help text is correct
    def test_invitation_form_users_help_text(self):
        event = self.event
        form = InvitationForm(instance=event)
        self.assertEqual(form.fields['users'].help_text, "Users You Would Like to Invite to Event.")

#Tests for the form to create/edit a wishlist
class WishlistFormTest(MyTestCase):
    #Test to ensure a user is able to create a wishlist providing all fields
    def test_valid_wishlist_creation(self):
        user = self.global_user1
        title = "My Test Wishlist"
        description = "Stuff I want"
        data = {'title': title, 'description': description, 'items': [str(self.global_item1.id)]}
        form = WishlistForm(data=data, user=user)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is able to create a wishlist without an item
    def test_valid_wishlist_creation_no_items(self):
        user = self.global_user1
        title = "My Test Wishlist"
        description = "Stuff I want"
        data = {'title': title, 'description': description}
        form = WishlistForm(data=data, user=user)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to create a wishlist using an item they don't own
    def test_invalid_wishlist_creation_item_not_owned(self):
        user = self.global_user1
        title = "My Test Wishlist"
        description = "Stuff I want"
        data = {'title': title, 'description': description, 'items': [str(self.global_item2.id)]}
        form = WishlistForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a wishlist if title is missing
    def test_invalid_wishlist_creation_no_title(self):
        user = self.global_user1
        title = "My Test Wishlist"
        description = "Stuff I want"
        data = {'description': description, 'items': [str(self.global_item1.id)]}
        form = WishlistForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a wishlist if title is too long
    def test_invalid_wishlist_creation_title_too_long(self):
        user = self.global_user1
        title = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        description = "Stuff I want"
        data = {'title': title, 'description': description, 'items': [str(self.global_item1.id)]}
        form = WishlistForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a wishlist if description is missing
    def test_invalid_wishlist_creation_no_description(self):
        user = self.global_user1
        title = "My Test Wishlist"
        description = "Stuff I want"
        data = {'title': title, 'items': [str(self.global_item1.id)]}
        form = WishlistForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a wishlist if description is too long
    def test_invalid_wishlist_creation_description_too_long(self):
        user = self.global_user1
        title = "My Test Wishlist"
        description = ("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        data = {'title': title, 'description': description, 'items': [str(self.global_item1.id)]}
        form = WishlistForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure that title field help text is correct
    def test_wishlist_creation_title_help_text(self):
        user = self.global_user1
        form = WishlistForm(user=user)
        self.assertEqual(form.fields['title'].help_text, "Title of Wishlist.")

    #Test to ensure that description field help text is correct
    def test_wishlist_creation_description_help_text(self):
        user = self.global_user1
        form = WishlistForm(user=user)
        self.assertEqual(form.fields['description'].help_text, ("Description for Wishlist" +
            " (what it contains, how you want to accuire the items, etc.)"))

    #Test to ensure that items field label is correct
    def test_wishlist_creation_items_help_text(self):
        user = self.global_user1
        form = WishlistForm(user=user)
        self.assertEqual(form.fields['items'].label, "Wishlist Items")

    #Test to ensure that items field help text is correct
    def test_wishlist_creation_items_help_text(self):
        user = self.global_user1
        form = WishlistForm(user=user)
        self.assertEqual(form.fields['items'].help_text, "Items That You Are Seeking.")

#Tests for the form to create a wishlist listing
class WishlistListingFormTest(MyTestCase):
    #Test to ensure a user is able to create an wishlist listing providing all fields
    def test_valid_wishlist_listing_creation(self):
        user = self.global_user1
        name = "My Wishlist Listing"
        end_time_choice = '1h'
        money_offer = 6.00
        notes = "Please I really want this"
        data = {'name': name, 'items': [str(self.global_item1.id)],
            'endTimeChoices': end_time_choice, 'moneyOffer': money_offer,
            'itemsOffer': [str(self.global_item1.id)],'notes': notes}
        form = WishlistListingForm(data=data, user=user)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is able to create an wishlist listing without offering money
    #but offering items
    def test_valid_wishlist_listing_creation_no_money_offered(self):
        user = self.global_user1
        name = "My Wishlist Listing"
        end_time_choice = '1h'
        money_offer = 6.00
        notes = "Please I really want this"
        data = {'name': name, 'items': [str(self.global_item1.id)],
            'endTimeChoices': end_time_choice, 'itemsOffer': [str(self.global_item1.id)],
            'notes': notes}
        form = WishlistListingForm(data=data, user=user)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is able to create an wishlist listing without offering items
    #but offering money
    def test_valid_wishlist_listing_creation_no_items_offered(self):
        user = self.global_user1
        name = "My Wishlist Listing"
        end_time_choice = '1h'
        money_offer = 6.00
        notes = "Please I really want this"
        data = {'name': name, 'items': [str(self.global_item1.id)],
            'endTimeChoices': end_time_choice, 'moneyOffer': money_offer,
            'notes': notes}
        form = WishlistListingForm(data=data, user=user)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to create an wishlist listing using item not owned
    #as wishlist item
    def test_invalid_wishlist_listing_creation_item_not_owned_for_wishlist_item(self):
        user = self.global_user1
        name = "My Wishlist Listing"
        end_time_choice = '1h'
        money_offer = 6.00
        notes = "Please I really want this"
        data = {'name': name, 'items': [str(self.global_item2.id)],
            'endTimeChoices': end_time_choice, 'moneyOffer': money_offer,
            'itemsOffer': [str(self.global_item1.id)],'notes': notes}
        form = WishlistListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an wishlist listing using item not on
    #wishlist as wishlist item
    def test_invalid_wishlist_listing_creation_item_not_in_wishlist(self):
        user = self.global_user1
        name = "My Wishlist Listing"
        end_time_choice = '1h'
        money_offer = 6.00
        notes = "Please I really want this"
        data = {'name': name, 'items': [str(self.global_non_wishlist_item.id)],
            'endTimeChoices': end_time_choice, 'moneyOffer': money_offer,
            'itemsOffer': [str(self.global_item1.id)],'notes': notes}
        form = WishlistListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an wishlist listing using item not
    #owned for item offer
    def test_invalid_wishlist_listing_creation_item_not_owned_to_offer(self):
        user = self.global_user1
        name = "My Wishlist Listing"
        end_time_choice = '1h'
        money_offer = 6.00
        notes = "Please I really want this"
        data = {'name': name, 'items': [str(self.global_item1.id)],
            'endTimeChoices': end_time_choice, 'moneyOffer': money_offer,
            'itemsOffer': [str(self.global_item2.id)],'notes': notes}
        form = WishlistListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an wishlist listing if wishlist items
    #are not selected
    def test_invalid_wishlist_listing_creation_no_wishlist_items(self):
        user = self.global_user1
        name = "My Wishlist Listing"
        end_time_choice = '1h'
        money_offer = 6.00
        notes = "Please I really want this"
        data = {'name': name, 'endTimeChoices': end_time_choice,
            'moneyOffer': money_offer, 'itemsOffer': [str(self.global_item1.id)],
            'notes': notes}
        form = WishlistListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is able to create an wishlist listing if name is not given
    def test_valid_wishlist_listing_creation_no_name_given(self):
        user = self.global_user1
        name = "My Wishlist Listing"
        end_time_choice = '1h'
        money_offer = 6.00
        notes = "Please I really want this"
        data = {'items': [str(self.global_item1.id)],
            'endTimeChoices': end_time_choice, 'moneyOffer': money_offer,
            'itemsOffer': [str(self.global_item1.id)],'notes': notes}
        form = WishlistListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an wishlist listing if end time
    #is not selected
    def test_invalid_wishlist_listing_creation_no_end_time(self):
        user = self.global_user1
        name = "My Wishlist Listing"
        end_time_choice = '1h'
        money_offer = 6.00
        notes = "Please I really want this"
        data = {'name': name, 'items': [str(self.global_item1.id)],
            'moneyOffer': money_offer, 'itemsOffer': [str(self.global_item1.id)],
            'notes': notes}
        form = WishlistListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an wishlist listing if money
    #offer and offer items are not given
    def test_invalid_wishlist_listing_creation_no_money_or_items_offered(self):
        user = self.global_user1
        name = "My Wishlist Listing"
        end_time_choice = '1h'
        money_offer = 6.00
        notes = "Please I really want this"
        data = {'name': name, 'items': [str(self.global_item1.id)],
            'endTimeChoices': end_time_choice, 'notes': notes}
        form = WishlistListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an wishlist listing if notes
    #are not included
    def test_invalid_wishlist_listing_creation_no_notes(self):
        user = self.global_user1
        name = "My Wishlist Listing"
        end_time_choice = '1h'
        money_offer = 6.00
        notes = "Please I really want this"
        data = {'name': name, 'items': [str(self.global_item1.id)],
            'endTimeChoices': end_time_choice, 'moneyOffer': money_offer,
            'itemsOffer': [str(self.global_item1.id)]}
        form = WishlistListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an wishlist listing if name is
    #too long
    def test_invalid_wishlist_listing_creation_name_too_long(self):
        user = self.global_user1
        name = ("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        end_time_choice = '1h'
        money_offer = 6.00
        notes = "Please I really want this"
        data = {'name': name, 'items': [str(self.global_item1.id)],
            'endTimeChoices': end_time_choice, 'moneyOffer': money_offer,
            'itemsOffer': [str(self.global_item1.id)],'notes': notes}
        form = WishlistListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an wishlist listing if amount offered
    #is negative
    def test_invalid_wishlist_listing_creation_negative_amount_offered(self):
        user = self.global_user1
        name = "My Wishlist Listing"
        end_time_choice = '1h'
        money_offer = -6.00
        notes = "Please I really want this"
        data = {'name': name, 'items': [str(self.global_item1.id)],
            'endTimeChoices': end_time_choice, 'moneyOffer': money_offer,
            'itemsOffer': [str(self.global_item1.id)],'notes': notes}
        form = WishlistListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create an wishlist listing if notes
    #are too long
    def test_invalid_wishlist_listing_creation_notes_too_long(self):
        user = self.global_user1
        name = "My Wishlist Listing"
        end_time_choice = '1h'
        money_offer = 6.00
        notes = ("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        data = {'name': name, 'items': [str(self.global_item1.id)],
            'endTimeChoices': end_time_choice, 'moneyOffer': money_offer,
            'itemsOffer': [str(self.global_item1.id)],'notes': notes}
        form = WishlistListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure that name field help text is correct
    def test_wishlist_listing_name_help_text(self):
        user = self.global_user1
        form = WishlistListingForm(user=user)
        self.assertEqual(form.fields['name'].help_text, "Name for listing is required.")

    #Test to ensure that items field help text is correct
    def test_wishlist_listing_items_help_text(self):
        user = self.global_user1
        form = WishlistListingForm(user=user)
        self.assertEqual(form.fields['items'].help_text, ("At least one " +
            "wishlist item must be selected."))

    #Test to ensure that items field label is correct
    def test_wishlist_listing_items_label(self):
        user = self.global_user1
        form = WishlistListingForm(user=user)
        self.assertEqual(form.fields['items'].label, "Wishlist Items")

    #Test to ensure that itemsOffer field help text is correct
    def test_wishlist_listing_items_offer_help_text(self):
        user = self.global_user1
        form = WishlistListingForm(user=user)
        self.assertEqual(form.fields['itemsOffer'].help_text, ("Items you " +
            "would exchange for wishlist items."))

    #Test to ensure that itemsOffer field label is correct
    def test_wishlist_listing_items_offer_label(self):
        user = self.global_user1
        form = WishlistListingForm(user=user)
        self.assertEqual(form.fields['itemsOffer'].label, "Items Being Offered")

    #Test to ensure that moneyOffer field help text is correct
    def test_wishlist_listing_money_offer_help_text(self):
        user = self.global_user1
        form = WishlistListingForm(user=user)
        self.assertEqual(form.fields['moneyOffer'].help_text, ("Monetary " +
            "amount you would exchange for wishlist items."))

    #Test to ensure that moneyOffer field label is correct
    def test_wishlist_listing_money_offer_label(self):
        user = self.global_user1
        form = WishlistListingForm(user=user)
        self.assertEqual(form.fields['moneyOffer'].label, "Money Being Offered")

#Tests for the form to edit profile
class ProfileFormTest(MyTestCase):
    #Test to ensure a user is able to submit profile form providing all fields
    def test_valid_profile_submission(self):
        bio = "My Biography"
        delivery = True
        delivery_address = "SUNY Potsdam"
        data = {'bio': bio, 'delivery': delivery,
            'deliveryAddress': delivery_address}
        form = ProfileForm(data=data)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is able to submit profile form without a
    #delivery address
    def test_valid_profile_submission_no_address(self):
        bio = "My Biography"
        delivery = False
        data = {'bio': bio, 'delivery': delivery}
        form = ProfileForm(data=data)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to submit profile form if delivery
    #is true and delivery address is missing
    def test_invalid_profile_submission_delivery_true_no_address(self):
        bio = "My Biography"
        delivery = True
        data = {'bio': bio, 'delivery': delivery}
        form = ProfileForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to submit profile form if biography
    #is missing
    def test_invalid_profile_submission_no_bio(self):
        delivery = True
        delivery_address = "SUNY Potsdam"
        data = {'delivery': delivery, 'deliveryAddress': delivery_address}
        form = ProfileForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure that bio field help text is correct
    def test_profile_bio_help_text(self):
        form = ProfileForm()
        self.assertEqual(form.fields['bio'].help_text, ("A biography for " +
            "your profile so others can know you better."))

    #Test to ensure that bio field label is correct
    def test_profile_bio_label(self):
        form = ProfileForm()
        self.assertEqual(form.fields['bio'].label, "Biography")

    #Test to ensure that delivery field help text is correct
    def test_profile_delivery_help_text(self):
        form = ProfileForm()
        self.assertEqual(form.fields['delivery'].help_text, ("Check this " +
            "if you are able to deliver items."))

    #Test to ensure that delivery address field help text is correct
    def test_profile_delivery_address_help_text(self):
        form = ProfileForm()
        self.assertEqual(form.fields['deliveryAddress'].help_text, ("Submit " +
            "an delivery address that you pick up items from.  Required if" +
            " delivery check box is checked."))

    #Test to ensure that delivery address field label is correct
    def test_profile_delivery_address_label(self):
        form = ProfileForm()
        self.assertEqual(form.fields['deliveryAddress'].label, "Delivery Address")

#Tests for the form to create a conversation
class ConversationFormTest(MyTestCase):
    #Test to ensure a user is able to start a conversation providing all fields
    def test_valid_conversation_creation(self):
        topic = "Trade me your stuff"
        message = "I want your stuff for free"
        data = {'topic': topic, 'message': message}
        form = ConversationForm(data=data)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to start a conversation if topic is
    #missing
    def test_invalid_conversation_creation_no_topic(self):
        topic = "Trade me your stuff"
        message = "I want your stuff for free"
        data = {'message': message}
        form = ConversationForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to start a conversation if message is
    #missing
    def test_invalid_conversation_creation_no_topic(self):
        topic = "Trade me your stuff"
        message = "I want your stuff for free"
        data = {'topic': topic}
        form = ConversationForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to start a conversation if topic
    #is too long
    def test_invalid_conversation_creation_topic_too_long(self):
        topic = ("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        message = "I want your stuff for free"
        data = {'topic': topic, 'message': message}
        form = ConversationForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to start a conversation if message
    #is too long
    def test_invalid_conversation_creation_message_too_long(self):
        topic = "Trade me your stuff"
        message = ("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        data = {'topic': topic, 'message': message}
        form = ConversationForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure that topic field help text is correct
    def test_conversation_topic_help_text(self):
        form = ConversationForm()
        self.assertEqual(form.fields['topic'].help_text, ("Topic " +
            "of the conversation."))

    #Test to ensure that message field help text is correct
    def test_message_topic_help_text(self):
        form = ConversationForm()
        self.assertEqual(form.fields['message'].help_text, ("Initiating " +
            "message for the conversation."))

#Tests for the form to send a message
class MessageFormTest(MyTestCase):
    #Test to ensure a user is able to create a message providing all fields
    def test_valid_message_creation(self):
        content = "Can I have your stuff?"
        data = {'content': content}
        form = MessageForm(data=data)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to create a message if content is
    #missing
    def test_invalid_conversation_creation_no_content(self):
        content = "Can I have your stuff?"
        data = {}
        form = MessageForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to start a conversation if message
    #is too long
    def test_invalid_conversation_creation_message_too_long(self):
        content = ("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        data = {'content': content}
        form = MessageForm(data=data)
        self.assertFalse(form.is_valid())

#Tests for the form to report a listing
class ListingReportFormTest(MyTestCase):
    #Test to ensure a user is able to create a listing report providing all fields
    def test_valid_listing_report_creation(self):
        reason = "Malicious Content"
        description = "Illegal items being advertised"
        data = {'reason': reason, 'description': description}
        form = ListingReportForm(data=data)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to create a listing report if fields
    #are not provided
    def test_invalid_listing_report_no_data(self):
        reason = "Malicious Content"
        description = "Illegal items being advertised"
        data = {}
        form = ListingReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a listing report if a
    #reason is not provided
    def test_invalid_listing_report_no_reason(self):
        reason = "Malicious Content"
        description = "Illegal items being advertised"
        data = {'description': description}
        form = ListingReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a listing report if a
    #description is not provided
    def test_invalid_listing_report_no_description(self):
        reason = "Malicious Content"
        description = "Illegal items being advertised"
        data = {'reason': reason}
        form = ListingReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a listing report if a
    #description is too long
    def test_invalid_listing_report_description_too_long(self):
        reason = "Malicious Content"
        description = ("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        data = {'reason': reason, 'description': description}
        form = ListingReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure that reason field help text is correct
    def test_event_report_reason_help_text(self):
        form = ListingReportForm()
        self.assertEqual(form.fields['reason'].help_text, "Reason for the report")

    #Test to ensure that description field help text is correct
    def test_event_report_description_help_text(self):
        form = ListingReportForm()
        self.assertEqual(form.fields['description'].help_text,
            "Tell us more in depth about the reason for reporting")

#Tests for the form to report an event
class EventReportFormTest(MyTestCase):
    #Test to ensure a user is able to create a event report providing all fields
    def test_valid_event_report_creation(self):
        reason = "Malicious Event"
        description = "The event is for a pyramid scheme"
        data = {'reason': reason, 'description': description}
        form = EventReportForm(data=data)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to create a event report if fields
    #are not provided
    def test_invalid_event_report_no_data(self):
        reason = "Malicious Event"
        description = "The event is for a pyramid scheme"
        data = {}
        form = EventReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a event report if a
    #reason is not provided
    def test_invalid_event_report_no_reason(self):
        reason = "Malicious Event"
        description = "The event is for a pyramid scheme"
        data = {'description': description}
        form = EventReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a event report if a
    #description is not provided
    def test_invalid_event_report_no_description(self):
        reason = "Malicious Event"
        description = "The event is for a pyramid scheme"
        data = {'reason': reason}
        form = EventReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a event report if a
    #description is too long
    def test_invalid_event_report_description_too_long(self):
        reason = "Malicious Event"
        description = ("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        data = {'reason': reason, 'description': description}
        form = EventReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure that reason field help text is correct
    def test_event_report_reason_help_text(self):
        form = EventReportForm()
        self.assertEqual(form.fields['reason'].help_text, "Reason for the report")

    #Test to ensure that description field help text is correct
    def test_event_report_description_help_text(self):
        form = EventReportForm()
        self.assertEqual(form.fields['description'].help_text,
            "Tell us more in depth about the reason for reporting")

#Tests for the form to report a user
class UserReportFormTest(MyTestCase):
    #Test to ensure a user is able to create a user report providing all fields
    def test_valid_user_report_creation(self):
        reason = "Malicious User"
        description = "The user is trying to scam me"
        data = {'reason': reason, 'description': description}
        form = UserReportForm(data=data)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to create a user report if fields
    #are not provided
    def test_invalid_user_report_no_data(self):
        reason = "Malicious User"
        description = "The user is trying to scam me"
        data = {}
        form = UserReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a user report if a
    #reason is not provided
    def test_invalid_user_report_no_reason(self):
        reason = "Malicious User"
        description = "The user is trying to scam me"
        data = {'description': description}
        form = UserReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a user report if a
    #description is not provided
    def test_invalid_user_report_no_description(self):
        reason = "Malicious User"
        description = "The user is trying to scam me"
        data = {'reason': reason}
        form = UserReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a user report if a
    #description is too long
    def test_invalid_user_report_description_too_long(self):
        reason = "Malicious User"
        description = ("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        data = {'reason': reason, 'description': description}
        form = UserReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure that reason field help text is correct
    def test_user_report_reason_help_text(self):
        form = UserReportForm()
        self.assertEqual(form.fields['reason'].help_text, "Reason for the report")

    #Test to ensure that description field help text is correct
    def test_user_report_description_help_text(self):
        form = UserReportForm()
        self.assertEqual(form.fields['description'].help_text,
            "Tell us more in depth about the reason for reporting")

#Tests for the form to report a wishlist
class WishlistReportFormTest(MyTestCase):
    #Test to ensure a user is able to create a wishlist report providing all fields
    def test_valid_wishlist_report_creation(self):
        reason = "Malicious Content"
        description = "The items in this wishlist are questionable"
        data = {'reason': reason, 'description': description}
        form = WishlistReportForm(data=data)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to create a wishlist report if fields
    #are not provided
    def test_invalid_wishlist_report_no_data(self):
        reason = "Malicious Content"
        description = "The items in this wishlist are questionable"
        data = {}
        form = WishlistReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a wishlist report if a
    #reason is not provided
    def test_invalid_wishlist_report_no_reason(self):
        reason = "Malicious Content"
        description = "The items in this wishlist are questionable"
        data = {'description': description}
        form = WishlistReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a wishlist report if a
    #description is not provided
    def test_invalid_wishlist_report_no_description(self):
        reason = "Malicious Content"
        description = "The items in this wishlist are questionable"
        data = {'reason': reason}
        form = WishlistReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a wishlist report if a
    #description is too long
    def test_invalid_wishlist_report_description_too_long(self):
        reason = "Malicious Content"
        description = ("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        data = {'reason': reason, 'description': description}
        form = WishlistReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure that reason field help text is correct
    def test_wishlist_report_reason_help_text(self):
        form = WishlistReportForm()
        self.assertEqual(form.fields['reason'].help_text, "Reason for the report")

    #Test to ensure that description field help text is correct
    def test_wishlist_report_description_help_text(self):
        form = WishlistReportForm()
        self.assertEqual(form.fields['description'].help_text,
            "Tell us more in depth about the reason for reporting")

#Tests for the form to report a image
class ImageReportFormTest(MyTestCase):
    #Test to ensure a user is able to create a image report providing all fields
    def test_valid_image_report_creation(self):
        reason = "Malicious Image"
        description = "The image contains questionable objects"
        data = {'reason': reason, 'description': description}
        form = ImageReportForm(data=data)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to create a image report if fields
    #are not provided
    def test_invalid_image_report_no_data(self):
        reason = "Malicious Image"
        description = "The image contains questionable objects"
        data = {}
        form = ImageReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a image report if a
    #reason is not provided
    def test_invalid_image_report_no_reason(self):
        reason = "Malicious Image"
        description = "The image contains questionable objects"
        data = {'description': description}
        form = ImageReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a image report if a
    #description is not provided
    def test_invalid_image_report_no_description(self):
        reason = "Malicious Image"
        description = "The image contains questionable objects"
        data = {'reason': reason}
        form = ImageReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a image report if a
    #description is too long
    def test_invalid_image_report_description_too_long(self):
        reason = "Malicious Image"
        description = ("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        data = {'reason': reason, 'description': description}
        form = ImageReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure that reason field help text is correct
    def test_image_report_reason_help_text(self):
        form = ImageReportForm()
        self.assertEqual(form.fields['reason'].help_text, "Reason for the report")

    #Test to ensure that description field help text is correct
    def test_image_report_description_help_text(self):
        form = ImageReportForm()
        self.assertEqual(form.fields['description'].help_text,
            "Tell us more in depth about the reason for reporting")

#Tests for the form to report a rating
class RatingReportFormTest(MyTestCase):
    #Test to ensure a user is able to create a rating report providing all fields
    def test_valid_rating_report_creation(self):
        reason = "False Rating"
        description = "This rating is not telling the truth"
        data = {'reason': reason, 'description': description}
        form = RatingReportForm(data=data)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to create a rating report if fields
    #are not provided
    def test_invalid_rating_report_no_data(self):
        reason = "False Rating"
        description = "This rating is not telling the truth"
        data = {}
        form = RatingReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a rating report if a
    #reason is not provided
    def test_invalid_rating_report_no_reason(self):
        reason = "False Rating"
        description = "This rating is not telling the truth"
        data = {'description': description}
        form = RatingReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a rating report if a
    #description is not provided
    def test_invalid_rating_report_no_description(self):
        reason = "False Rating"
        description = "This rating is not telling the truth"
        data = {'reason': reason}
        form = RatingReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a rating report if a
    #description is too long
    def test_invalid_rating_report_description_too_long(self):
        reason = "False Rating"
        description = ("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        data = {'reason': reason, 'description': description}
        form = RatingReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure that reason field help text is correct
    def test_rating_report_reason_help_text(self):
        form = RatingReportForm()
        self.assertEqual(form.fields['reason'].help_text, "Reason for the report")

    #Test to ensure that description field help text is correct
    def test_rating_report_description_help_text(self):
        form = RatingReportForm()
        self.assertEqual(form.fields['description'].help_text,
            "Tell us more in depth about the reason for reporting")

#Tests for the form to create a rating
class CreateRatingFormTest(MyTestCase):
    #Test to ensure a user is able to create a rating providing all fields
    def test_valid_rating_creation(self):
        user = self.global_user2
        user2 = self.global_user1
        rating_value = 5
        feedback = ("This user is very trustworthy and honest.  I received " +
            "all my items on time and in the condition advertised.  I would " +
            "definitely do business with them again.")
        data = {'ratingValue': rating_value, 'feedback': feedback,
            'ratingTicket': self.global_rating_ticket.id}
        form = CreateRatingForm(data=data, user=user, receiver=user2)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to create a rating if fields
    #are not provided
    def test_invalid_rating_no_data(self):
        user = self.global_user2
        user2 = self.global_user1
        rating_value = 5
        feedback = ("This user is very trustworthy and honest.  I received " +
            "all my items on time and in the condition advertised.  I would " +
            "definitely do business with them again.")
        data = {}
        form = CreateRatingForm(data=data, user=user, receiver=user2)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a rating if rating value is
    #not provided
    def test_invalid_rating_no_rating_value(self):
        user = self.global_user2
        user2 = self.global_user1
        rating_value = 5
        feedback = ("This user is very trustworthy and honest.  I received " +
            "all my items on time and in the condition advertised.  I would " +
            "definitely do business with them again.")
        data = {'feedback': feedback, 'ratingTicket': self.global_rating_ticket.id}
        form = CreateRatingForm(data=data, user=user, receiver=user2)
        self.assertFalse(form.is_valid())

    #Test to ensure user is able to create a rating if feedback is not provided
    def test_valid_rating_no_feedback(self):
        user = self.global_user2
        user2 = self.global_user1
        rating_value = 5
        feedback = ("This user is very trustworthy and honest.  I received " +
            "all my items on time and in the condition advertised.  I would " +
            "definitely do business with them again.")
        data = {'ratingValue': rating_value,
            'ratingTicket': self.global_rating_ticket.id}
        form = CreateRatingForm(data=data, user=user, receiver=user2)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to create a rating if rating ticket is
    #not provided
    def test_invalid_rating_no_rating_ticket(self):
        user = self.global_user2
        user2 = self.global_user1
        rating_value = 5
        feedback = ("This user is very trustworthy and honest.  I received " +
            "all my items on time and in the condition advertised.  I would " +
            "definitely do business with them again.")
        data = {'ratingValue': rating_value, 'feedback': feedback}
        form = CreateRatingForm(data=data, user=user, receiver=user2)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a rating using rating ticket
    #they are not the rater for
    def test_invalid_rating_not_rater_for_rating_ticket(self):
        user = self.global_user1
        user2 = self.global_user2
        rating_value = 5
        feedback = ("This user is very trustworthy and honest.  I received " +
            "all my items on time and in the condition advertised.  I would " +
            "definitely do business with them again.")
        data = {'ratingValue': rating_value, 'feedback': feedback,
            'ratingTicket': self.global_rating_ticket.id}
        form = CreateRatingForm(data=data, user=user, receiver=user2)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to create a rating if the feedback
    #provided is too long
    def test_invalid_rating_feedback_too_long(self):
        user = self.global_user2
        user2 = self.global_user1
        rating_value = 5
        feedback = ("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        data = {'ratingValue': rating_value, 'feedback': feedback,
            'ratingTicket': self.global_rating_ticket.id}
        form = CreateRatingForm(data=data, user=user, receiver=user2)
        self.assertFalse(form.is_valid())

    #Test to ensure that rating value field help text is correct
    def test_rating_rating_value_help_text(self):
        user = self.global_user2
        user2 = self.global_user1
        form = CreateRatingForm(user=user, receiver=user2)
        self.assertEqual(form.fields['ratingValue'].help_text,
            "Rating for user from 1 to 5, 5 being the best.")

    #Test to ensure that feedback field help text is correct
    def test_rating_feedback_help_text(self):
        user = self.global_user2
        user2 = self.global_user1
        form = CreateRatingForm(user=user, receiver=user2)
        self.assertEqual(form.fields['feedback'].help_text,
            "Leave feedback for the user you're rating.")

    #Test to ensure that rating value field label is correct
    def test_rating_rating_value_label(self):
        user = self.global_user2
        user2 = self.global_user1
        form = CreateRatingForm(user=user, receiver=user2)
        self.assertEqual(form.fields['ratingValue'].label, "Rating")

    #Test to ensure that rating ticket field label is correct
    def test_rating_rating_value_label(self):
        user = self.global_user2
        user2 = self.global_user1
        form = CreateRatingForm(user=user, receiver=user2)
        self.assertEqual(form.fields['ratingTicket'].label, "Listing")

#Tests for the form to take action on a report
class TakeActionOnReportFormTest(MyTestCase):
    def setUp(self):
        super(TakeActionOnReportFormTest, self).setUp()

        #Create some reports for testing with
        self.listingReport = ListingReport.objects.create(
            listing=self.global_offer_listing1, reason="Malicious Content",
            description="The items are of concern", reportType="Listing")
        self.userReport = UserReport.objects.create(
            user=self.global_user1, reason="Malicious User",
            description="This user has bad intentions", reportType="User")

    #Test to ensure an admin can submit form if a reason is provided
    def test_valid_form_for_listing(self):
        reason = "This listing was deleted due to having illegal objects advertised."
        action_taken = "Delete"
        data = {'reason': reason, 'action_taken': action_taken}
        form = TakeActionOnReportForm(data=data)
        self.assertTrue(form.is_valid())

    #Test to ensure an admin can submit form if a reason is provided for a
    #different kind of object
    def test_valid_form_for_user(self):
        reason = "Your profile was cleared for suspicious advertisement."
        action_taken = "Take Manual Action"
        data = {'reason': reason, 'action_taken': action_taken}
        form = TakeActionOnReportForm(data=data)
        self.assertTrue(form.is_valid())

    #Test to ensure an admin cannot submit form if a reason is not provided
    def test_valid_form_no_reason(self):
        reason = "This listing was deleted due to having illegal objects advertised."
        action_taken = "Delete"
        data = {'action_taken': action_taken}
        form = TakeActionOnReportForm(data=data)
        self.assertTrue(form.is_valid())

    #Test to ensure an admin can not submit form if a action to take is
    #not provided
    def test_invalid_form_no_action(self):
        reason = "This listing was deleted due to having illegal objects advertised."
        action_taken = "Delete"
        data = {'reason': reason}
        form = TakeActionOnReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure an admin can not submit form if no data is provided
    def test_invalid_form_no_data(self):
        reason = "This listing was deleted due to having illegal objects advertised."
        action_taken = "Delete"
        data = {}
        form = TakeActionOnReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure an admin can not submit form if reason provided is too long
    def test_invalid_form_reason_too_long(self):
        reason = ("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        action_taken = "Take Manual Action"
        data = {'reason': reason, 'action_taken': action_taken}
        form = TakeActionOnReportForm(data=data)
        self.assertFalse(form.is_valid())

    #Test to ensure that reason field help text is correct
    def test_action_on_report_reason_help_text(self):
        form = TakeActionOnReportForm()
        self.assertEqual(form.fields['reason'].help_text,
            "Reason for taking action on object.")

    #Test to ensure that action taken field help text is correct
    def test_action_on_report_action_taken_help_text(self):
        form = TakeActionOnReportForm()
        self.assertEqual(form.fields['action_taken'].help_text,
            "Action to preform on the object")

    #Test to ensure that reason field label is correct
    def test_action_on_report_reason_label(self):
        form = TakeActionOnReportForm()
        self.assertEqual(form.fields['reason'].label,
            "Reason for Action")

    #Test to ensure that action taken field label is correct
    def test_action_on_report_action_taken_label(self):
        form = TakeActionOnReportForm()
        self.assertEqual(form.fields['action_taken'].label,
            "Action to Take")
