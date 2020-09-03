from django.test import TestCase
from listings.models import (User, Image, Tag, Item, Listing, OfferListing, AuctionListing)

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import make_aware
from django.conf import settings

# Create your tests here.
class MyTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="mike2", password="example",
            email="example2@text.com", paypalEmail="example2@text.com",
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

class ImagesViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

    #Test to ensure that a user must be logged in to upload image
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('images'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/images/')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('images'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('images'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/images.html')

class AddImageViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

    #Test to ensure that a user must be logged in to upload image
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('images-add'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/images/add')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('images-add'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('images-add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/add_image.html')

    #Test to ensure that a user is able to create the image and have it relate to them
    def test_image_is_created(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('images-add'))
        self.assertEqual(response.status_code, 200)
        image = SimpleUploadedFile(name='art1.png', content=open('listings/imagetest/art1.png', 'rb').read(), content_type='image/png')
        tag1 = Tag.objects.create(name="Test Tag")
        tag2 = Tag.objects.create(name="Test Tag 2")
        name = "My Image"
        post_response = self.client.post(reverse('images-add'),
            data={'image': image, 'name': name, 'tags': [str(tag1.id), str(tag2.id)]})
        self.assertEqual(post_response.status_code, 302)
        new_image = Image.objects.get(id=1)
        self.assertEqual(new_image.owner, post_response.wsgi_request.user)

    #Test to ensure user is redirected to image gallery if form was valid
    def test_image_is_created_redirect(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('images-add'))
        self.assertEqual(response.status_code, 200)
        image = SimpleUploadedFile(name='art1.png', content=open('listings/imagetest/art1.png', 'rb').read(), content_type='image/png')
        tag1 = Tag.objects.create(name="Test Tag")
        tag2 = Tag.objects.create(name="Test Tag 2")
        name = "My Image"
        post_response = self.client.post(reverse('images-add'),
            data={'image': image, 'name': name, 'tags': [str(tag1.id), str(tag2.id)]})
        self.assertEqual(post_response.status_code, 302)
        self.assertRedirects(post_response, '/listings/images/')

class ItemsViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

    #Test to ensure that a user must be logged in to upload image
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('items'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/items/')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('items'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('items'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'items/items.html')

class AddItemViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

    #Test to ensure that a user must be logged in to upload image
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('items-add'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/items/add')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('items-add'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('items-add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'items/add_item.html')

    #Test to ensure that a user is able to create the image and have it relate to them
    def test_item_is_created(self):
        user = User.objects.create_user(username="mikey", password="example",
            email="exampley@text.com", paypalEmail="exampley@text.com",
            invitesOpen=True, inquiriesOpen=True)
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('images-add'))
        self.assertEqual(response.status_code, 200)
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
        post_response = self.client.post(reverse('items-add'),
            data={'name': "My Image", 'description': "A test image",
                'images': [str(test_image1.id), str(test_image2.id)]})
        self.assertEqual(post_response.status_code, 302)
        new_item = Item.objects.get(id=1)
        self.assertEqual(new_item.owner, post_response.wsgi_request.user)

    #Test to ensure user is redirected to image gallery if form was valid
    def test_item_is_created_redirect(self):
        user = User.objects.create_user(username="mikey", password="example",
            email="exampley@text.com", paypalEmail="exampley@text.com",
            invitesOpen=True, inquiriesOpen=True)
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('images-add'))
        self.assertEqual(response.status_code, 200)
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
        post_response = self.client.post(reverse('items-add'),
            data={'name': "My Image", 'description': "A test image",
                'images': [str(test_image1.id), str(test_image2.id)]})
        self.assertEqual(post_response.status_code, 302)
        self.assertRedirects(post_response, '/listings/items/')

class FAQViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

    #Test to ensure that a user must be logged in to view FAQ
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('faq'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/FAQ/')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq/documents.html')

class FAQImagesViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

    #Test to ensure that a user must be logged in to view FAQ
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('faq-images'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/FAQ/images')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-images'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-images'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq/images.html')

class FAQItemsViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

    #Test to ensure that a user must be logged in to view FAQ
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('faq-items'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/FAQ/items')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-items'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-items'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq/items.html')

class OfferListingsViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

    #Test to ensure that a user must be logged in to view listings
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('offer-listings'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/offer-listings/')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('offer-listings'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('offer-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/offer_listings.html')

class OfferListingDetailViewTest(MyTestCase):
    def setUp(self):
        super(OfferListingDetailViewTest, self).setUp()
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)
        date = datetime.today()
        settings.TIME_ZONE
        aware_date = make_aware(date)
        self.offerListing = OfferListing.objects.create(owner=user,
            name="My Items For Offers", description="A few items up for offers",
            openToMoneyOffers=True, minRange=5.00, maxRange=10.00, notes="Just offer",
            endTime=aware_date)
        self.offerListing.items.add = self.global_item1
        self.offerListing.save

    #Test to ensure that a user must be logged in to view listings
    def test_redirect_if_not_logged_in(self):
        listing = self.offerListing
        response = self.client.get(reverse('offer-listing-detail', args=[str(listing.id)]))
        self.assertRedirects(response, '/accounts/login/?next=/listings/offer-listings/3')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        listing = self.offerListing
        response = self.client.get(reverse('offer-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        listing = self.offerListing
        response = self.client.get(reverse('offer-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/offer_listing_detail.html')

class CreateOfferListingViewTest(TestCase):
    def setUp(self):
        super(CreateOfferListingViewTest, self).setUp()
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)
        test_image = SimpleUploadedFile(name='art1.png', content=open('listings/imagetest/art1.png', 'rb').read(), content_type='image/png')
        image = Image.objects.create(owner=user,  image=test_image, name="Test Image")
        tag = Tag.objects.create(name="Test Tag")
        image.tags.add(tag)
        image.save
        self.item = Item.objects.create(name="Global Item",
            description="A global item for testing", owner=user)
        self.item.images.add(image)
        self.item.save

    #Test to ensure that a user must be logged in to upload image
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('create-offer-listing'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/offer-listings/create-offer-listing')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/create_offer_listing.html')

    #Test to ensure that a user is able to create an offer listing and have it relate to them
    def test_offer_listing_is_created(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-offer-listing'),
            data={'name': "My Offer Listing", 'description': "Just a test listing",
                'endTimeChoices': "1h", 'items': [str(self.item.id)],
                'openToMoneyOffers': True, 'minRange': 5.00, 'maxRange': 10.00,
                'notes': "Just offer anything"})
        self.assertEqual(post_response.status_code, 302)
        new_offer_listing = OfferListing.objects.get(id=4)
        self.assertEqual(new_offer_listing.owner, post_response.wsgi_request.user)

    #Test to ensure that an offer listing created to end in 1 hour has correct end time
    def test_offer_listing_is_created_correct_1h(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-offer-listing'),
            data={'name': "My Offer Listing", 'description': "Just a test listing",
                'endTimeChoices': "1h", 'items': [str(self.item.id)],
                'openToMoneyOffers': True, 'minRange': 5.00, 'maxRange': 10.00,
                'notes': "Just offer anything"})
        self.assertEqual(post_response.status_code, 302)
        new_offer_listing = OfferListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=1)
        to_tz = timezone.get_default_timezone()
        new_offer_listing_endtime = new_offer_listing.endTime
        new_offer_listing_endtime = new_offer_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_offer_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that an offer listing created to end in 2 hours has correct end time
    def test_offer_listing_is_created_correct_2h(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-offer-listing'),
            data={'name': "My Offer Listing", 'description': "Just a test listing",
                'endTimeChoices': "2h", 'items': [str(self.item.id)],
                'openToMoneyOffers': True, 'minRange': 5.00, 'maxRange': 10.00,
                'notes': "Just offer anything"})
        self.assertEqual(post_response.status_code, 302)
        new_offer_listing = OfferListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=2)
        to_tz = timezone.get_default_timezone()
        new_offer_listing_endtime = new_offer_listing.endTime
        new_offer_listing_endtime = new_offer_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_offer_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that an offer listing created to end in 4 hours has correct end time
    def test_offer_listing_is_created_correct_4h(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-offer-listing'),
            data={'name': "My Offer Listing", 'description': "Just a test listing",
                'endTimeChoices': "4h", 'items': [str(self.item.id)],
                'openToMoneyOffers': True, 'minRange': 5.00, 'maxRange': 10.00,
                'notes': "Just offer anything"})
        self.assertEqual(post_response.status_code, 302)
        new_offer_listing = OfferListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=4)
        to_tz = timezone.get_default_timezone()
        new_offer_listing_endtime = new_offer_listing.endTime
        new_offer_listing_endtime = new_offer_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_offer_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that an offer listing created to end in 8 hours has correct end time
    def test_offer_listing_is_created_correct_8h(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-offer-listing'),
            data={'name': "My Offer Listing", 'description': "Just a test listing",
                'endTimeChoices': "8h", 'items': [str(self.item.id)],
                'openToMoneyOffers': True, 'minRange': 5.00, 'maxRange': 10.00,
                'notes': "Just offer anything"})
        self.assertEqual(post_response.status_code, 302)
        new_offer_listing = OfferListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=8)
        to_tz = timezone.get_default_timezone()
        new_offer_listing_endtime = new_offer_listing.endTime
        new_offer_listing_endtime = new_offer_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_offer_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that an offer listing created to end in 12 hours has correct end time
    def test_offer_listing_is_created_correct_12h(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-offer-listing'),
            data={'name': "My Offer Listing", 'description': "Just a test listing",
                'endTimeChoices': "12h", 'items': [str(self.item.id)],
                'openToMoneyOffers': True, 'minRange': 5.00, 'maxRange': 10.00,
                'notes': "Just offer anything"})
        self.assertEqual(post_response.status_code, 302)
        new_offer_listing = OfferListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=12)
        to_tz = timezone.get_default_timezone()
        new_offer_listing_endtime = new_offer_listing.endTime
        new_offer_listing_endtime = new_offer_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_offer_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that an offer listing created to end in 1 day has correct end time
    def test_offer_listing_is_created_correct_1d(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-offer-listing'),
            data={'name': "My Offer Listing", 'description': "Just a test listing",
                'endTimeChoices': "1d", 'items': [str(self.item.id)],
                'openToMoneyOffers': True, 'minRange': 5.00, 'maxRange': 10.00,
                'notes': "Just offer anything"})
        self.assertEqual(post_response.status_code, 302)
        new_offer_listing = OfferListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(days=1)
        to_tz = timezone.get_default_timezone()
        new_offer_listing_endtime = new_offer_listing.endTime
        new_offer_listing_endtime = new_offer_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_offer_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that an offer listing created to end in 3 days has correct end time
    def test_offer_listing_is_created_correct_3d(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-offer-listing'),
            data={'name': "My Offer Listing", 'description': "Just a test listing",
                'endTimeChoices': "3d", 'items': [str(self.item.id)],
                'openToMoneyOffers': True, 'minRange': 5.00, 'maxRange': 10.00,
                'notes': "Just offer anything"})
        self.assertEqual(post_response.status_code, 302)
        new_offer_listing = OfferListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(days=3)
        to_tz = timezone.get_default_timezone()
        new_offer_listing_endtime = new_offer_listing.endTime
        new_offer_listing_endtime = new_offer_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_offer_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that an offer listing created to end in 7 days has correct end time
    def test_offer_listing_is_created_correct_7d(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-offer-listing'),
            data={'name': "My Offer Listing", 'description': "Just a test listing",
                'endTimeChoices': "7d", 'items': [str(self.item.id)],
                'openToMoneyOffers': True, 'minRange': 5.00, 'maxRange': 10.00,
                'notes': "Just offer anything"})
        self.assertEqual(post_response.status_code, 302)
        new_offer_listing = OfferListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(days=7)
        to_tz = timezone.get_default_timezone()
        new_offer_listing_endtime = new_offer_listing.endTime
        new_offer_listing_endtime = new_offer_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_offer_listing_endtime.hour, end_time_check.hour)
