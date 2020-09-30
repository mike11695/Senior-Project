from django.test import TestCase
from listings.models import (User, Image, Tag, Item, Listing, OfferListing,
    AuctionListing, Offer, Bid, Event)

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

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

        #Create a global item for each user for testing
        self.global_item1 = Item.objects.create(name="Global Item",
            description="A global item for testing", owner=self.global_user1)
        self.global_item1.images.add(self.global_image1)
        self.global_item1.save
        self.global_item2 = Item.objects.create(name="Global Item 2",
            description="Another global item for testing", owner=self.global_user2)
        self.global_item2.images.add(self.global_image2)
        self.global_item2.save
        self.global_test_image1 = test_image1
        self.global_test_image2 = test_image2

        #Get the current date and time for testing and create active and inactive endtimes
        date_ended = timezone.localtime(timezone.now()) - timedelta(hours=1)
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        #Create a global offer listing that is active
        self.global_offer_listing1 = OfferListing.objects.create(owner=user1, name='Test Offer Listing',
            description="Just a test listing", openToMoneyOffers=True, minRange=5.00,
            maxRange=10.00, notes="Just offer", endTime=date_active)
        self.global_offer_listing1.items.add(self.global_item1)
        self.global_offer_listing1.save

        #Create a global offer listing that is not active
        self.global_offer_listing2 = OfferListing.objects.create(owner=user1, name='Test Offer Listing',
            description="Just a test listing", openToMoneyOffers=True, minRange=5.00,
            maxRange=10.00, notes="Just offer", endTime=date_ended)
        self.global_offer_listing2.items.add(self.global_item1)
        self.global_offer_listing2.save

        #Create a global offer listing that has completed
        self.global_offer_listing3 = OfferListing.objects.create(owner=user1, name='Test Offer Listing',
            description="Just a test listing", openToMoneyOffers=True, minRange=5.00,
            maxRange=10.00, notes="Just offer", endTime=date_ended, listingCompleted=True)
        self.global_offer_listing3.items.add(self.global_item1)
        self.global_offer_listing3.save

        #Create a global auction listing that is active
        self.global_auction_listing1 = AuctionListing.objects.create(owner=user1, name='Test Auction Listing',
            description="Just a test listing", startingBid=5.00, minimumIncrement=1.00, autobuy=25.00,
            endTime=date_active)
        self.global_auction_listing1.items.add(self.global_item1)
        self.global_auction_listing1.save

        #Create a global auction listing that is inactive
        self.global_auction_listing2 = AuctionListing.objects.create(owner=user1, name='Test Auction Listing',
            description="Just a test listing", startingBid=5.00, minimumIncrement=1.00, autobuy=25.00,
            endTime=date_ended)
        self.global_auction_listing2.items.add(self.global_item1)
        self.global_auction_listing2.save

        #Crete a global event
        self.global_event = Event.objects.create(host=self.global_user1,
            title="My Awesome Event", context="Please come to my event.",
            date="2020-11-06 15:00", location="1234 Sesame Street")
        self.global_event.participants.add(self.global_user2)
        self.global_event.save

class ImagesViewTest(MyTestCase):
    def setUp(self):
        super(ImagesViewTest, self).setUp()
        user1 = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)
        user2 = User.objects.create_user(username="mikey", password="example",
            email="example1@text.com", paypalEmail="example1@text.com",
            invitesOpen=True, inquiriesOpen=True)

        number_of_images_user1 = 5
        number_of_images_user2 = 2
        tag = Tag.objects.create(name="Test Tag")
        test_image = self.global_test_image1

        for num in range(number_of_images_user1):
            image = Image.objects.create(owner=user1, image=test_image,
                name='Test Image #{0}'.format(num))
            image.tags.add(tag)
            image.save

        for num in range(number_of_images_user2):
            image = Image.objects.create(owner=user2, image=test_image,
                name='Test Image #{0}'.format(num))
            image.tags.add(tag)
            image.save

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

    #Test to ensure that the user only sees images they've uploaded for user1
    def test_list_only_current_users_images_user1(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('images'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['images']) == 5)

    #Test to ensure that the user only sees images they've uploaded for user2
    def test_list_only_current_users_images_user2(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('images'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['images']) == 2)

class ImageDetailViewTest(MyTestCase):
    def setUp(self):
        super(ImageDetailViewTest, self).setUp()
        user1 = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)
        user2 = User.objects.create_user(username="mikey", password="example",
            email="example2@text.com", paypalEmail="example2@text.com",
            invitesOpen=True, inquiriesOpen=True)
        tag = Tag.objects.create(name="Test Tag")
        test_image = self.global_test_image1
        self.image = Image.objects.create(owner=user1, image=test_image, name='Test Image')
        self.image.tags.add(tag)
        self.image.save

    #Test to ensure that a user must be logged in to view images
    def test_redirect_if_not_logged_in(self):
        image = self.image
        response = self.client.get(reverse('image-detail', args=[str(image.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        image = self.image
        response = self.client.get(reverse('image-detail', args=[str(image.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if they are not the user that owns the image
    def test_redirect_if_logged_in_but_incorrect_user(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        image = self.image
        response = self.client.get(reverse('image-detail', args=[str(image.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        image = self.image
        response = self.client.get(reverse('image-detail', args=[str(image.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/image_detail.html')

class AddImageViewTest(MyTestCase):
    def setUp(self):
        super(AddImageViewTest, self).setUp()
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)
        self.test_image = self.global_test_image1

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
        new_image = Image.objects.last()
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

class EditImageViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to edit an image
    def test_redirect_if_not_logged_in(self):
        image = self.global_image1
        response = self.client.get(reverse('edit-image', args=[str(image.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in and owns image
    def test_no_redirect_if_logged_in_owner(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        image = self.global_image1
        response = self.client.get(reverse('edit-image', args=[str(image.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in but does not own image
    def test_redirect_if_logged_in_not_owner(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        image = self.global_image1
        response = self.client.get(reverse('edit-image', args=[str(image.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        image = self.global_image1
        response = self.client.get(reverse('edit-image', args=[str(image.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/edit_image.html')

    #Test to ensure that a user is able to edit the image successfully
    def test_item_is_updated(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        image = self.global_image1
        response = self.client.get(reverse('edit-image', args=[str(image.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('edit-image', args=[str(image.id)]),
            data={'name': "My Edited Image", 'tags': [str(self.tag.id)]})
        self.assertEqual(post_response.status_code, 302)
        edited_image = Image.objects.get(id=image.id)
        self.assertEqual(edited_image.name, 'My Edited Image')

    #Test to ensure that a user is not able to edit the image successfully without a name
    def test_item_is_not_updated_no_name(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        image = self.global_image1
        response = self.client.get(reverse('edit-image', args=[str(image.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('edit-image', args=[str(image.id)]),
            data={'tags': [str(self.tag.id)]})
        self.assertEqual(post_response.status_code, 200)

    #Test to ensure that a user is able to edit the image successfully without tags
    def test_item_is_updated_no_tags(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        image = self.global_image1
        response = self.client.get(reverse('edit-image', args=[str(image.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('edit-image', args=[str(image.id)]),
            data={'name': "My Edited Image"})
        self.assertEqual(post_response.status_code, 302)
        edited_image = Image.objects.get(id=image.id)
        self.assertEqual(edited_image.name, 'My Edited Image')

class ImageDeleteViewTest(MyTestCase):
    def setUp(self):
        super(ImageDeleteViewTest, self).setUp()

        #Create an image object to test for deletion
        test_image = SimpleUploadedFile(name='art1.png',
            content=open('listings/imagetest/art1.png', 'rb').read(), content_type='image/png')
        self.image = Image.objects.create(owner=self.global_user1,
            image=test_image, name="Test Image")
        self.image_id = self.image.id

        #create an item object to test that it will be deleted after having the sole image deleted
        self.item =  Item.objects.create(name="Item to Delete",
            description="A item to test deletion", owner=self.global_user1)
        self.item.images.add = self.image
        self.item.save
        self.item_id = self.item.id

        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        #Create an offer listing to test for deletion
        self.offer_listing = OfferListing.objects.create(owner=self.global_user1, name='Test Offer Listing',
            description="Just a test listing", openToMoneyOffers=True, minRange=5.00,
            maxRange=10.00, notes="Just offer", endTime=date_active)
        self.offer_listing.items.add(self.item)
        self.offer_listing.save
        self.offer_listing_id = self.offer_listing.id

        #create an auction listing to test for deletion
        self.auction_listing = AuctionListing.objects.create(owner=self.global_user1, name='Test Auction Listing',
            description="Just a test listing", startingBid=5.00, minimumIncrement=1.00, autobuy= 25.00,
            endTime=date_active)
        self.auction_listing.items.add(self.item)
        self.auction_listing.save
        self.auction_listing_id = self.auction_listing.id

    #Test to ensure that a user must be logged in to delete an image
    def test_redirect_if_not_logged_in(self):
        image = self.image
        response = self.client.get(reverse('delete-image', args=[str(image.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in if they own the image
    def test_no_redirect_if_logged_in_owner(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        image = self.image
        response = self.client.get(reverse('delete-image', args=[str(image.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged but they do not own the image
    def test_no_redirect_if_logged_in_not_owner(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        image = self.image
        response = self.client.get(reverse('delete-image', args=[str(image.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        image = self.image
        response = self.client.get(reverse('delete-image', args=[str(image.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/image_delete.html')

    #Test to ensure object is deleted if user confirms as well as items that contain the image
    #as its sole image and listings that contained the item
    def test_succesful_deletion(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        image = self.image
        post_response = self.client.post(reverse('delete-image', args=[str(image.id)]))
        self.assertRedirects(post_response, reverse('images'))
        self.assertFalse(Image.objects.filter(id=self.image_id).exists())
        self.assertFalse(Item.objects.filter(id=self.item_id).exists())
        self.assertFalse(OfferListing.objects.filter(id=self.offer_listing_id).exists())
        self.assertFalse(AuctionListing.objects.filter(id=self.auction_listing_id).exists())
        self.assertTrue(Item.objects.filter(id=self.global_item1.id).exists())

class ItemsViewTest(MyTestCase):
    def setUp(self):
        super(ItemsViewTest, self).setUp()
        user1 = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)
        user2 = User.objects.create_user(username="mikey", password="example",
            email="example1@text.com", paypalEmail="example1@text.com",
            invitesOpen=True, inquiriesOpen=True)

        number_of_items_user1 = 3
        number_of_items_user2 = 6
        tag = Tag.objects.create(name="Test Tag")
        test_image = self.global_test_image1
        image1 = Image.objects.create(owner=user1, image=test_image, name='Test Image')
        image1.tags.add(tag)
        image1.save
        image2 = Image.objects.create(owner=user2, image=test_image, name='Test Image')
        image2.tags.add(tag)
        image2.save

        for num in range(number_of_items_user1):
            item = Item.objects.create(name='Item #{0}'.format(num),
                description="Just an item", owner=user1)
            item.images.add(image1)
            item.save

        for num in range(number_of_items_user2):
            item = Item.objects.create(name='Item #{0}'.format(num),
                description="Just an item", owner=user2)
            item.images.add(image2)
            item.save

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

    #Test to ensure that the user only sees items they've uploaded for user1
    def test_list_only_current_users_items_user1(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('items'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['items']) == 3)

    #Test to ensure that the user only sees items they've uploaded for user2
    def test_list_only_current_users_items_user2(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('items'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['items']) == 6)

class ItemDetailViewTest(MyTestCase):
    def setUp(self):
        super(ItemDetailViewTest, self).setUp()
        user1 = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)
        user2 = User.objects.create_user(username="mikey", password="example",
            email="example2@text.com", paypalEmail="example2@text.com",
            invitesOpen=True, inquiriesOpen=True)
        tag = Tag.objects.create(name="Test Tag")
        test_image = self.global_test_image1
        image = Image.objects.create(owner=user1, image=test_image, name='Test Image')
        self.item = Item.objects.create(name='Test Item', description="Just an item", owner=user1)
        self.item.images.add(image)
        self.item.save

    #Test to ensure that a user must be logged in to view items
    def test_redirect_if_not_logged_in(self):
        item = self.item
        response = self.client.get(reverse('item-detail', args=[str(item.id)]))
        self.assertRedirects(response, '/accounts/login/?next=/listings/items/{0}'.format(item.id))

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        item = self.item
        response = self.client.get(reverse('item-detail', args=[str(item.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        item = self.item
        response = self.client.get(reverse('item-detail', args=[str(item.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'items/item_detail.html')

class AddItemViewTest(MyTestCase):
    def setUp(self):
        super(AddItemViewTest, self).setUp()
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)
        self.test_image1 = self.global_test_image1
        self.test_image2 = self.global_test_image2

    #Test to ensure that a user must be logged in to create item
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

    #Test to ensure that a user is able to create the item and have it relate to them
    def test_item_is_created(self):
        user = User.objects.create_user(username="mikey", password="example",
            email="exampley@text.com", paypalEmail="exampley@text.com",
            invitesOpen=True, inquiriesOpen=True)
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('images-add'))
        self.assertEqual(response.status_code, 200)
        image1 = self.test_image1
        image2 = self.test_image2
        tag1 = Tag.objects.create(name="Test Tag")
        tag2 = Tag.objects.create(name="Test Tag 2")
        my_test_image1 = Image.objects.create(owner=user,
            image=image1, name="Test Image 1")
        my_test_image1.tags.add(tag1)
        my_test_image1.tags.add(tag2)
        my_test_image1.save
        my_test_image2 = Image.objects.create(owner=user,
            image=image2, name="Test Image 2")
        my_test_image2.tags.add(tag1)
        my_test_image2.save
        post_response = self.client.post(reverse('items-add'),
            data={'name': "My Image", 'description': "A test image",
                'images': [str(my_test_image1.id), str(my_test_image2.id)]})
        self.assertEqual(post_response.status_code, 302)
        new_item = Item.objects.last()
        self.assertEqual(new_item.owner, post_response.wsgi_request.user)

    #Test to ensure user is redirected to item list if form was valid
    def test_item_is_created_redirect(self):
        user = User.objects.create_user(username="mikey", password="example",
            email="exampley@text.com", paypalEmail="exampley@text.com",
            invitesOpen=True, inquiriesOpen=True)
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('images-add'))
        self.assertEqual(response.status_code, 200)
        image1 = self.test_image1
        image2 = self.test_image2
        tag1 = Tag.objects.create(name="Test Tag")
        tag2 = Tag.objects.create(name="Test Tag 2")
        my_test_image1 = Image.objects.create(owner=user,
            image=image1, name="Test Image 1")
        my_test_image1.tags.add(tag1)
        my_test_image1.tags.add(tag2)
        my_test_image1.save
        my_test_image2 = Image.objects.create(owner=user,
            image=image2, name="Test Image 2")
        my_test_image2.tags.add(tag1)
        my_test_image2.save
        post_response = self.client.post(reverse('items-add'),
            data={'name': "My Image", 'description': "A test image",
                'images': [str(my_test_image1.id), str(my_test_image2.id)]})
        self.assertEqual(post_response.status_code, 302)
        self.assertRedirects(post_response, '/listings/items/')

class EditItemViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to edit an item
    def test_redirect_if_not_logged_in(self):
        item = self.global_item1
        response = self.client.get(reverse('edit-item', args=[str(item.id)]))
        self.assertRedirects(response, '/accounts/login/?next=/listings/items/{0}/edit'.format(item.id))

    #Test to ensure user is not redirected if logged in and owns item
    def test_no_redirect_if_logged_in_owner(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.global_item1
        response = self.client.get(reverse('edit-item', args=[str(item.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in but does not own item
    def test_redirect_if_logged_in_not_owner(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        item = self.global_item1
        response = self.client.get(reverse('edit-item', args=[str(item.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.global_item1
        response = self.client.get(reverse('edit-item', args=[str(item.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'items/edit_item.html')

    #Test to ensure that a user is able to edit the image successfully
    def test_item_is_updated(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.global_item1
        response = self.client.get(reverse('edit-item', args=[str(item.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('edit-item', args=[str(item.id)]),
            data={'name': "My Edited Item", 'description': "Updating an item",
                'images': [str(self.global_image1.id)]})
        self.assertEqual(post_response.status_code, 302)
        edited_item = Item.objects.get(id=item.id)
        self.assertEqual(edited_item.name, 'My Edited Item')

class ItemDeleteViewTest(MyTestCase):
    def setUp(self):
        super(ItemDeleteViewTest, self).setUp()
        #Create an item object to test for deletion
        self.item =  Item.objects.create(name="Item to Delete",
            description="A item to test deletion", owner=self.global_user1)
        self.item.images.add = self.global_image1
        self.item.save
        self.item_id = self.item.id

        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        #Create an offer listing to test for deletion
        self.offer_listing = OfferListing.objects.create(owner=self.global_user1, name='Test Offer Listing',
            description="Just a test listing", openToMoneyOffers=True, minRange=5.00,
            maxRange=10.00, notes="Just offer", endTime=date_active)
        self.offer_listing.items.add(self.item)
        self.offer_listing.save
        self.offer_listing_id = self.offer_listing.id

        #create an auction listing to test for deletion
        self.auction_listing = AuctionListing.objects.create(owner=self.global_user1, name='Test Auction Listing',
            description="Just a test listing", startingBid=5.00, minimumIncrement=1.00, autobuy= 25.00,
            endTime=date_active)
        self.auction_listing.items.add(self.item)
        self.auction_listing.save
        self.auction_listing_id = self.auction_listing.id

    #Test to ensure that a user must be logged in to delete an item
    def test_redirect_if_not_logged_in(self):
        item = self.item
        response = self.client.get(reverse('delete-item', args=[str(item.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in if they own the listing
    def test_no_redirect_if_logged_in_owner(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.item
        response = self.client.get(reverse('delete-item', args=[str(item.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged but they do not own the item
    def test_no_redirect_if_logged_in_not_owner(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        item = self.item
        response = self.client.get(reverse('delete-item', args=[str(item.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.item
        response = self.client.get(reverse('delete-item', args=[str(item.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'items/item_delete.html')

    #Test to ensure object is deleted if user confirms as well as listings that contained the item
    def test_succesful_deletion(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.item
        post_response = self.client.post(reverse('delete-item', args=[str(item.id)]))
        self.assertRedirects(post_response, reverse('items'))
        self.assertFalse(Item.objects.filter(id=self.item_id).exists())
        self.assertFalse(OfferListing.objects.filter(id=self.offer_listing_id).exists())
        self.assertFalse(AuctionListing.objects.filter(id=self.auction_listing_id).exists())
        self.assertTrue(OfferListing.objects.filter(id=self.global_offer_listing1.id).exists())
        self.assertTrue(AuctionListing.objects.filter(id=self.global_auction_listing1.id).exists())

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

class FAQListingsViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

    #Test to ensure that a user must be logged in to view FAQ
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('faq-listings'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/FAQ/listings')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-listings'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq/listings.html')

class FAQEventsViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to view FAQ
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('faq-events'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/FAQ/events')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-events'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-events'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq/events.html')

class OfferListingsViewTest(MyTestCase):
    def setUp(self):
        super(OfferListingsViewTest, self).setUp()
        user1 = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)
        user2 = User.objects.create_user(username="mikey", password="example",
            email="example1@text.com", paypalEmail="example1@text.com",
            invitesOpen=True, inquiriesOpen=True)

        number_of_listings_user1 = 4
        number_of_listings_user2 = 5
        tag = Tag.objects.create(name="Test Tag")
        test_image = self.global_test_image1
        image1 = Image.objects.create(owner=user1, image=test_image, name='Test Image')
        image1.tags.add(tag)
        image1.save
        image2 = Image.objects.create(owner=user2, image=test_image, name='Test Image')
        image2.tags.add(tag)
        image2.save
        item1 = Item.objects.create(name='Test Item', description="Just an item", owner=user1)
        item1.images.add(image1)
        item1.save
        item2 = Item.objects.create(name='Test Item', description="Just an item", owner=user2)
        item2.images.add(image2)
        item2.save

        date = datetime.today()
        settings.TIME_ZONE
        aware_date = make_aware(date)

        for num in range(number_of_listings_user1):
            listing = OfferListing.objects.create(owner=user1,
                name='Test Offer Listing #{0}'.format(num), description="Just a test listing",
                openToMoneyOffers=True, minRange=5.00, maxRange=10.00, notes="Just offer",
                endTime=aware_date)
            listing.items.add(item1)
            listing.save

        for num in range(number_of_listings_user2):
            listing = OfferListing.objects.create(owner=user2,
                name='Test Offer Listing #{0}'.format(num), description="Just a test listing",
                openToMoneyOffers=True, minRange=5.00, maxRange=10.00, notes="Just offer",
                endTime=aware_date)
            listing.items.add(item2)
            listing.save

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

    #Test to ensure that the user only sees listings they've uploaded for user1
    def test_list_only_current_users_listings_user1(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('offer-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['offerlistings']) == 4)

    #Test to ensure that the user only sees listings they've uploaded for user2
    def test_list_only_current_users_listings_user2(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('offer-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['offerlistings']) == 5)

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

        #create some offers for the listing
        number_of_offers = 5

        for offer in range(number_of_offers):
            new_offer = Offer.objects.create(offerListing=self.offerListing, owner=self.global_user2,
                amount=7.00)
            new_offer.items.add(self.global_item2)
            new_offer.save

        #A completed listing offer for testing redirects
        completed_offer = Offer.objects.create(offerListing=self.global_offer_listing3, owner=self.global_user2,
            amount=7.00)
        completed_offer.items.add(self.global_item2)
        completed_offer.save

    #Test to ensure that a user must be logged in to view listings
    def test_redirect_if_not_logged_in(self):
        listing = self.offerListing
        response = self.client.get(reverse('offer-listing-detail', args=[str(listing.id)]))
        self.assertRedirects(response, '/accounts/login/?next=/listings/offer-listings/{0}'.format(listing.id))

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

    #Test that the owner can see all offers on the listing
    def test_owner_can_see_offers(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        listing = self.offerListing
        response = self.client.get(reverse('offer-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['offers']) == 5)

    #Test that a user that does not own the listing cannot see offers
    def test_not_owner_can_not_see_offers(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.offerListing
        response = self.client.get(reverse('offer-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['offers'] == None)

    #Test to ensure a user is redirected if a listing has completed and they are not the owner or offerer
    def test_redirect_if_not_owner_or_accepted_offer_listing_completed(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        listing = self.global_offer_listing3
        response = self.client.get(reverse('offer-listing-detail', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure a user is not redirected if a listing has completed and they are the owner of listing
    def test_no_redirect_if_listing_owner_listing_completed(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.global_offer_listing3
        response = self.client.get(reverse('offer-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure a user is not redirected if a listing has completed and they are the owner of accepted offer
    def test_no_redirect_if_accepted_owner_listing_completed(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        listing = self.global_offer_listing3
        response = self.client.get(reverse('offer-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

class AllOfferListingsViewTest(MyTestCase):
    def setUp(self):
        super(AllOfferListingsViewTest, self).setUp()

        #Create a variety of listings to test with
        #Number of active listings should be 10 as there is a global active listing
        number_of_active_listings_user1 = 4
        number_of_active_listings_user2 = 5
        number_of_inactive_listings_user1 = 2
        number_of_completed_listings_user2 = 3

        self.num_active_listings = 10

        date_ended = timezone.localtime(timezone.now()) - timedelta(hours=1)
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        for num in range(number_of_active_listings_user1):
            listing = OfferListing.objects.create(owner=self.global_user1,
                name='Test Offer Listing #{0}'.format(num), description="Just a test listing",
                openToMoneyOffers=True, minRange=5.00, maxRange=10.00, notes="Just offer",
                endTime=date_active)
            listing.items.add(self.global_item1)
            listing.save

        for num in range(number_of_active_listings_user2):
            listing = OfferListing.objects.create(owner=self.global_user2,
                name='Test Offer Listing #{0}'.format(num), description="Just a test listing",
                openToMoneyOffers=True, minRange=5.00, maxRange=10.00, notes="Just offer",
                endTime=date_active)
            listing.items.add(self.global_item2)
            listing.save

        for num in range(number_of_inactive_listings_user1):
            listing = OfferListing.objects.create(owner=self.global_user1,
                name='Test Offer Listing #{0}'.format(num), description="Just a test listing",
                openToMoneyOffers=True, minRange=5.00, maxRange=10.00, notes="Just offer",
                endTime=date_ended)
            listing.items.add(self.global_item1)
            listing.save

        for num in range(number_of_completed_listings_user2):
            listing = OfferListing.objects.create(owner=self.global_user2,
                name='Test Offer Listing #{0}'.format(num), description="Just a test listing",
                openToMoneyOffers=True, minRange=5.00, maxRange=10.00, notes="Just offer",
                endTime=date_active, listingCompleted=True)
            listing.items.add(self.global_item2)
            listing.save

    #Test to ensure that a user must be logged in to view listings
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('all-offer-listings'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/offer-listings/all')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('all-offer-listings'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('all-offer-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/all_offer_listings.html')

    #Test to ensure that a user sees the correct amount of active listings
    def test_list_only_active_listings(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('all-offer-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['offerlistings']), self.num_active_listings)

    #Test to ensure that  different user sees the correct amount of active listings
    def test_list_only_active_listings_new_user(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('all-offer-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['offerlistings']), self.num_active_listings)

class MyOffersViewTest(MyTestCase):
    def setUp(self):
        super(MyOffersViewTest, self).setUp()
        #Create a user for testing with
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

        #Set the amount of offers to be made to test
        number_of_offers_user1 = 3
        number_of_offers_user2 = 8

        #Create the required amount of offers for user 1
        for num in range(number_of_offers_user1):
            offer = Offer.objects.create(offerListing=self.global_offer_listing1, owner=user,
                amount=7.00)

        #Create the required amount of offers for user 2
        for num in range(number_of_offers_user2):
            offer = Offer.objects.create(offerListing=self.global_offer_listing1, owner=self.global_user2,
                amount=7.00)
            offer.items.add(self.global_item2)
            offer.save

    #Test to ensure that a user must be logged in view offers
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my-offers'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/offer-listings/my-offers')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('my-offers'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('my-offers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/offers.html')

    #Test to ensure that the user only sees offers they have made for first user
    def test_list_only_current_users_offers_user1(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('my-offers'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['offers']) == 3)

    #Test to ensure that the user only sees offers they have made for the second user
    def test_list_only_current_users_offers_user2(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('my-offers'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['offers']) == 8)

class CreateOfferListingViewTest(MyTestCase):
    def setUp(self):
        super(CreateOfferListingViewTest, self).setUp()
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)
        test_image = self.global_test_image1
        image = Image.objects.create(owner=user,  image=test_image, name="Test Image")
        tag = Tag.objects.create(name="Test Tag")
        image.tags.add(tag)
        image.save
        self.item = Item.objects.create(name="Global Item",
            description="A global item for testing", owner=user)
        self.item.images.add(image)
        self.item.save

    #Test to ensure that a user must be logged in to create offer listing
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
        new_offer_listing = OfferListing.objects.last()
        self.assertEqual(new_offer_listing.owner, post_response.wsgi_request.user)
        self.assertEqual(new_offer_listing.minRange, 5.00)
        self.assertEqual(new_offer_listing.maxRange, 10.00)

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

    #Test to ensure that an offer listing has minRange and maxRange set to 0.00 if no money is wanted
    def test_offer_listing_ranges_set_to_0(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-offer-listing'),
            data={'name': "My Offer Listing", 'description': "Just a test listing",
                'endTimeChoices': "1h", 'items': [str(self.item.id)],
                'openToMoneyOffers': False, 'minRange': 5.00, 'maxRange': 10.00,
                'notes': "Just offer anything"})
        self.assertEqual(post_response.status_code, 302)
        new_offer_listing = OfferListing.objects.last()
        self.assertEqual(new_offer_listing.minRange, 0.00)
        self.assertEqual(new_offer_listing.maxRange, 0.00)

    #Test to ensure that maxRange is set to 0.00 if t was left blank and listing is open to money offers
    def test_offer_listing_ranges_set_to_0(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-offer-listing'),
            data={'name': "My Offer Listing", 'description': "Just a test listing",
                'endTimeChoices': "1h", 'items': [str(self.item.id)],
                'openToMoneyOffers': True, 'minRange': 5.00, 'notes': "Just offer anything"})
        self.assertEqual(post_response.status_code, 302)
        new_offer_listing = OfferListing.objects.last()
        self.assertEqual(new_offer_listing.minRange, 5.00)
        self.assertEqual(new_offer_listing.maxRange, 0.00)

class EditOfferListingViewTest(MyTestCase):
    def setUp(self):
        super(EditOfferListingViewTest, self).setUp()

        #Create users for testing
        user1 = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)
        user2 = User.objects.create_user(username="mikey", password="example",
            email="example1@text.com", paypalEmail="example1@text.com",
            invitesOpen=True, inquiriesOpen=True)

        #Create objects needed for the new listing to be made
        tag = Tag.objects.create(name="Test Tag")
        test_image = self.global_test_image1

        image1 = Image.objects.create(owner=user1, image=test_image, name='Test Image')
        image1.tags.add(tag)
        image1.save
        self.item1 = Item.objects.create(name='Test Item', description="Just an item", owner=user1)
        self.item1.images.add(image1)
        self.item1.save

        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        #Create a listing for testing
        self.offerListing = OfferListing.objects.create(owner=user1, name='Test Offer Listing',
            description="Just a test listing", openToMoneyOffers=True, minRange=5.00,
            maxRange=10.00, notes="Just offer", endTime=date_active)
        self.offerListing.items.add(self.item1)
        self.offerListing.save

        #Make an offer for a listing to ensure that users can not edit listings with offers
        new_offer = Offer.objects.create(offerListing=self.global_offer_listing1, owner=self.global_user2,
            amount=7.00)
        new_offer.items.add(self.global_item2)
        new_offer.save

    #Test to ensure that a user must be logged in to view the listing
    def test_redirect_if_not_logged_in(self):
        listing = self.offerListing
        response = self.client.get(reverse('update-offer-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/accounts/login/?next=/listings/offer-listings/{0}/update'.format(listing.id))

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        listing = self.offerListing
        response = self.client.get(reverse('update-offer-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        listing = self.offerListing
        response = self.client.get(reverse('update-offer-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/update_offer_listing.html')

    #Test to ensure user is redirected if they are not the user that owns the listing
    def test_redirect_if_logged_in_but_incorrect_user(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        listing = self.offerListing
        response = self.client.get(reverse('update-offer-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is redirected if they own listing but it currently has at least one offer
    def test_redirect_if_logged_in_but_listing_has_offers(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.global_offer_listing1
        response = self.client.get(reverse('update-offer-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/offer-listings/')

    #Test to ensure user is redirected if they own listing but it has already been completed
    def test_redirect_if_logged_in_but_listing_has_completed(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.global_offer_listing3
        response = self.client.get(reverse('update-offer-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/offer-listings/')

    #Test to ensure user is redirected if they own listing but it has already ended
    def test_redirect_if_logged_in_but_listing_has_ended(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.global_offer_listing2
        response = self.client.get(reverse('update-offer-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/offer-listings/')

    #Test to ensure that updating the listing works
    def test_succesful_listing_update(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        listing = self.offerListing
        response = self.client.get(reverse('update-offer-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('update-offer-listing', args=[str(listing.id)]),
            data={'name': "Test Offer Listing Edit", 'description': "Just a test listing",
                'items': [str(self.item1.id)], 'openToMoneyOffers': False, 'notes': "Just offer anything"})
        self.assertEqual(post_response.status_code, 302)
        edited_listing = OfferListing.objects.get(id=listing.id)
        self.assertEqual(edited_listing.name, 'Test Offer Listing Edit')
        self.assertEqual(edited_listing.minRange, 0.00)
        self.assertEqual(edited_listing.maxRange, 0.00)

class RelistOfferListingViewTest(MyTestCase):
    def setUp(self):
        super(RelistOfferListingViewTest, self).setUp()

        #create some offers for the listing to test they are deleted when listing is relisted
        number_of_offers = 6

        for offer in range(number_of_offers):
            new_offer = Offer.objects.create(offerListing=self.global_offer_listing2, owner=self.global_user2,
                amount=7.00)
            new_offer.items.add(self.global_item2)
            new_offer.save

    #Test to ensure that a user must be logged in to relist a listing
    def test_redirect_if_not_logged_in(self):
        listing = self.global_offer_listing2
        response = self.client.get(reverse('relist-offer-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/accounts/login/?next=/listings/offer-listings/{0}/relist'.format(listing.id))

    #Test to ensure user is not redirected if logged in and they own the listing
    def test_no_redirect_if_logged_in_and_owns_listing(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.global_offer_listing2
        response = self.client.get(reverse('relist-offer-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in but they do not own the listing
    def test_no_redirect_if_logged_in_but_does_not_own_listing(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        listing = self.global_offer_listing2
        response = self.client.get(reverse('relist-offer-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is redirected if logged in and they own the listing, but it is active
    def test_redirect_if_logged_in_and_owns_listing_active_listing(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.global_offer_listing1
        response = self.client.get(reverse('relist-offer-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/offer-listings/')

    #Test to ensure user is redirected if logged in and they own the listing, but it has been completed
    def test_redirect_if_logged_in_and_owns_listing_completed_listing(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.global_offer_listing3
        response = self.client.get(reverse('relist-offer-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/offer-listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.global_offer_listing2
        response = self.client.get(reverse('relist-offer-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/relist_offer_listing.html')

    #Test to ensure that relisting the listing works
    def test_succesful_listing_relist(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.global_offer_listing2
        response = self.client.get(reverse('relist-offer-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('relist-offer-listing', args=[str(listing.id)]),
            data={'name': "Test Offer Listing Relist", 'description': "Relisting my listing",
                'items': [str(self.global_item1.id)], 'endTimeChoices': "8h", 'openToMoneyOffers': True,
                'minRange': 15.00, 'maxRange': 20.00, 'notes': "Just offer anything"})
        self.assertEqual(post_response.status_code, 302)
        relisted_listing = OfferListing.objects.get(id=listing.id)
        self.assertEqual(relisted_listing.name, 'Test Offer Listing Relist')
        self.assertEqual(relisted_listing.minRange, 15.00)
        self.assertEqual(relisted_listing.maxRange, 20.00)
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=8)
        to_tz = timezone.get_default_timezone()
        self.assertEqual(relisted_listing.endTime.astimezone(to_tz).hour, end_time_check.hour)

    #Test to ensure that previous offers were deleted upon succesful relisting
    def test_succesful_listing_relist_offers_deleted(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.global_offer_listing2
        response = self.client.get(reverse('relist-offer-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('relist-offer-listing', args=[str(listing.id)]),
            data={'name': "Test Offer Listing Relist", 'description': "Relisting my listing",
                'items': [str(self.global_item1.id)], 'endTimeChoices': "8h", 'openToMoneyOffers': True,
                'minRange': 15.00, 'maxRange': 20.00, 'notes': "Just offer anything"})
        self.assertEqual(post_response.status_code, 302)
        relisted_listing = OfferListing.objects.get(id=listing.id)
        self.assertFalse(Offer.objects.filter(offerListing=relisted_listing).exists())

class OfferListingDeleteViewTest(MyTestCase):
    def setUp(self):
        super(OfferListingDeleteViewTest, self).setUp()
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

        #Create an offer listing object to test for deletion
        self.offerListing = OfferListing.objects.create(owner=user,
            name="My Items For Offers", description="A few items up for offers",
            openToMoneyOffers=True, minRange=5.00, maxRange=10.00, notes="Just offer")
        self.offerListing.items.add = self.global_item1
        self.offerListing.save
        self.listingID = self.offerListing.id

        #create some offers for the listing
        number_of_offers = 3

        self.offerIDs = [0 for number in range(number_of_offers)]

        for offer in range(number_of_offers):
            new_offer = Offer.objects.create(offerListing=self.offerListing, owner=self.global_user2,
                amount=7.00)
            new_offer.items.add(self.global_item2)
            new_offer.save
            self.offerIDs[offer] = new_offer.id

    #Test to ensure that a user must be logged in to view listings
    def test_redirect_if_not_logged_in(self):
        listing = self.offerListing
        response = self.client.get(reverse('delete-offer-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in if they own the listing
    def test_no_redirect_if_logged_in_owner(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        listing = self.offerListing
        response = self.client.get(reverse('delete-offer-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged but they do not own the listing
    def test_no_redirect_if_logged_in_not_owner(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        listing = self.offerListing
        response = self.client.get(reverse('delete-offer-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        listing = self.offerListing
        response = self.client.get(reverse('delete-offer-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/offer_listing_delete.html')

    #Test to ensure object is deleted and offers asociated are also deleted if user confirms
    def test_succesful_deletion(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        listing = self.offerListing
        post_response = self.client.post(reverse('delete-offer-listing', args=[str(listing.id)]))
        self.assertRedirects(post_response, reverse('offer-listings'))
        self.assertFalse(OfferListing.objects.filter(id=self.listingID).exists())
        for offer_id in self.offerIDs:
            self.assertFalse(Offer.objects.filter(id=offer_id).exists())

class AuctionListingsViewTest(MyTestCase):
    def setUp(self):
        super(AuctionListingsViewTest, self).setUp()
        user1 = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)
        user2 = User.objects.create_user(username="mikey", password="example",
            email="example1@text.com", paypalEmail="example1@text.com",
            invitesOpen=True, inquiriesOpen=True)

        number_of_listings_user1 = 9
        number_of_listings_user2 = 2
        tag = Tag.objects.create(name="Test Tag")
        test_image = self.global_test_image1
        image1 = Image.objects.create(owner=user1, image=test_image, name='Test Image')
        image1.tags.add(tag)
        image1.save
        image2 = Image.objects.create(owner=user2, image=test_image, name='Test Image')
        image2.tags.add(tag)
        image2.save
        item1 = Item.objects.create(name='Test Item', description="Just an item", owner=user1)
        item1.images.add(image1)
        item1.save
        item2 = Item.objects.create(name='Test Item', description="Just an item", owner=user2)
        item2.images.add(image2)
        item2.save

        date = datetime.today()
        settings.TIME_ZONE
        aware_date = make_aware(date)

        for num in range(number_of_listings_user1):
            listing = AuctionListing.objects.create(owner=user1,
                name="Test Auction", description="Just a test auction",
                startingBid=5.00, minimumIncrement=2.50, autobuy=50.00, endTime=aware_date)
            listing.items.add(item1)
            listing.save

        for num in range(number_of_listings_user2):
            listing = AuctionListing.objects.create(owner=user2,
                name="Test Auction", description="Just a test auction",
                startingBid=5.00, minimumIncrement=2.50, autobuy=50.00, endTime=aware_date)
            listing.items.add(item2)
            listing.save

        #create some bids for tests
        for num in range(5):
            Bid.objects.create(auctionListing=self.global_auction_listing1,
                bidder=self.global_user2, amount=(5.00 * (.25 * num)), winningBid = False)

    #Test to ensure that a user must be logged in to view listings
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('auction-listings'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/auction-listings/')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('auction-listings'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('auction-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/auction_listings.html')

    #Test to ensure that the user only sees listings they've uploaded for user1
    def test_list_only_current_users_listings_user1(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('auction-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['auctionlistings']) == 9)

    #Test to ensure that the user only sees listings they've uploaded for user2
    def test_list_only_current_users_listings_user2(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('auction-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['auctionlistings']) == 2)

    #Test to ensure that the a user can see number of bids on a listing
    def test_list_only_current_users_listings_user2(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('auction-listings'))
        self.assertEqual(response.status_code, 200)
        listing_to_check = AuctionListing.objects.get(pk=self.global_auction_listing1.pk)
        for obj in response:
            if obj == listing_to_check:
                self.assertEqual(obj.bid_count, 5)

class AuctionListingDetailViewTest(MyTestCase):
    def setUp(self):
        super(AuctionListingDetailViewTest, self).setUp()
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)
        date = datetime.today()
        settings.TIME_ZONE
        aware_date = make_aware(date)
        self.auctionListing = AuctionListing.objects.create(owner=user,
            name="My Items For Auction", description="A few items up for bids",
            startingBid=5.00, minimumIncrement=2.50, autobuy=50.00, endTime=aware_date)
        self.auctionListing.items.add = self.global_item1
        self.auctionListing.save

    #Test to ensure that a user must be logged in to view listings
    def test_redirect_if_not_logged_in(self):
        listing = self.auctionListing
        response = self.client.get(reverse('auction-listing-detail', args=[str(listing.id)]))
        self.assertRedirects(response, '/accounts/login/?next=/listings/auction-listings/{0}'.format(listing.id))

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        listing = self.auctionListing
        response = self.client.get(reverse('auction-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        listing = self.auctionListing
        response = self.client.get(reverse('auction-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/auction_listing_detail.html')

class AllAuctionListingsViewTest(MyTestCase):
    def setUp(self):
        super(AllAuctionListingsViewTest, self).setUp()

        #Create a variety of listings to test with
        #Number of active listings should be 11 as there is a global active listing
        number_of_active_listings_user1 = 7
        number_of_active_listings_user2 = 5
        number_of_inactive_listings_user1 = 4

        date_ended = timezone.localtime(timezone.now()) - timedelta(hours=1)
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        for num in range(number_of_active_listings_user1):
            listing = AuctionListing.objects.create(owner=self.global_user1, name='Test Auction Listing',
                description="Just a test listing", startingBid=5.00, minimumIncrement=1.00, autobuy=25.00,
                endTime=date_active)
            listing.items.add(self.global_item1)
            listing.save

        for num in range(number_of_active_listings_user2):
            listing = AuctionListing.objects.create(owner=self.global_user2, name='Test Auction Listing',
                description="Just a test listing", startingBid=5.00, minimumIncrement=1.00, autobuy=25.00,
                endTime=date_active)
            listing.items.add(self.global_item2)
            listing.save
            print(num)

        for num in range(number_of_inactive_listings_user1):
            listing = AuctionListing.objects.create(owner=self.global_user1, name='Test Auction Listing',
                description="Just a test listing", startingBid=5.00, minimumIncrement=1.00, autobuy=25.00,
                endTime=date_ended)
            listing.items.add(self.global_item1)
            listing.save

    #Test to ensure that a user must be logged in to view listings
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('all-auction-listings'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/auction-listings/all')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('all-auction-listings'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('all-auction-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/all_auction_listings.html')

    #Test to ensure that a user sees the correct amount of active listings for first page
    def test_list_only_active_listings_page_1(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('all-auction-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['auctionlistings']), 10)

    #Test to ensure that a user sees the correct amount of active listings for second page
    def test_list_only_active_listings_page_2(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('all-auction-listings')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['auctionlistings']), 3)

    #Test to ensure that  different user sees the correct amount of active listings for first page
    def test_list_only_active_listings_new_user_page_1(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('all-auction-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['auctionlistings']), 10)

    #Test to ensure that  different user sees the correct amount of active listings for second page
    def test_list_only_active_listings_new_user_page_2(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('all-auction-listings')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['auctionlistings']), 3)

class MyBidsViewTest(MyTestCase):
    def setUp(self):
        super(MyBidsViewTest, self).setUp()
        #Create a user for testing with
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

        #Set the amount of bids to be made to test
        number_of_bids = 9

        #Create the required amount of bids
        for num in range(number_of_bids):
            remainder = num % 2
            if remainder == 0:
                bid = Bid.objects.create(auctionListing=self.global_auction_listing1, bidder=user,
                    amount=5.00+(1.00*num))
            else:
                bid = Bid.objects.create(auctionListing=self.global_auction_listing1,
                    bidder=self.global_user2, amount=5.00+(1.00*num))

    #Test to ensure that a user must be logged in view bids
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my-bids'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/auction-listings/my-bids')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('my-bids'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('my-bids'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/bids.html')

    #Test to ensure that the user only sees bids they have made for first user
    def test_list_only_current_users_bids_user1(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('my-bids'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['bids']) == 5)

    #Test to ensure that the user only sees offers they have made for the second user
    def test_list_only_current_users_bids_user2(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('my-bids'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['bids']) == 4)

class CreateAuctionListingViewTest(MyTestCase):
    def setUp(self):
        super(CreateAuctionListingViewTest, self).setUp()
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)
        test_image = self.global_test_image1
        image = Image.objects.create(owner=user,  image=test_image, name="Test Image")
        tag = Tag.objects.create(name="Test Tag")
        image.tags.add(tag)
        image.save
        self.item = Item.objects.create(name="Global Item",
            description="A global item for testing", owner=user)
        self.item.images.add(image)
        self.item.save

    #Test to ensure that a user must be logged in to create auction listing
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('create-auction-listing'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/auction-listings/create-auction-listing')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-auction-listing'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-auction-listing'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/create_auction_listing.html')

    #Test to ensure a user is able to create an auction listing and have it relate to them
    def test_auction_listing_is_created(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-auction-listing'),
            data={'name': "My Auction Listing", 'description': "TEST AUCTION",
                'endTimeChoices': "1h", 'items': [str(self.item.id)],
                'startingBid': 5.00, 'minimumIncrement': 1.00, 'autobuy': 50.00})
        self.assertEqual(post_response.status_code, 302)
        new_auction_listing = AuctionListing.objects.last()
        self.assertEqual(new_auction_listing.owner, post_response.wsgi_request.user)
        self.assertEqual(new_auction_listing.autobuy, 50.00)

    #Test to ensure autobuy is set to 0.00 if left blank and auction listing is created successfully
    def test_auction_listing_autobuy_set_to_0_if_blank(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-auction-listing'),
            data={'name': "My Auction Listing", 'description': "TEST AUCTION",
                'endTimeChoices': "1h", 'items': [str(self.item.id)],
                'startingBid': 5.00, 'minimumIncrement': 1.00})
        self.assertEqual(post_response.status_code, 302)
        new_auction_listing = AuctionListing.objects.last()
        self.assertEqual(new_auction_listing.autobuy, 0.00)

    #Test to ensure that an auction listing created to end in 1 hour has correct end time
    def test_auction_listing_1h_end_time(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-auction-listing'),
            data={'name': "My Auction Listing", 'description': "TEST AUCTION",
                'endTimeChoices': "1h", 'items': [str(self.item.id)],
                'startingBid': 5.00, 'minimumIncrement': 1.00, 'autobuy': 50.00})
        self.assertEqual(post_response.status_code, 302)
        new_auction_listing = AuctionListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=1)
        to_tz = timezone.get_default_timezone()
        new_auction_listing_endtime = new_auction_listing.endTime.astimezone(to_tz)
        self.assertEqual(new_auction_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that an auction listing created to end in 2 hours has correct end time
    def test_auction_listing_2h_end_time(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-auction-listing'),
            data={'name': "My Auction Listing", 'description': "TEST AUCTION",
                'endTimeChoices': "2h", 'items': [str(self.item.id)],
                'startingBid': 5.00, 'minimumIncrement': 1.00, 'autobuy': 50.00})
        self.assertEqual(post_response.status_code, 302)
        new_auction_listing = AuctionListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=2)
        to_tz = timezone.get_default_timezone()
        new_auction_listing_endtime = new_auction_listing.endTime.astimezone(to_tz)
        self.assertEqual(new_auction_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that an auction listing created to end in 4 hours has correct end time
    def test_auction_listing_4h_end_time(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-auction-listing'),
            data={'name': "My Auction Listing", 'description': "TEST AUCTION",
                'endTimeChoices': "4h", 'items': [str(self.item.id)],
                'startingBid': 5.00, 'minimumIncrement': 1.00, 'autobuy': 50.00})
        self.assertEqual(post_response.status_code, 302)
        new_auction_listing = AuctionListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=4)
        to_tz = timezone.get_default_timezone()
        new_auction_listing_endtime = new_auction_listing.endTime.astimezone(to_tz)
        self.assertEqual(new_auction_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that an auction listing created to end in 8 hours has correct end time
    def test_auction_listing_8h_end_time(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-auction-listing'),
            data={'name': "My Auction Listing", 'description': "TEST AUCTION",
                'endTimeChoices': "8h", 'items': [str(self.item.id)],
                'startingBid': 5.00, 'minimumIncrement': 1.00, 'autobuy': 50.00})
        self.assertEqual(post_response.status_code, 302)
        new_auction_listing = AuctionListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=8)
        to_tz = timezone.get_default_timezone()
        new_auction_listing_endtime = new_auction_listing.endTime.astimezone(to_tz)
        self.assertEqual(new_auction_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that an auction listing created to end in 12 hours has correct end time
    def test_auction_listing_12h_end_time(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-auction-listing'),
            data={'name': "My Auction Listing", 'description': "TEST AUCTION",
                'endTimeChoices': "12h", 'items': [str(self.item.id)],
                'startingBid': 5.00, 'minimumIncrement': 1.00, 'autobuy': 50.00})
        self.assertEqual(post_response.status_code, 302)
        new_auction_listing = AuctionListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=12)
        to_tz = timezone.get_default_timezone()
        new_auction_listing_endtime = new_auction_listing.endTime.astimezone(to_tz)
        self.assertEqual(new_auction_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that an auction listing created to end in 1 day has correct end time
    def test_auction_listing_1d_end_time(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-auction-listing'),
            data={'name': "My Auction Listing", 'description': "TEST AUCTION",
                'endTimeChoices': "1d", 'items': [str(self.item.id)],
                'startingBid': 5.00, 'minimumIncrement': 1.00, 'autobuy': 50.00})
        self.assertEqual(post_response.status_code, 302)
        new_auction_listing = AuctionListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(days=1)
        to_tz = timezone.get_default_timezone()
        new_auction_listing_endtime = new_auction_listing.endTime.astimezone(to_tz)
        self.assertEqual(new_auction_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that an auction listing created to end in 3 days has correct end time
    def test_auction_listing_3d_end_time(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-auction-listing'),
            data={'name': "My Auction Listing", 'description': "TEST AUCTION",
                'endTimeChoices': "3d", 'items': [str(self.item.id)],
                'startingBid': 5.00, 'minimumIncrement': 1.00, 'autobuy': 50.00})
        self.assertEqual(post_response.status_code, 302)
        new_auction_listing = AuctionListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(days=3)
        to_tz = timezone.get_default_timezone()
        new_auction_listing_endtime = new_auction_listing.endTime.astimezone(to_tz)
        self.assertEqual(new_auction_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that an auction listing created to end in 7 days has correct end time
    def test_auction_listing_7d_end_time(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-auction-listing'),
            data={'name': "My Auction Listing", 'description': "TEST AUCTION",
                'endTimeChoices': "7d", 'items': [str(self.item.id)],
                'startingBid': 5.00, 'minimumIncrement': 1.00, 'autobuy': 50.00})
        self.assertEqual(post_response.status_code, 302)
        new_auction_listing = AuctionListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(days=7)
        to_tz = timezone.get_default_timezone()
        new_auction_listing_endtime = new_auction_listing.endTime.astimezone(to_tz)
        self.assertEqual(new_auction_listing_endtime.hour, end_time_check.hour)

class RelistAuctionListingViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to relist a listing
    def test_redirect_if_not_logged_in(self):
        listing = self.global_auction_listing2
        response = self.client.get(reverse('relist-auction-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/accounts/login/?next=/listings/auction-listings/{0}/relist'.format(listing.id))

    #Test to ensure user is not redirected if logged in and they own the listing
    def test_no_redirect_if_logged_in_and_owns_listing(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.global_auction_listing2
        response = self.client.get(reverse('relist-auction-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in but they do not own the listing
    def test_redirect_if_logged_in_but_does_not_own_listing(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        listing = self.global_auction_listing2
        response = self.client.get(reverse('relist-auction-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is redirected if they own listing but it has bids
    def test_redirect_if_owner_but_bids_exist(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.global_auction_listing2
        bid = Bid.objects.create(auctionListing=self.global_auction_listing2,
            bidder=self.global_user2, amount=5.00, winningBid = True)
        response = self.client.get(reverse('relist-auction-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/auction-listings/')

    #Test to ensure user is redirected if they own listing but it is still active
    def test_redirect_if_owner_but_active_listing(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.global_auction_listing1
        response = self.client.get(reverse('relist-auction-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/auction-listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.global_auction_listing2
        response = self.client.get(reverse('relist-auction-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/relist_auction_listing.html')

    #Test to ensure that relisting the listing works
    def test_succesful_listing_relist(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.global_auction_listing2
        listing.bids.clear()
        response = self.client.get(reverse('relist-auction-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('relist-auction-listing', args=[str(listing.id)]),
            data={'name': "Test Offer Listing Relist", 'description': "Relisting my listing",
                'items': [str(self.global_item1.id)], 'endTimeChoices': "4h", 'startingBid': 10.00,
                'minimumIncrement': 1.00, 'autobuy': 30.00})
        self.assertEqual(post_response.status_code, 302)
        relisted_listing = AuctionListing.objects.get(id=listing.id)
        self.assertEqual(relisted_listing.name, 'Test Offer Listing Relist')
        self.assertEqual(relisted_listing.startingBid, 10.00)
        self.assertEqual(relisted_listing.autobuy, 30.00)
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=4)
        to_tz = timezone.get_default_timezone()
        self.assertEqual(relisted_listing.endTime.astimezone(to_tz).hour, end_time_check.hour)

class CreateOfferViewTest(MyTestCase):
    def setUp(self):
        super(CreateOfferViewTest, self).setUp()
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

        self.active_listing = self.global_offer_listing1
        self.inactive_listing = self.global_offer_listing2
        self.completed_listing = self.global_offer_listing3

    #Test to ensure that a user must be logged in to create offer
    def test_redirect_if_not_logged_in(self):
        listing = self.active_listing
        response = self.client.get(reverse('create-offer', args=[str(listing.id)]))
        self.assertRedirects(response, '/accounts/login/?next=/listings/offer-listings/{0}/offer'.format(listing.id))

    #Test to ensure a user is redirected if they own the listing
    def test_redirect_if_logged_in_but_owns_listing(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.active_listing
        response = self.client.get(reverse('create-offer', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        listing = self.active_listing
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        listing = self.active_listing
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/create_offer.html')

    #Test to ensure a user is able to create an offer and have it relate to them
    def test_succesful_offer_creation_related_to_user(self):
        listing = self.active_listing
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-offer', args=[str(listing.id)]),
            data={'items': [str(self.global_item2.id)], 'amount': 7.00})
        self.assertEqual(post_response.status_code, 302)
        created_offer = Offer.objects.last()
        self.assertEqual(created_offer.owner, post_response.wsgi_request.user)

    #Test to ensure a user is able to create an offer and have it relate to the appropriate listing
    def test_succesful_offer_creation_related_to_listing(self):
        listing = self.active_listing
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-offer', args=[str(listing.id)]),
            data={'items': [str(self.global_item2.id)], 'amount': 7.00})
        self.assertEqual(post_response.status_code, 302)
        created_offer = Offer.objects.last()
        self.assertEqual(created_offer.offerListing, listing)
        self.assertRedirects(post_response, '/listings/offer-listings/offer/{0}'.format(created_offer.id))

    #Test to ensure a user is redirected if a listing has ended
    def test_redirect_if_listing_ended(self):
        listing = self.inactive_listing
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure a user is redirected if a listing has been completed
    def test_redirect_if_listing_completed(self):
        listing = self.completed_listing
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

class CreateBidViewTest(MyTestCase):
    def setUp(self):
        super(CreateBidViewTest, self).setUp()
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

        self.active_listing = self.global_auction_listing1
        self.inactive_listing = self.global_auction_listing2

    #Test to ensure that a user must be logged in to create a bid
    def test_redirect_if_not_logged_in(self):
        listing = self.active_listing
        response = self.client.get(reverse('create-bid', args=[str(listing.id)]))
        self.assertRedirects(response, '/accounts/login/?next=/listings/auction-listings/{0}/bid'.format(listing.id))

    #Test to ensure a user is redirected if they own the listing
    def test_redirect_if_logged_in_but_owns_listing(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.active_listing
        response = self.client.get(reverse('create-bid', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        listing = self.active_listing
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-bid', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        listing = self.active_listing
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-bid', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/create_bid.html')

    #Test to ensure that a user is redirected if the listing has ended
    def test_redirect_if_listing_ended(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        listing = self.inactive_listing
        response = self.client.get(reverse('create-bid', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure that a bid is created succesfully and relates to the current user
    def test_successful_bid_creation_related_to_user(self):
        listing = self.active_listing
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-bid', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-bid', args=[str(listing.id)]),
            data={'amount': 5.00})
        self.assertEqual(post_response.status_code, 302)
        created_bid = Bid.objects.last()
        self.assertEqual(created_bid.amount, 5.00)
        self.assertEqual(created_bid.bidder, post_response.wsgi_request.user)

    #Test to ensure that a bid is created succesfully and relates to the current listing
    def test_successful_bid_creation_related_to_listing(self):
        listing = self.active_listing
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-bid', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-bid', args=[str(listing.id)]),
            data={'amount': 5.00})
        self.assertEqual(post_response.status_code, 302)
        created_bid = Bid.objects.last()
        self.assertEqual(created_bid.auctionListing, listing)

    #Test to ensure that a auction ends if autobuy bid is made
    def test_successful_bid_creation_autobuy_ends_listing(self):
        listing = self.active_listing
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-bid', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-bid', args=[str(listing.id)]),
            data={'amount': 25.00})
        self.assertEqual(post_response.status_code, 302)
        updated_listing = AuctionListing.objects.get(id=listing.id)
        self.assertEqual(updated_listing.listingEnded, True)

    #Test to ensure that previous winning bid is set to false and current bid is winning bid
    def test_successful_bid_creation_previous_bid_changed(self):
        listing = self.active_listing
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-bid', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-bid', args=[str(listing.id)]),
            data={'amount': 5.00})
        self.assertEqual(post_response.status_code, 302)
        created_bid1 = Bid.objects.last()
        self.assertEqual(created_bid1.winningBid, True)
        self.assertEqual(created_bid1.auctionListing, listing)
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        post_response = self.client.post(reverse('create-bid', args=[str(listing.id)]),
            data={'amount': 6.00})
        self.assertEqual(post_response.status_code, 302)
        edited_bid1 = Bid.objects.get(id=created_bid1.id)
        created_bid2 = Bid.objects.last()
        self.assertEqual(edited_bid1.winningBid, False)
        self.assertEqual(created_bid2.winningBid, True)

class OfferDetailViewTest(MyTestCase):
    def setUp(self):
        super(OfferDetailViewTest, self).setUp()

        #Create a user that will be redirected as they are not associated with offer
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

        #Create an Offer instance for testing
        self.offer = Offer.objects.create(offerListing=self.global_offer_listing1, owner=self.global_user2,
                amount=7.00)
        self.offer.items.add(self.global_item2)
        self.offer.save

    #Test to ensure that a user must be logged in to view an offer
    def test_redirect_if_not_logged_in(self):
        offer = self.offer
        response = self.client.get(reverse('offer-detail', args=[str(offer.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in if they own the offer
    def test_no_redirect_if_logged_in_owns_offer(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        offer = self.offer
        response = self.client.get(reverse('offer-detail', args=[str(offer.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is not redirected if logged in if they own the listing
    def test_no_redirect_if_logged_in_owns_listing(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.offer
        response = self.client.get(reverse('offer-detail', args=[str(offer.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if they are not the user that owns the offer or listing
    def test_redirect_if_logged_in_but_incorrect_user(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        offer = self.offer
        response = self.client.get(reverse('offer-detail', args=[str(offer.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        offer = self.offer
        response = self.client.get(reverse('offer-detail', args=[str(offer.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/offer_detail.html')

class AcceptOfferViewTest(MyTestCase):
    def setUp(self):
        super(AcceptOfferViewTest, self).setUp()

        #create some offers for the active listing for testing
        number_of_offers = 5
        for offer in range(number_of_offers):
            new_offer = Offer.objects.create(offerListing=self.global_offer_listing1,
                owner=self.global_user2, amount=7.00)
            new_offer.items.add(self.global_item2)
            new_offer.save
            if offer == 4:
                self.offer = new_offer

        #create offers for an inactive listing to test that a user cannot accept an offer once ended
        self.expired_offer = Offer.objects.create(offerListing=self.global_offer_listing2,
            owner=self.global_user2, amount=7.00)
        expired_offer2 = Offer.objects.create(offerListing=self.global_offer_listing2,
            owner=self.global_user2, amount=7.00)

    #Test to ensure that a user must be logged in to accept an offer
    def test_redirect_if_not_logged_in(self):
        offer = self.offer
        response = self.client.get(reverse('accept-offer', args=[str(offer.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user if logged in is redirected to the offer listing if they own the offer listing
    def test_no_redirect_if_logged_in_owns_listing(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.offer
        response = self.client.get(reverse('accept-offer', args=[str(offer.id)]))
        self.assertRedirects(response, '/listings/offer-listings/{0}'.format(offer.offerListing.id))

    #Test to ensure user is redirected if they do not own the offer listing
    def test_no_redirect_if_logged_does_not_own_listing(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        offer = self.offer
        response = self.client.get(reverse('accept-offer', args=[str(offer.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure that the offer field offerAccepted is updated
    def test_offer_accepted_field_becomes_true(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.offer
        post_response = self.client.post(reverse('accept-offer', args=[str(offer.id)]))
        self.assertEqual(post_response.status_code, 302)
        updated_offer = Offer.objects.get(id=offer.id)
        self.assertEqual(updated_offer.offerAccepted, True)

    #Test to ensure that the offerListing field listingCompleted is updated
    def test_listing_completed_field_becomes_true(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.offer
        post_response = self.client.post(reverse('accept-offer', args=[str(offer.id)]))
        self.assertEqual(post_response.status_code, 302)
        updated_listing = OfferListing.objects.get(id=offer.offerListing.id)
        self.assertEqual(updated_listing.listingCompleted, True)

    #Test to ensure that the offerListing ends when an offer is accepted
    def test_listing_ends(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.offer
        post_response = self.client.post(reverse('accept-offer', args=[str(offer.id)]))
        self.assertEqual(post_response.status_code, 302)
        updated_listing = OfferListing.objects.get(id=offer.offerListing.id)
        self.assertEqual(updated_listing.listingEnded, True)

    #Test to ensure that the unaccepted offers on listing are destroyed
    def test_unaccepted_offers_are_destroyed(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.offer
        post_response = self.client.post(reverse('accept-offer', args=[str(offer.id)]))
        self.assertEqual(post_response.status_code, 302)
        all_listing_offers = Offer.objects.filter(offerListing=self.global_offer_listing1)
        self.assertEqual(len(all_listing_offers), 1)

    #Test to ensure that the accepted offer remains
    def test_accepted_offers_remains(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.offer
        post_response = self.client.post(reverse('accept-offer', args=[str(offer.id)]))
        self.assertEqual(post_response.status_code, 302)
        all_listing_offers = Offer.objects.filter(offerListing=self.global_offer_listing1)
        self.assertEqual(len(all_listing_offers), 1)
        self.assertEqual(offer, all_listing_offers.first())

    #Test to ensure that a user cannot accept an offer once listing has completed
    def test_offer_not_accepted_listing_completed(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.offer
        post_response = self.client.post(reverse('accept-offer', args=[str(offer.id)]))
        self.assertEqual(post_response.status_code, 302)
        response = self.client.get(reverse('accept-offer', args=[str(offer.id)]))
        self.assertRedirects(response, '/listings/offer-listings/{0}'.format(offer.offerListing.id))
        all_listing_offers = Offer.objects.filter(offerListing=self.global_offer_listing1)
        self.assertEqual(len(all_listing_offers), 1)

    #Test to ensure that a user cannot accept an offer once listing has ended, also ensure the same amount of offers remain
    def test_offer_not_accepted_listing_ended(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.expired_offer
        response = self.client.get(reverse('accept-offer', args=[str(offer.id)]))
        self.assertRedirects(response, '/listings/offer-listings/{0}'.format(offer.offerListing.id))
        all_listing_offers = Offer.objects.filter(offerListing=self.global_offer_listing2)
        self.assertEqual(len(all_listing_offers), 2)

class OfferDeleteViewTest(MyTestCase):
    def setUp(self):
        super(OfferDeleteViewTest, self).setUp()
        #User that is not associated with offer
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

        #Create offers for testing deletion with
        self.regular_offer = Offer.objects.create(offerListing=self.global_offer_listing1,
            owner=self.global_user2, amount=7.00)

        self.accepted_offer = Offer.objects.create(offerListing=self.global_offer_listing1,
            owner=self.global_user2, amount=7.00, offerAccepted=True)

    #Test to ensure that a user must be logged in to delete an offer
    def test_redirect_if_not_logged_in(self):
        offer = self.regular_offer
        response = self.client.get(reverse('delete-offer', args=[str(offer.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in if they own the listing
    def test_no_redirect_if_logged_in_owner_of_listing(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.regular_offer
        response = self.client.get(reverse('delete-offer', args=[str(offer.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is not redirected if logged in if they own the offer
    def test_no_redirect_if_logged_in_owner_of_offer(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        offer = self.regular_offer
        response = self.client.get(reverse('delete-offer', args=[str(offer.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged but they do not own the listing or offer
    def test_no_redirect_if_logged_in_not_owner_of_listing_or_offer(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        offer = self.regular_offer
        response = self.client.get(reverse('delete-offer', args=[str(offer.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.regular_offer
        response = self.client.get(reverse('delete-offer', args=[str(offer.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/offer_delete.html')

    #Test to ensure object is deleted
    def test_succesful_deletion(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.regular_offer
        offer_id = self.regular_offer.id
        post_response = self.client.post(reverse('delete-offer', args=[str(offer.id)]))
        self.assertRedirects(post_response, reverse('offer-listing-detail', args=[str(self.global_offer_listing1.id)]))
        self.assertFalse(Offer.objects.filter(id=offer_id).exists())

    #Test to ensure an accepted offer cannot be deleted
    def test_unsuccesful_deletion_accepted_offer(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.accepted_offer
        offer_id = self.accepted_offer.id
        post_response = self.client.post(reverse('delete-offer', args=[str(offer.id)]))
        self.assertRedirects(post_response, reverse('offer-detail', args=[str(offer.id)]))
        self.assertTrue(Offer.objects.filter(id=offer_id).exists())

class OfferEditViewTest(MyTestCase):
    def setUp(self):
        super(OfferEditViewTest, self).setUp()

        #Create offers for testing editing with
        self.offer = Offer.objects.create(offerListing=self.global_offer_listing1,
            owner=self.global_user2, amount=7.00)
        self.offer.items.add(self.global_item2)
        self.offer.save

        self.expired_offer = Offer.objects.create(offerListing=self.global_offer_listing2,
            owner=self.global_user2, amount=7.00)
        self.completed_offer = Offer.objects.create(offerListing=self.global_offer_listing3,
            owner=self.global_user2, amount=7.00)

    #Test to ensure that a user must be logged in to edit an offer
    def test_redirect_if_not_logged_in(self):
        offer = self.offer
        response = self.client.get(reverse('edit-offer', args=[str(offer.id)]))
        self.assertRedirects(response, '/accounts/login/?next=/listings/offer-listings/offer/{0}/edit'.format(offer.id))

    #Test to ensure user is not redirected if logged in if they own the offer
    def test_no_redirect_if_logged_in_owner_of_offer(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        offer = self.offer
        response = self.client.get(reverse('edit-offer', args=[str(offer.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged but they do not own the offer
    def test_redirect_if_logged_in_not_owner_of_offer(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.offer
        response = self.client.get(reverse('edit-offer', args=[str(offer.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is redirected if logged in if they own the offer but listing ended
    def test_redirect_if_logged_in_owner_of_offer_listing_ended(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        offer = self.expired_offer
        response = self.client.get(reverse('edit-offer', args=[str(offer.id)]))
        self.assertRedirects(response, reverse('offer-detail', args=[str(offer.id)]))

    #Test to ensure user is redirected if logged in if they own the offer but listing is completed
    def test_redirect_if_logged_in_owner_of_offer_listing_completed(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        offer = self.completed_offer
        response = self.client.get(reverse('edit-offer', args=[str(offer.id)]))
        self.assertRedirects(response, reverse('offer-detail', args=[str(offer.id)]))

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        offer = self.offer
        response = self.client.get(reverse('edit-offer', args=[str(offer.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/offer_edit.html')

    #Test to ensure object is edited
    def test_succesful_edit(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        offer = self.offer
        response = self.client.get(reverse('edit-offer', args=[str(offer.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('edit-offer', args=[str(offer.id)]),
            data={'items': [str(self.global_item2.id)], 'amount': 10.00})
        self.assertEqual(post_response.status_code, 302)
        edited_offer = Offer.objects.get(id=offer.id)
        self.assertEqual(edited_offer.amount, 10.00)

class AuctionListingDeleteViewTest(MyTestCase):
    def setUp(self):
        super(AuctionListingDeleteViewTest, self).setUp()

        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)
        date_inactive = timezone.localtime(timezone.now()) - timedelta(days=1)

        #Create auction listing objects to test for deletion
        self.inactive_auction_listing = AuctionListing.objects.create(owner=self.global_user1,
            name='Test Auction Listing', description="Just a test listing", startingBid=5.00,
            minimumIncrement=1.00, autobuy=25.00, endTime=date_inactive)
        self.inactive_auction_listing.items.add = self.global_item1
        self.inactive_auction_listing.save
        self.inactive_listing_id = self.inactive_auction_listing.id

        self.active_auction_listing = AuctionListing.objects.create(owner=self.global_user1,
            name='Test Auction Listing', description="Just a test listing", startingBid=5.00,
            minimumIncrement=1.00, autobuy=25.00, endTime=date_active)
        self.active_auction_listing.items.add = self.global_item1
        self.active_auction_listing.save

        #create some bids for the listing
        number_of_bids = 3

        self.bid_IDs = [0 for number in range(number_of_bids)]

        for count in range(number_of_bids):
            new_bid = Bid.objects.create(auctionListing=self.inactive_auction_listing, bidder=self.global_user2,
                amount=(5.00 + (1.00 * count)))
            self.bid_IDs[count] = new_bid.id

    #Test to ensure that a user must be logged in to view listings
    def test_redirect_if_not_logged_in(self):
        listing = self.inactive_auction_listing
        response = self.client.get(reverse('delete-auction-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in if they own the listing
    def test_no_redirect_if_logged_in_owner(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.inactive_auction_listing
        response = self.client.get(reverse('delete-auction-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged but they do not own the listing
    def test_redirect_if_logged_in_not_owner(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        listing = self.inactive_auction_listing
        response = self.client.get(reverse('delete-auction-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is redirected if logged in and is owner but listing is active
    def test_redirect_if_logged_in_owner_but_active_listing(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.active_auction_listing
        response = self.client.get(reverse('delete-auction-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/auction-listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.inactive_auction_listing
        response = self.client.get(reverse('delete-auction-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/auction_listing_delete.html')

    #Test to ensure object is deleted and offers asociated are also deleted if user confirms
    def test_succesful_deletion(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.inactive_auction_listing
        post_response = self.client.post(reverse('delete-auction-listing', args=[str(listing.id)]))
        self.assertRedirects(post_response, reverse('auction-listings'))
        self.assertFalse(AuctionListing.objects.filter(id=self.inactive_listing_id).exists())
        for bid_id in self.bid_IDs:
            self.assertFalse(Bid.objects.filter(id=bid_id).exists())

class EventListViewTest(MyTestCase):
    def setUp(self):
        super(EventListViewTest, self).setUp()

        #Create a user to invite to an event
        user1 = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

        self.number_of_events_user1 = 3
        self.number_of_events_user2 = 6
        self.number_of_events_user3 = 5

        #Create the events for the 1st user
        for num in range(self.number_of_events_user1):
            event = Event.objects.create(host=self.global_user1,
                title="My Awesome Event", context="Please come to my event.",
                date="2020-11-06 15:00", location="1234 Sesame Street")
            remainder = num % 2
            if remainder == 0:
                event.participants.add(user1)
                event.save

        #Create the events for the 2nd user
        for num in range(self.number_of_events_user2):
            event = Event.objects.create(host=self.global_user2,
                title="My Radical Event", context="Please come to my event.",
                date="2020-12-25 15:00", location="6789 Sesame Street")
            remainder = num % 2
            if remainder == 0:
                event.participants.add(user1)
                event.save

    #Test to ensure that a user must be logged in to view events
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('events'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/events/')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/events.html')

    #Test to ensure that the user only sees events they're hosting for user1
    def test_list_only_current_users_events_user1(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['events']), self.number_of_events_user1)

    #Test to ensure that the user only sees events they're hosting for user2
    def test_list_only_current_users_events_user2(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['events']), self.number_of_events_user2)

    #Test to ensure that the user only sees events they've been invited to for user3
    def test_list_only_current_users_events_user3(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['events']), self.number_of_events_user3)

class EventDetailViewTest(MyTestCase):
    def setUp(self):
        super(EventDetailViewTest, self).setUp()

        #Create a user that cant access the event
        user1 = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

    #Test to ensure that a user must be logged in to view an event
    def test_redirect_if_not_logged_in(self):
        event = self.global_event
        response = self.client.get(reverse('event-detail', args=[str(event.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in if they are the host
    def test_no_redirect_if_logged_in_host(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('event-detail', args=[str(event.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is not redirected if logged in if they are a participant
    def test_no_redirect_if_logged_in_participant(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('event-detail', args=[str(event.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if they are part of the event
    def test_redirect_if_logged_in_not_host_or_participant(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('event-detail', args=[str(event.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('event-detail', args=[str(event.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_detail.html')

class CreateEventViewTest(MyTestCase):
    def setUp(self):
        super(CreateEventViewTest, self).setUp()

    #Test to ensure that a user must be logged in to create an event
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('create-event'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/events/create-event')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-event'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-event'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/create_event.html')

    #Test to ensure that a event is created succesfully and relates to the current user
    def test_successful_event_creation_related_to_user(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-event'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-event'),
            data={'title': "My Cool Event", 'context': "It will be cool, please come",
                'date': "2020-11-06 15:00", 'location': "SUNY Potsdam"})
        self.assertEqual(post_response.status_code, 302)
        created_event = Event.objects.last()
        self.assertEqual(created_event.host, post_response.wsgi_request.user)

class EditEventViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to edit an event
    def test_redirect_if_not_logged_in(self):
        event = self.global_event
        response = self.client.get(reverse('edit-event', args=[str(event.id)]))
        self.assertRedirects(response, '/accounts/login/?next=/listings/events/{0}/edit'.format(event.id))

    #Test to ensure user is not redirected if logged in and they are host of event
    def test_no_redirect_if_logged_in_host(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('edit-event', args=[str(event.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in but they are not the host
    def test_redirect_if_logged_in_not_host(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('edit-event', args=[str(event.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('edit-event', args=[str(event.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/edit_event.html')

    #Test to ensure that event is successfully updated
    def test_successful_event_update(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('edit-event', args=[str(event.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('edit-event', args=[str(event.id)]),
            data={'title': "My Rad Event", 'context': "It will be rad, please come",
                'date': "2020-11-06 15:00", 'location': "SUNY Potsdam"})
        self.assertEqual(post_response.status_code, 302)
        edited_event = Event.objects.get(id=event.id)
        self.assertEqual(edited_event.title, "My Rad Event")
        self.assertEqual(edited_event.context, "It will be rad, please come")
        self.assertEqual(edited_event.location, "SUNY Potsdam")

class EventDeleteViewTest(MyTestCase):
    def setUp(self):
        super(EventDeleteViewTest, self).setUp()

        #Create an event object to test for deletion
        self.event_to_delete = Event.objects.create(host=self.global_user1,
            title="My Dumb Event", context="Don't come I regret this.",
            date="2020-11-06 15:00", location="1234 Sesame Street")
        self.event_id = self.event_to_delete.id

        #Add invitations to this later to ensure they are deleted as well

    #Test to ensure that a user must be logged in to delete an event
    def test_redirect_if_not_logged_in(self):
        event = self.event_to_delete
        response = self.client.get(reverse('delete-event', args=[str(event.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in if they are hosting the event
    def test_no_redirect_if_logged_in_host(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        event = self.event_to_delete
        response = self.client.get(reverse('delete-event', args=[str(event.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged but they are not hosting event
    def test_redirect_if_logged_in_not_host(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        event = self.event_to_delete
        response = self.client.get(reverse('delete-event', args=[str(event.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        event = self.event_to_delete
        response = self.client.get(reverse('delete-event', args=[str(event.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_delete.html')

    #Test to ensure object is deleted if user confirms
    #Once invitations are implemented, check to ensure invitations are deleted as well
    def test_succesful_deletion(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        event = self.event_to_delete
        post_response = self.client.post(reverse('delete-event', args=[str(event.id)]))
        self.assertRedirects(post_response, reverse('events'))
        self.assertFalse(Event.objects.filter(id=self.event_id).exists())
