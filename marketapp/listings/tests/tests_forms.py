from django.test import TestCase
from listings.forms import SignUpForm, AddImageForm, AddItemForm, CreateOfferListingForm
from django.core.files.uploadedfile import SimpleUploadedFile
from listings.models import (User, Image, Tag, Item, Listing, OfferListing, AuctionListing)

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

class AddItemFormTest(TestCase):
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
        form = AddItemForm(data=data, user=user)
        self.assertTrue(form.is_valid())

    #Test to ensure a user is not able to upload an item if name is missing
    def test_invalid_item_name_missing(self):
        user = User.objects.get(pk=1)
        image1 = Image.objects.get(id=1)
        image2 = Image.objects.get(id=2)
        description = "An Item to test adding items."
        data = {'description': description, 'images': [str(image1.id), str(image2.id)]}
        form = AddItemForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to upload an item if name is too long
    def test_invalid_item_upload_name_too_long(self):
        user = User.objects.get(pk=1)
        image1 = Image.objects.get(id=1)
        image2 = Image.objects.get(id=2)
        name = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        description = "An Item to test adding items."
        data = {'name': name, 'description': description, 'images': [str(image1.id), str(image2.id)]}
        form = AddItemForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to upload an item if description is too long
    def test_invalid_item_upload_description_too_long(self):
        user = User.objects.get(pk=1)
        image1 = Image.objects.get(id=1)
        image2 = Image.objects.get(id=2)
        name = "My Item"
        description = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        data = {'name': name, 'description': description, 'images': [str(image1.id), str(image2.id)]}
        form = AddItemForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure a user is not able to upload an item if image is missing
    def test_invalid_item_image_missing(self):
        user = User.objects.get(pk=1)
        name = "My Item"
        description = "An Item to test adding items."
        data = {'name': name, 'description': description}
        form = AddItemForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure that name field help text is correct
    def test_item_upload_name_help_text(self):
        user = User.objects.get(pk=1)
        form = AddItemForm(user=user)
        self.assertEqual(form.fields['name'].help_text, "Name for item is required.")

    #Test to ensure that images field help text is correct
    def test_item_upload_image_help_text(self):
        user = User.objects.get(pk=1)
        form = AddItemForm(user=user)
        self.assertEqual(form.fields['images'].help_text, "An image is required.")

class CreateOfferListingFormTest(MyTestCase):
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
        form = CreateOfferListingForm(data=data, user=user)
        self.assertTrue(form.is_valid())

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
        form = CreateOfferListingForm(data=data, user=user)
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
        form = CreateOfferListingForm(data=data, user=user)
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
        form = CreateOfferListingForm(data=data, user=user)
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
        form = CreateOfferListingForm(data=data, user=user)
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
        form = CreateOfferListingForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    #Test to ensure that name field help text is correct
    def test_item_upload_name_help_text(self):
        user = self.global_user1
        form = CreateOfferListingForm(user=user)
        self.assertEqual(form.fields['name'].help_text, "Name for listing is required.")

    #Test to ensure that items field help text is correct
    def test_item_upload_image_help_text(self):
        user = self.global_user1
        form = CreateOfferListingForm(user=user)
        self.assertEqual(form.fields['items'].help_text, "An item is required.")
