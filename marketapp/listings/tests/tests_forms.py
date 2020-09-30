from django.test import TestCase
from listings.forms import (SignUpForm, AddImageForm, ItemForm, OfferListingForm,
    AuctionListingForm, OfferForm, CreateBidForm, EventForm)
from django.core.files.uploadedfile import SimpleUploadedFile
from listings.models import (User, Image, Tag, Item, Listing, OfferListing,
    AuctionListing, Offer, Bid, Event)

from datetime import datetime, timedelta
from django.utils import timezone
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
        self.global_item1 = Item.objects.create(name="Global Item",
            description="A global item for testing", owner=self.global_user1)
        self.global_item1.images.add(self.global_image1)
        self.global_item1.save
        self.global_item2 = Item.objects.create(name="Global Item 2",
            description="Another global item for testing", owner=self.global_user2)
        self.global_item2.images.add(self.global_image2)
        self.global_item2.save

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
    def test_valid_paypal_email(self):
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
    def test_valid_email(self):
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
    def test_valid_paypal_email_length(self):
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
    def test_valid_email_length(self):
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

class CreateBidFormTest(MyTestCase):
    def setUp(self):
        super(CreateBidFormTest, self).setUp()
        user1 = self.global_user1
        user2 = self.global_user2
        user3 = User.objects.create(username="mikey", password="example",
            email="example4@text.com", paypalEmail="example4@text.com",
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
