from django.test import TestCase
from listings.models import (User, Image, Tag, Item, Listing, OfferListing,
    AuctionListing, Offer, Bid, Event, Invitation, Wishlist, WishlistListing,
    Profile, Conversation, Message, Receipt, PaymentReceipt,
    ListingNotification, OfferNotification, BidNotification, RatingNotification,
    PaymentNotification, InvitationNotification, EventNotification,
    Notification, Favorite, Report, ListingReport, EventReport, UserReport,
    WishlistReport, ImageReport, RatingReport, Rating, RatingTicket)

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import make_aware
from django.conf import settings
from django.contrib.messages import get_messages

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
        self.global_non_wishlist_item = Item.objects.create(name="Global Item",
            description="A global item not in wishlist for testing", owner=self.global_user1)
        self.global_non_wishlist_item.images.add(self.global_image1)
        self.global_non_wishlist_item.save
        self.global_test_image1 = test_image1
        self.global_test_image2 = test_image2

        #Get the current date and time for testing and create active and inactive endtimes
        date_ended = timezone.localtime(timezone.now()) - timedelta(hours=1)
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        #Create a global offer listing that is active
        self.global_offer_listing1 = OfferListing.objects.create(owner=user1, name='Test Offer Listing',
            description="Just a test listing", openToMoneyOffers=True, minRange=5.00,
            maxRange=10.00, notes="Just offer", endTime=date_active,
            listingCompleted=False, latitude=40.0200, longitude=-75.0300)
        self.global_offer_listing1.items.add(self.global_item1)
        self.global_offer_listing1.save

        #Create a global offer listing that is not active
        self.global_offer_listing2 = OfferListing.objects.create(owner=user1, name='Test Offer Listing',
            description="Just a test listing", openToMoneyOffers=True, minRange=5.00,
            maxRange=10.00, notes="Just offer", endTime=date_ended, latitude=40.0200, longitude=-75.0300)
        self.global_offer_listing2.items.add(self.global_item1)
        self.global_offer_listing2.save

        #Create a global offer listing that has completed
        self.global_offer_listing3 = OfferListing.objects.create(owner=user1, name='Test Offer Listing',
            description="Just a test listing", openToMoneyOffers=True, minRange=5.00,
            maxRange=10.00, notes="Just offer", endTime=date_ended, listingCompleted=True,
            latitude=40.0200, longitude=-75.0300)
        self.global_offer_listing3.items.add(self.global_item1)
        self.global_offer_listing3.save

        #Create a global auction listing that is active
        self.global_auction_listing1 = AuctionListing.objects.create(owner=user1, name='Test Auction Listing',
            description="Just a test listing", startingBid=5.00, minimumIncrement=1.00, autobuy=25.00,
            endTime=date_active, latitude=40.0200, longitude=-75.0300)
        self.global_auction_listing1.items.add(self.global_item1)
        self.global_auction_listing1.save

        #Create a global auction listing that is inactive
        self.global_auction_listing2 = AuctionListing.objects.create(owner=user1, name='Test Auction Listing',
            description="Just a test listing", startingBid=5.00, minimumIncrement=1.00, autobuy=25.00,
            endTime=date_ended, latitude=40.0200, longitude=-75.0300)
        self.global_auction_listing2.items.add(self.global_item1)
        self.global_auction_listing2.save

        #Crete a global event
        self.global_event = Event.objects.create(host=self.global_user1,
            title="My Awesome Event", context="Please come to my event.",
            date="2020-11-06 15:00", location="1234 Sesame Street")
        self.global_event.participants.add(self.global_user2)
        self.global_event.save

        #Create a global wishlist
        self.global_wishlist = Wishlist.objects.create(owner=self.global_user1,
            title="My Wishlist", description="Stuff I would love to trade for")
        self.global_wishlist.items.add(self.global_item1)
        self.global_wishlist.save

#Tests for images list view that belong to a single user
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

#Tests for an image's detail view
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

#Tests for users to upload an image to the site
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

#Tests for a user to edit an image they own
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

#Tests for users to delete an image they own
class ImageDeleteViewTest(MyTestCase):
    def setUp(self):
        super(ImageDeleteViewTest, self).setUp()

        #Create image objects to test for deletion
        test_image = SimpleUploadedFile(name='art1.png',
            content=open('listings/imagetest/art1.png', 'rb').read(), content_type='image/png')
        self.unrelated_image = Image.objects.create(owner=self.global_user1,
            image=test_image, name="Test Image")
        self.unrelated_image_id = self.unrelated_image.id

        self.related_image_owned_item = Image.objects.create(owner=self.global_user1,
            image=test_image, name="Test Image")
        self.related_image_owned_item_id = self.related_image_owned_item.id

        self.related_image_unowned_item_in_receipt = Image.objects.create(owner=self.global_user1,
            image=test_image, name="Test Image")
        self.related_image_unowned_item_in_receipt_id = self.related_image_unowned_item_in_receipt.id

        #create item objects to test with
        self.owned_item =  Item.objects.create(name="Item to Delete",
            description="A item to test deletion", owner=self.global_user1)
        self.owned_item.images.add(self.related_image_owned_item)
        self.owned_item.save
        self.owned_item_id = self.owned_item.id

        self.unowned_item_in_receipt =  Item.objects.create(name="Item to Delete",
            description="A item to test deletion", owner=None)
        self.unowned_item_in_receipt.images.add(self.related_image_unowned_item_in_receipt)
        self.unowned_item_in_receipt.save
        self.unowned_item_in_receipt_id = self.unowned_item_in_receipt.id

    #Test to ensure that a user must be logged in to delete an image
    def test_redirect_if_not_logged_in(self):
        image = self.unrelated_image
        response = self.client.get(reverse('delete-image', args=[str(image.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in if they own the image
    def test_no_redirect_if_logged_in_owner(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        image = self.unrelated_image
        response = self.client.get(reverse('delete-image', args=[str(image.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged but they do not own the image
    def test_no_redirect_if_logged_in_not_owner(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        image = self.unrelated_image
        response = self.client.get(reverse('delete-image', args=[str(image.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        image = self.unrelated_image
        response = self.client.get(reverse('delete-image', args=[str(image.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/image_delete.html')

    #Test to ensure object is deleted if image is not related to any items
    def test_successful_deletion_unrelated_image(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        image = self.unrelated_image
        post_response = self.client.post(reverse('delete-image', args=[str(image.id)]))
        self.assertRedirects(post_response, reverse('images'))
        self.assertFalse(Image.objects.filter(id=self.unrelated_image_id).exists())

    #Test to ensure object is not deleted if image is related to any items
    #owned by current user
    def test_unsuccessful_deletion_related_image_to_owned_item(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        image = self.related_image_owned_item
        post_response = self.client.post(reverse('delete-image', args=[str(image.id)]))
        self.assertEqual(post_response.status_code, 404)

    #Test to ensure object is soft deleted if image is related to any items
    #not owned by current user and there exists no items owned by user
    def test_successful_soft_deletion_related_image_to_unowned_item(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        image = self.related_image_unowned_item_in_receipt
        post_response = self.client.post(reverse('delete-image', args=[str(image.id)]))
        self.assertRedirects(post_response, reverse('images'))
        self.assertTrue(Image.objects.filter(id=self.related_image_unowned_item_in_receipt_id).exists())
        updated_image = Image.objects.get(id=self.related_image_unowned_item_in_receipt_id)
        self.assertEqual(updated_image.owner, None)

#Tests for a user to view a list of items they own
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

#Tests for a user to view details on an item
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

#Tests for a user to create an item
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

#Test for a user to edit an item they created
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

#Tests for a user to delete an item they created
class ItemDeleteViewTest(MyTestCase):
    def setUp(self):
        super(ItemDeleteViewTest, self).setUp()
        #Create item objects to test for deletion
        self.unrelated_item =  Item.objects.create(name="Item to Delete",
            description="A item to test deletion", owner=self.global_user1)
        self.unrelated_item.images.add = self.global_image1
        self.unrelated_item.save
        self.unrelated_item_id = self.unrelated_item.id

        self.undeletable_offer_listing_item =  Item.objects.create(name="Item to Delete",
            description="A item to test deletion", owner=self.global_user1)
        self.undeletable_offer_listing_item.images.add = self.global_image1
        self.undeletable_offer_listing_item.save
        self.undeletable_offer_listing_item_id = self.undeletable_offer_listing_item.id

        self.undeletable_auction_listing_item =  Item.objects.create(name="Item to Delete",
            description="A item to test deletion", owner=self.global_user1)
        self.undeletable_auction_listing_item.images.add = self.global_image1
        self.undeletable_auction_listing_item.save
        self.undeletable_auction_listing_item_id = self.undeletable_auction_listing_item.id

        self.deletable_offer_listing_item =  Item.objects.create(name="Item to Delete",
            description="A item to test deletion", owner=self.global_user1)
        self.deletable_offer_listing_item.images.add = self.global_image1
        self.deletable_offer_listing_item.save
        self.deletable_offer_listing_item_id = self.deletable_offer_listing_item.id

        self.soft_deletable_offer_listing_item =  Item.objects.create(name="Item to Delete",
            description="A item to test deletion", owner=self.global_user1)
        self.soft_deletable_offer_listing_item.images.add = self.global_image1
        self.soft_deletable_offer_listing_item.save
        self.soft_deletable_offer_listing_item_id = self.soft_deletable_offer_listing_item.id

        self.deletable_auction_listing_item =  Item.objects.create(name="Item to Delete",
            description="A item to test deletion", owner=self.global_user1)
        self.deletable_auction_listing_item.images.add = self.global_image1
        self.deletable_auction_listing_item.save
        self.deletable_auction_listing_item_id = self.deletable_auction_listing_item.id

        self.undeletable_auction_listing_no_bids_item =  Item.objects.create(name="Item to Delete",
            description="A item to test deletion", owner=self.global_user1)
        self.undeletable_auction_listing_no_bids_item.images.add = self.global_image1
        self.undeletable_auction_listing_no_bids_item.save
        self.undeletable_auction_listing_no_bids_item_id = self.undeletable_auction_listing_no_bids_item.id

        self.soft_deletable_auction_listing_item =  Item.objects.create(name="Item to Delete",
            description="A item to test deletion", owner=self.global_user1)
        self.soft_deletable_auction_listing_item.images.add = self.global_image1
        self.soft_deletable_auction_listing_item.save
        self.soft_deletable_auction_listing_item_id = self.soft_deletable_auction_listing_item.id

        self.deletable_wishlist_listing_item =  Item.objects.create(name="Item to Delete",
            description="A item to test deletion", owner=self.global_user1)
        self.deletable_wishlist_listing_item.images.add = self.global_image1
        self.deletable_wishlist_listing_item.save
        self.deletable_wishlist_listing_item_id = self.deletable_wishlist_listing_item.id
        self.global_wishlist.items.add(self.deletable_wishlist_listing_item)
        self.global_wishlist.save

        self.deletable_offer_item =  Item.objects.create(name="Item to Delete",
            description="A item to test deletion", owner=self.global_user2)
        self.deletable_offer_item.images.add = self.global_image1
        self.deletable_offer_item.save
        self.deletable_offer_item_id = self.deletable_offer_item.id

        self.soft_deletable_offer_item =  Item.objects.create(name="Item to Delete",
            description="A item to test deletion", owner=self.global_user2)
        self.soft_deletable_offer_item.images.add = self.global_image1
        self.soft_deletable_offer_item.save
        self.soft_deletable_offer_item_id = self.soft_deletable_offer_item.id

        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)
        date_ended = timezone.localtime(timezone.now()) - timedelta(days=1)

        #Create offer listings to test for deletion
        self.active_offer_listing_no_offers = OfferListing.objects.create(
            owner=self.global_user1, name='Test Offer Listing',
            description="Just a test listing", openToMoneyOffers=True, minRange=5.00,
            maxRange=10.00, notes="Just offer", endTime=date_active,
            listingCompleted=False)
        self.active_offer_listing_no_offers.items.add(self.deletable_offer_listing_item)
        self.active_offer_listing_no_offers.save
        self.active_offer_listing_no_offers_id = self.active_offer_listing_no_offers.id

        self.inactive_offer_listing_no_offers = OfferListing.objects.create(
            owner=self.global_user1, name='Test Offer Listing',
            description="Just a test listing", openToMoneyOffers=True, minRange=5.00,
            maxRange=10.00, notes="Just offer", endTime=date_ended,
            listingCompleted=False)
        self.inactive_offer_listing_no_offers.items.add(self.deletable_offer_listing_item)
        self.inactive_offer_listing_no_offers.save
        self.inactive_offer_listing_no_offers_id = self.inactive_offer_listing_no_offers.id

        self.active_offer_listing_offers = OfferListing.objects.create(
            owner=self.global_user1, name='Test Offer Listing',
            description="Just a test listing", openToMoneyOffers=True, minRange=5.00,
            maxRange=10.00, notes="Just offer", endTime=date_active,
            listingCompleted=False)
        self.active_offer_listing_offers.items.add(self.undeletable_offer_listing_item)
        self.active_offer_listing_offers.save
        self.active_offer_listing_offers_id = self.active_offer_listing_offers.id
        self.deleteable_offer = Offer.objects.create(offerListing=self.active_offer_listing_offers,
            owner=self.global_user2, amount=5.00, offerAccepted=False)
        self.deleteable_offer.items.add(self.deletable_offer_item)
        self.deleteable_offer.save
        self.deleteable_offer_id = self.deleteable_offer.id

        self.completed_offer_listing = OfferListing.objects.create(
            owner=self.global_user1, name='Test Offer Listing',
            description="Just a test listing", openToMoneyOffers=True, minRange=5.00,
            maxRange=10.00, notes="Just offer", endTime=date_ended,
            listingCompleted=True)
        self.completed_offer_listing.items.add(self.soft_deletable_offer_listing_item)
        self.completed_offer_listing.save
        self.completed_offer_listing_id = self.completed_offer_listing.id
        self.accepted_offer = Offer.objects.create(offerListing=self.completed_offer_listing,
            owner=self.global_user2, amount=5.00, offerAccepted=True)
        self.accepted_offer.items.add(self.soft_deletable_offer_item)
        self.accepted_offer.save
        self.accepted_offer_id = self.accepted_offer.id

        #create an auction listing to test for deletion
        self.active_auction_listing_no_bids = AuctionListing.objects.create(owner=self.global_user1, name='Test Auction Listing',
            description="Just a test listing", startingBid=5.00, minimumIncrement=1.00, autobuy= 25.00,
            endTime=date_active)
        self.active_auction_listing_no_bids.items.add(self.undeletable_auction_listing_no_bids_item)
        self.active_auction_listing_no_bids.save
        self.active_auction_listing_no_bids_id = self.active_auction_listing_no_bids.id

        self.inactive_auction_listing_no_bids = AuctionListing.objects.create(owner=self.global_user1, name='Test Auction Listing',
            description="Just a test listing", startingBid=5.00, minimumIncrement=1.00, autobuy= 25.00,
            endTime=date_ended)
        self.inactive_auction_listing_no_bids.items.add(self.deletable_auction_listing_item)
        self.inactive_auction_listing_no_bids.save
        self.inactive_auction_listing_no_bids_id = self.inactive_auction_listing_no_bids.id

        self.active_auction_listing_bids = AuctionListing.objects.create(owner=self.global_user1, name='Test Auction Listing',
            description="Just a test listing", startingBid=5.00, minimumIncrement=1.00, autobuy= 25.00,
            endTime=date_active)
        self.active_auction_listing_bids.items.add(self.undeletable_auction_listing_item)
        self.active_auction_listing_bids.save
        self.active_auction_listing_bids_id = self.active_auction_listing_bids.id
        Bid.objects.create(auctionListing=self.active_auction_listing_bids,
            bidder=self.global_user2, amount=5.00, winningBid=True)

        self.completed_auction_listing = AuctionListing.objects.create(owner=self.global_user1, name='Test Auction Listing',
            description="Just a test listing", startingBid=5.00, minimumIncrement=1.00, autobuy= 25.00,
            endTime=date_ended)
        self.completed_auction_listing.items.add(self.soft_deletable_auction_listing_item)
        self.completed_auction_listing.save
        self.completed_auction_listing_id = self.completed_auction_listing.id
        Bid.objects.create(auctionListing=self.completed_auction_listing,
            bidder=self.global_user2, amount=5.00, winningBid=True)

        #Create wishlist listings to test for deletion
        self.active_wishlist_listing = WishlistListing.objects.create(owner=self.global_user1,
            name='My Wishlist Listing', endTime=date_active,
            moneyOffer=5.00, notes="Just a test")
        self.active_wishlist_listing.items.add(self.deletable_wishlist_listing_item)
        self.active_wishlist_listing.save
        self.active_wishlist_listing_id = self.active_wishlist_listing.id

        self.inactive_wishlist_listing = WishlistListing.objects.create(owner=self.global_user1,
            name='My Wishlist Listing', endTime=date_ended,
            moneyOffer=5.00, notes="Just a test")
        self.inactive_wishlist_listing.items.add(self.deletable_wishlist_listing_item)
        self.inactive_wishlist_listing.save
        self.inactive_wishlist_listing_id = self.inactive_wishlist_listing.id

    #Test to ensure that a user must be logged in to delete an item
    def test_redirect_if_not_logged_in(self):
        item = self.unrelated_item
        response = self.client.get(reverse('delete-item', args=[str(item.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in if they own the listing
    def test_no_redirect_if_logged_in_owner(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.unrelated_item
        response = self.client.get(reverse('delete-item', args=[str(item.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged but they do not own the item
    def test_no_redirect_if_logged_in_not_owner(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        item = self.unrelated_item
        response = self.client.get(reverse('delete-item', args=[str(item.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.unrelated_item
        response = self.client.get(reverse('delete-item', args=[str(item.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'items/item_delete.html')

    #Test to ensure user can delete an item that has no relations to a
    #listing or offer
    def test_successful_deletion_unrelated_item(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.unrelated_item
        post_response = self.client.post(reverse('delete-item', args=[str(item.id)]))
        self.assertRedirects(post_response, reverse('items'))
        self.assertFalse(Item.objects.filter(id=self.unrelated_item_id).exists())

    #Test to ensure user can not delete an item that is contained in an active
    #offer listing that has offers
    def test_unsuccessful_deletion_item_in_active_listing_with_offers(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.undeletable_offer_listing_item
        post_response = self.client.post(reverse('delete-item', args=[str(item.id)]))
        self.assertEqual(post_response.status_code, 404)

    #Test to ensure user can not delete an item that is contained in an active
    #auction listing that has bids
    def test_unsuccessful_deletion_item_in_active_listing_with_bids(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.undeletable_auction_listing_item
        post_response = self.client.post(reverse('delete-item', args=[str(item.id)]))
        self.assertEqual(post_response.status_code, 404)

    #Test to ensure user can delete an item that is contained in an active
    #or inactive offer listing that has no offers
    def test_successful_deletion_item_in_offer_listings_with_no_offers(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.deletable_offer_listing_item
        post_response = self.client.post(reverse('delete-item', args=[str(item.id)]))
        self.assertRedirects(post_response, reverse('items'))
        self.assertFalse(Item.objects.filter(id=self.deletable_offer_listing_item_id).exists())
        self.assertFalse(OfferListing.objects.filter(id=self.active_offer_listing_no_offers_id).exists())
        self.assertFalse(OfferListing.objects.filter(id=self.inactive_offer_listing_no_offers_id).exists())
        self.assertTrue(OfferListing.objects.filter(id=self.global_offer_listing1.id).exists())

    #Test to ensure user can soft delete an item that is contained in an
    #completed offer listing
    def test_successful_soft_deletion_item_in_completed_offer_listing(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.soft_deletable_offer_listing_item
        post_response = self.client.post(reverse('delete-item', args=[str(item.id)]))
        self.assertRedirects(post_response, reverse('items'))
        self.assertTrue(Item.objects.filter(id=self.soft_deletable_offer_listing_item_id).exists())
        self.assertTrue(OfferListing.objects.filter(id=self.completed_offer_listing_id).exists())
        updated_item = Item.objects.get(id=self.soft_deletable_offer_listing_item_id)
        self.assertEqual(updated_item.owner, None)

    #Test to ensure user can delete an item that is contained in inactive
    #auction listing that has no bids
    def test_successful_deletion_item_in_inactive_auction_listings_with_no_bids(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.deletable_auction_listing_item
        post_response = self.client.post(reverse('delete-item', args=[str(item.id)]))
        self.assertRedirects(post_response, reverse('items'))
        self.assertFalse(Item.objects.filter(id=self.deletable_auction_listing_item_id).exists())
        self.assertFalse(AuctionListing.objects.filter(id=self.inactive_auction_listing_no_bids_id).exists())
        self.assertTrue(AuctionListing.objects.filter(id=self.global_auction_listing1.id).exists())

    #Test to ensure user can not delete an item that is contained in active
    #auction listing that has no bids
    def test_unsuccessful_deletion_item_in_active_auction_listings_with_no_bids(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.undeletable_auction_listing_no_bids_item
        post_response = self.client.post(reverse('delete-item', args=[str(item.id)]))
        self.assertEqual(post_response.status_code, 404)

    #Test to ensure user can soft delete an item that is contained in an
    #completed auction listing
    def test_successful_soft_deletion_item_in_completed_auction_listing(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.soft_deletable_auction_listing_item
        post_response = self.client.post(reverse('delete-item', args=[str(item.id)]))
        self.assertRedirects(post_response, reverse('items'))
        self.assertTrue(Item.objects.filter(id=self.soft_deletable_auction_listing_item_id).exists())
        self.assertTrue(AuctionListing.objects.filter(id=self.completed_auction_listing_id).exists())
        updated_item = Item.objects.get(id=self.soft_deletable_auction_listing_item_id)
        self.assertEqual(updated_item.owner, None)

    #Test to ensure user can delete an item that is contained in an active
    #or inactive wishlist listing
    def test_successful_deletion_item_in_wishlist_listings(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.deletable_wishlist_listing_item
        post_response = self.client.post(reverse('delete-item', args=[str(item.id)]))
        self.assertRedirects(post_response, reverse('items'))
        self.assertFalse(Item.objects.filter(id=self.deletable_wishlist_listing_item_id).exists())
        self.assertFalse(WishlistListing.objects.filter(id=self.active_wishlist_listing_id).exists())
        self.assertFalse(WishlistListing.objects.filter(id=self.inactive_wishlist_listing_id).exists())

    #Test to ensure user can delete an item that is contained in an unaccepted
    #offer
    def test_successful_deletion_item_in_unaccepted_offer(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        item = self.deletable_offer_item
        post_response = self.client.post(reverse('delete-item', args=[str(item.id)]))
        self.assertRedirects(post_response, reverse('items'))
        self.assertFalse(Item.objects.filter(id=self.deletable_offer_item_id).exists())
        self.assertFalse(Offer.objects.filter(id=self.deleteable_offer_id).exists())

    #Test to ensure user can soft delete an item that is contained in an accepted
    #offer
    def test_successful_deletion_item_in_unaccepted_offer(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        item = self.soft_deletable_offer_item
        post_response = self.client.post(reverse('delete-item', args=[str(item.id)]))
        self.assertRedirects(post_response, reverse('items'))
        self.assertTrue(Item.objects.filter(id=self.soft_deletable_offer_item_id).exists())
        self.assertTrue(Offer.objects.filter(id=self.accepted_offer_id).exists())
        updated_item = Item.objects.get(id=self.soft_deletable_offer_item_id)
        self.assertEqual(updated_item.owner, None)

#Tests for the FAQ index page
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

#Tests for the FAQ on images
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

#Tests for the FAQ on items
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

#Tests for the FAQ on listings (offer/auction/wishlist)
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

#Tests for the FAQ on events
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

#Tests for the FAQ on wishlists
class FAQWishlistsViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to view FAQ
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('faq-wishlists'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/FAQ/wishlists')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-wishlists'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-wishlists'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq/wishlists.html')

#Tests for the FAQ on profiles
class FAQProfilesViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to view FAQ
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('faq-profiles'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/FAQ/profiles')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-profiles'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-profiles'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq/profiles.html')

#Tests for the FAQ on accounts
class FAQAccountsViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to view FAQ
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('faq-accounts'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/FAQ/accounts')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-accounts'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-accounts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq/accounts.html')

#Tests for the FAQ on conversations
class FAQConversationsViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to view FAQ
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('faq-conversations'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/FAQ/conversations')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-conversations'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-conversations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq/conversations.html')

#Tests for the FAQ on receipts
class FAQReceiptsViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to view FAQ
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('faq-receipts'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/FAQ/receipts')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-receipts'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-receipts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq/receipts.html')

#Tests for the FAQ on favorites
class FAQFavoritesViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to view FAQ
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('faq-favorites'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/FAQ/favorites')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-favorites'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq/favorites.html')

#Tests for the FAQ on searching for listings
class FAQSearchViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to view FAQ
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('faq-search'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/FAQ/search')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-search'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq/search.html')

#Tests for the FAQ on creating reports
class FAQReportsViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to view FAQ
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('faq-reports'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/FAQ/reports')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-reports'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-reports'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq/reports.html')

#Tests for the FAQ on ratings
class FAQRatingsViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to view FAQ
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('faq-ratings'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/FAQ/ratings')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-ratings'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('faq-ratings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq/ratings.html')

#Tests for a user to view a list of their offer listings
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

#Tests for a user to view details on an offer listing
class OfferListingDetailViewTest(MyTestCase):
    def setUp(self):
        super(OfferListingDetailViewTest, self).setUp()
        self.new_user1 = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)
        date = datetime.today()
        settings.TIME_ZONE
        aware_date = make_aware(date)
        self.offerListing = OfferListing.objects.create(owner=self.new_user1,
            name="My Items For Offers", description="A few items up for offers",
            openToMoneyOffers=True, minRange=5.00, maxRange=10.00, notes="Just offer",
            endTime=aware_date, latitude=40.4000, longitude=-75.4000)
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

        #Set the locations of the global users and new user
        self.global_user1.profile.latitude = 40.0000
        self.global_user1.profile.longitude = -75.0000
        self.global_user1.profile.save()

        self.global_user2.profile.latitude = 40.5000
        self.global_user2.profile.longitude = -75.5000
        self.global_user2.profile.save()

        self.new_user1.profile.latitude = 40.4000
        self.new_user1.profile.longitude = -75.4000
        self.new_user1.profile.save()

        #Create an additional user for testing with
        self.new_user2 = User.objects.create_user(username="mike4",
            password="example", email="example5@text.com",
            paypalEmail="example5@text.com", invitesOpen=True,
            inquiriesOpen=True)

        self.new_user2.profile.latitude = 42.0000
        self.new_user2.profile.longitude = -77.000
        self.new_user2.profile.save()

    #Test to ensure that a user must be logged in to view listings
    def test_redirect_if_not_logged_in(self):
        listing = self.offerListing
        response = self.client.get(reverse('offer-listing-detail', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in and is nearby to owner
    #of listing
    def test_no_redirect_if_logged_in_nearby_user(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        listing = self.offerListing
        response = self.client.get(reverse('offer-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in but is not nearby to owner
    #of listing
    def test_no_redirect_if_logged_in_not_nearby_user(self):
        login = self.client.login(username='mike4', password='example')
        self.assertTrue(login)
        listing = self.offerListing
        response = self.client.get(reverse('offer-listing-detail', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

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
        self.assertEqual(len(response.context['offers']), 5)

    #Test that a user that does not own the listing cannot see offers
    def test_not_owner_can_not_see_offers(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.offerListing
        response = self.client.get(reverse('offer-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['offers']), 0)

    #Test to ensure a user is redirected if a listing has completed and they are
    #not the owner or offerer
    def test_redirect_if_not_owner_or_accepted_offer_listing_completed(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        listing = self.global_offer_listing3
        response = self.client.get(reverse('offer-listing-detail', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure a user is not redirected if a listing has completed and they
    #are the owner of listing
    def test_no_redirect_if_listing_owner_listing_completed(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.global_offer_listing3
        response = self.client.get(reverse('offer-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure a user is not redirected if a listing has completed and they
    #are the owner of accepted offer
    def test_no_redirect_if_accepted_owner_listing_completed(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        listing = self.global_offer_listing3
        response = self.client.get(reverse('offer-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

#Tests for a user to view all offer listings within 20 miles of them
class AllOfferListingsViewTest(MyTestCase):
    def setUp(self):
        super(AllOfferListingsViewTest, self).setUp()

        #Create a variety of listings to test with
        #Number of active listings should be 10 as there is a global active listing
        number_of_active_listings_user1 = 6
        number_of_active_listings_user2 = 5
        number_of_inactive_listings_user1 = 2
        number_of_completed_listings_user2 = 3

        date_ended = timezone.localtime(timezone.now()) - timedelta(hours=1)
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        #Set the locations of the users
        self.global_user1.profile.latitude = 40.0000
        self.global_user1.profile.longitude = -75.0000
        self.global_user1.profile.save()

        self.global_user2.profile.latitude = 41.0000
        self.global_user2.profile.longitude = -69.0000
        self.global_user2.profile.save()

        for num in range(number_of_active_listings_user1):
            listing = OfferListing.objects.create(owner=self.global_user1,
                name='Test Offer Listing #{0}'.format(num), description="Just a test listing",
                openToMoneyOffers=True, minRange=5.00, maxRange=10.00, notes="Just offer",
                endTime=date_active, latitude=40.0000, longitude=-75.0000)
            listing.items.add(self.global_item1)
            listing.save

        for num in range(number_of_active_listings_user2):
            listing = OfferListing.objects.create(owner=self.global_user2,
                name='Test Offer Listing #{0}'.format(num), description="Just a test listing",
                openToMoneyOffers=True, minRange=5.00, maxRange=10.00, notes="Just offer",
                endTime=date_active, latitude=41.0000, longitude=-69.0000)
            listing.items.add(self.global_item2)
            listing.save

        for num in range(number_of_inactive_listings_user1):
            listing = OfferListing.objects.create(owner=self.global_user1,
                name='Test Offer Listing #{0}'.format(num), description="Just a test listing",
                openToMoneyOffers=True, minRange=5.00, maxRange=10.00, notes="Just offer",
                endTime=date_ended, latitude=40.0000, longitude=-75.0000)
            listing.items.add(self.global_item1)
            listing.save

        for num in range(number_of_completed_listings_user2):
            listing = OfferListing.objects.create(owner=self.global_user2,
                name='Test Offer Listing #{0}'.format(num), description="Just a test listing",
                openToMoneyOffers=True, minRange=5.00, maxRange=10.00, notes="Just offer",
                endTime=date_active, listingCompleted=True, latitude=41.0000, longitude=-69.0000)
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

    #Test to ensure that a user sees the correct amount of active listings relative
    #to their location
    def test_list_only_active_listings(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('all-offer-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['offerlistings']), 7)

    #Test to ensure that a different user sees the correct amount of active listings
    #relative to their location
    def test_list_only_active_listings_new_user(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('all-offer-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['offerlistings']), 5)

#Tests for a user to view offers they have made
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

#Tests for a user to create an offer listing
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

        user.profile.latitude = 44.0265
        user.profile.longitude = -75.8499
        user.profile.save()

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

    #Test to ensure that a user is able to create an offer listing and
    #have it relate to them, a receipt is made for the listing, and a
    #ending notification was made
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
        self.assertEqual(str(new_offer_listing.latitude), '44.0265')
        self.assertEqual(str(new_offer_listing.longitude), '-75.8499')
        self.assertTrue(Receipt.objects.filter(listing=new_offer_listing).exists())
        receipt = Receipt.objects.get(listing=new_offer_listing)
        self.assertEqual(receipt.owner, post_response.wsgi_request.user)
        new_notification = ListingNotification.objects.last()
        self.assertEqual(new_notification.listing.name, new_offer_listing.name)
        self.assertEqual(new_notification.creationDate, new_offer_listing.endTime)
        self.assertEqual(new_notification.user, post_response.wsgi_request.user)

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

#Tests for a user to edit an offer listing they own
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

#Tests for a user to relist an expired offered listing they own
class RelistOfferListingViewTest(MyTestCase):
    def setUp(self):
        super(RelistOfferListingViewTest, self).setUp()

        #create some offers for the listing to test they are deleted when listing is relisted
        number_of_offers = 6

        self.offer_ids = [0 for number in range(number_of_offers)]

        for offer in range(number_of_offers):
            new_offer = Offer.objects.create(offerListing=self.global_offer_listing2, owner=self.global_user2,
                amount=7.00)
            new_offer.items.add(self.global_item2)
            new_offer.save
            self.offer_ids[offer] = new_offer.id
            content = (self.global_user2.username +
                ' has placed an offer on your listing "' +
                self.global_offer_listing2.name + '".')
            OfferNotification.objects.create(listing=self.global_offer_listing2,
                offer=new_offer, user=self.global_user1,
                creationDate=timezone.localtime(timezone.now()),
                content=content, type="Offer Made")

        content = ('Your listing "' + self.global_offer_listing2.name
            + '" has expired.')
        self.ending_notification = ListingNotification.objects.create(
            listing=self.global_offer_listing2, user=self.global_user1,
            creationDate=self.global_offer_listing2.endTime,
            content=content, type="Listing Ended")

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
    #Ensure that the ending notification was updated with new endTime
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
        updated_notification = ListingNotification.objects.get(id=self.ending_notification.id)
        self.assertEqual(updated_notification.listing.name, relisted_listing.name)
        self.assertEqual(updated_notification.creationDate, relisted_listing.endTime)

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
        for offer_id in self.offer_ids:
            self.assertFalse(OfferNotification.objects.filter(offer__id=offer_id).exists())

#Tests for a user to delete an offer listing they own
class OfferListingDeleteViewTest(MyTestCase):
    def setUp(self):
        super(OfferListingDeleteViewTest, self).setUp()
        #Get the current date and time for testing and create active and inactive endtimes
        date_ended = timezone.localtime(timezone.now()) - timedelta(hours=1)
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        #Create offer listing objects to test for deletion
        #Active listings
        self.active_offer_listing_no_offers = OfferListing.objects.create(owner=self.global_user1,
            name="My Items For Offers", description="A few items up for offers",
            openToMoneyOffers=True, minRange=5.00, maxRange=10.00,
            notes="Just offer", endTime=date_active)
        self.active_offer_listing_no_offers.items.add = self.global_item1
        self.active_offer_listing_no_offers.save
        self.active_offer_listing_no_offers_id = self.active_offer_listing_no_offers.id

        content = ('Your listing "' + self.active_offer_listing_no_offers.name
            + '" has expired.')
        self.active_no_offers_listing_notification = ListingNotification.objects.create(
            listing=self.active_offer_listing_no_offers, user=self.global_user1,
            creationDate=self.active_offer_listing_no_offers.endTime,
            content=content, type="Listing Ended")
        self.active_no_offers_listing_notification_id = self.active_no_offers_listing_notification.id

        self.active_offer_listing_offers = OfferListing.objects.create(owner=self.global_user1,
            name="My Items For Offers", description="A few items up for offers",
            openToMoneyOffers=True, minRange=5.00, maxRange=10.00,
            notes="Just offer", endTime=date_active)
        self.active_offer_listing_offers.items.add = self.global_item1
        self.active_offer_listing_offers.save
        self.active_offer_listing_offers_id = self.active_offer_listing_offers.id

        content = ('Your listing "' + self.active_offer_listing_offers.name
            + '" has expired.')
        self.active_offers_listing_notification = ListingNotification.objects.create(
            listing=self.active_offer_listing_offers, user=self.global_user1,
            creationDate=self.active_offer_listing_offers.endTime,
            content=content, type="Listing Ended")
        self.active_offers_listing_notification_id = self.active_offers_listing_notification.id

        #Inactive listings
        self.inactive_offer_listing_no_offers = OfferListing.objects.create(owner=self.global_user1,
            name="My Items For Offers", description="A few items up for offers",
            openToMoneyOffers=True, minRange=5.00, maxRange=10.00,
            notes="Just offer", endTime=date_ended)
        self.inactive_offer_listing_no_offers.items.add = self.global_item1
        self.inactive_offer_listing_no_offers.save
        self.inactive_offer_listing_no_offers_id = self.inactive_offer_listing_no_offers.id

        content = ('Your listing "' + self.inactive_offer_listing_no_offers.name
            + '" has expired.')
        self.inactive_no_offers_listing_notification = ListingNotification.objects.create(
            listing=self.inactive_offer_listing_no_offers, user=self.global_user1,
            creationDate=self.inactive_offer_listing_no_offers.endTime,
            content=content, type="Listing Ended")
        self.inactive_no_offers_listing_notification_id = self.inactive_no_offers_listing_notification.id

        self.inactive_offer_listing_offers = OfferListing.objects.create(owner=self.global_user1,
            name="My Items For Offers", description="A few items up for offers",
            openToMoneyOffers=True, minRange=5.00, maxRange=10.00,
            notes="Just offer", endTime=date_ended, listingCompleted=False)
        self.inactive_offer_listing_offers.items.add = self.global_item1
        self.inactive_offer_listing_offers.save
        self.inactive_offer_listing_offers_id = self.inactive_offer_listing_offers.id

        content = ('Your listing "' + self.inactive_offer_listing_offers.name
            + '" has expired.')
        self.inactive_offers_listing_notification = ListingNotification.objects.create(
            listing=self.inactive_offer_listing_offers, user=self.global_user1,
            creationDate=self.inactive_offer_listing_offers.endTime,
            content=content, type="Listing Ended")
        self.inactive_offers_listing_notification_id = self.inactive_offers_listing_notification.id

        self.inactive_offer_listing_completed = OfferListing.objects.create(owner=self.global_user1,
            name="My Items For Offers", description="A few items up for offers",
            openToMoneyOffers=True, minRange=5.00, maxRange=10.00,
            notes="Just offer", endTime=date_ended, listingCompleted=True)
        self.inactive_offer_listing_completed.items.add = self.global_item1
        self.inactive_offer_listing_completed.save
        self.inactive_offer_listing_completed_id = self.inactive_offer_listing_completed.id

        content = ('Your listing "' + self.inactive_offer_listing_completed.name
            + '" has expired.')
        self.inactive_completed_listing_notification = ListingNotification.objects.create(
            listing=self.inactive_offer_listing_completed, user=self.global_user1,
            creationDate=self.inactive_offer_listing_completed.endTime,
            content=content, type="Listing Ended")
        self.inactive_completed_listing_notification_id = self.inactive_completed_listing_notification.id

        #create some offers for listings
        number_of_offers = 3

        self.active_offer_listing_offers_offer_ids = [0 for number in range(number_of_offers)]
        self.inactive_offer_listing_offers_offer_ids = [0 for number in range(number_of_offers)]

        for offer in range(number_of_offers):
            new_offer = Offer.objects.create(offerListing=self.active_offer_listing_offers,
                owner=self.global_user2, amount=7.00)
            new_offer.items.add(self.global_item2)
            new_offer.save
            self.active_offer_listing_offers_offer_ids[offer] = new_offer.id
            content = (self.global_user2.username +
                ' has placed an offer on your listing "' +
                self.active_offer_listing_offers.name + '".')
            OfferNotification.objects.create(listing=self.active_offer_listing_offers,
                offer=new_offer, user=self.global_user1,
                creationDate=timezone.localtime(timezone.now()),
                content=content, type="Offer Made")

        for offer in range(number_of_offers):
            new_offer = Offer.objects.create(offerListing=self.inactive_offer_listing_offers,
                owner=self.global_user2, amount=7.00)
            new_offer.items.add(self.global_item2)
            new_offer.save
            self.inactive_offer_listing_offers_offer_ids[offer] = new_offer.id
            content = (self.global_user2.username +
                ' has placed an offer on your listing "' +
                self.inactive_offer_listing_offers.name + '".')
            OfferNotification.objects.create(listing=self.inactive_offer_listing_offers,
                offer=new_offer, user=self.global_user1,
                creationDate=timezone.localtime(timezone.now()),
                content=content, type="Offer Made")

    #Test to ensure that a user must be logged in to view listings
    def test_redirect_if_not_logged_in(self):
        listing = self.active_offer_listing_no_offers
        response = self.client.get(reverse('delete-offer-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in if they own the listing
    def test_no_redirect_if_logged_in_owner(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.active_offer_listing_no_offers
        response = self.client.get(reverse('delete-offer-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged but they do not own the listing
    def test_no_redirect_if_logged_in_not_owner(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        listing = self.active_offer_listing_no_offers
        response = self.client.get(reverse('delete-offer-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.active_offer_listing_no_offers
        response = self.client.get(reverse('delete-offer-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/offer_listing_delete.html')

    #Test to ensure user can delete an active offer listing with no offers
    def test_successful_deletion_active_listing_no_offers(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.active_offer_listing_no_offers
        post_response = self.client.post(reverse('delete-offer-listing', args=[str(listing.id)]))
        self.assertRedirects(post_response, reverse('offer-listings'))
        self.assertFalse(OfferListing.objects.filter(id=self.active_offer_listing_no_offers_id).exists())
        self.assertFalse(ListingNotification.objects.filter(id=self.active_no_offers_listing_notification_id).exists())

    #Test to ensure user cannot delete an active offer listing with offers
    def test_unsuccessful_deletion_active_listing_offers(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.active_offer_listing_offers
        post_response = self.client.post(reverse('delete-offer-listing', args=[str(listing.id)]))
        self.assertEqual(post_response.status_code, 404)
        self.assertTrue(ListingNotification.objects.filter(id=self.active_offers_listing_notification_id).exists())

    #Test to ensure that user can delete an inactive offer listing the was not
    #completed with no offers
    def test_successful_deletion_inactive_listing_no_offers(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.inactive_offer_listing_no_offers
        post_response = self.client.post(reverse('delete-offer-listing', args=[str(listing.id)]))
        self.assertRedirects(post_response, reverse('offer-listings'))
        self.assertFalse(OfferListing.objects.filter(id=self.inactive_offer_listing_no_offers_id).exists())
        self.assertFalse(ListingNotification.objects.filter(id=self.inactive_no_offers_listing_notification_id).exists())

    #Test to ensure that user can delete an inactive offer listing the was not
    #completed with offers and offers are deleted, as well as notifications
    #for offers made
    def test_successful_deletion_inactive_listing_offers(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.inactive_offer_listing_offers
        post_response = self.client.post(reverse('delete-offer-listing', args=[str(listing.id)]))
        self.assertRedirects(post_response, reverse('offer-listings'))
        self.assertFalse(OfferListing.objects.filter(id=self.inactive_offer_listing_offers_id).exists())
        for offer_id in self.inactive_offer_listing_offers_offer_ids:
            self.assertFalse(Offer.objects.filter(id=offer_id).exists())
            self.assertFalse(OfferNotification.objects.filter(offer__id=offer_id).exists())
        self.assertFalse(ListingNotification.objects.filter(id=self.inactive_offers_listing_notification_id).exists())

    #Test to ensure user can soft delete an offer listing that was completed
    def test_successful_soft_deletion_inactive_listing_completed(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.inactive_offer_listing_completed
        post_response = self.client.post(reverse('delete-offer-listing', args=[str(listing.id)]))
        self.assertRedirects(post_response, reverse('offer-listings'))
        self.assertTrue(OfferListing.objects.filter(id=self.inactive_offer_listing_completed_id).exists())
        updated_listing = OfferListing.objects.get(id=self.inactive_offer_listing_completed_id)
        self.assertEqual(updated_listing.owner, None)
        self.assertFalse(ListingNotification.objects.filter(id=self.inactive_completed_listing_notification_id).exists())

#Tests for a user to view the list of auction listings they own
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

#Tests for a user to view details on an auction listing
class AuctionListingDetailViewTest(MyTestCase):
    def setUp(self):
        super(AuctionListingDetailViewTest, self).setUp()
        self.new_user1 = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)
        date = datetime.today()
        settings.TIME_ZONE
        aware_date = make_aware(date)
        self.auctionListing = AuctionListing.objects.create(owner=self.new_user1,
            name="My Items For Auction", description="A few items up for bids",
            startingBid=5.00, minimumIncrement=2.50, autobuy=50.00,
            endTime=aware_date, latitude=40.4000, longitude=-75.4000)
        self.auctionListing.items.add = self.global_item1
        self.auctionListing.save

        #Set the locations of the global users and new user
        self.global_user1.profile.latitude = 40.0000
        self.global_user1.profile.longitude = -75.0000
        self.global_user1.profile.save()

        self.global_user2.profile.latitude = 40.5000
        self.global_user2.profile.longitude = -75.5000
        self.global_user2.profile.save()

        self.new_user1.profile.latitude = 40.4000
        self.new_user1.profile.longitude = -75.4000
        self.new_user1.profile.save()

        #Create an additional user for testing with
        self.new_user2 = User.objects.create_user(username="mike4",
            password="example", email="example5@text.com",
            paypalEmail="example5@text.com", invitesOpen=True,
            inquiriesOpen=True)

        self.new_user2.profile.latitude = 42.0000
        self.new_user2.profile.longitude = -77.000
        self.new_user2.profile.save()

        #Make a completed auction to test that only owner and winning bid owner
        #can view it when it ends
        Bid.objects.create(auctionListing=self.global_auction_listing1,
            bidder=self.global_user2, amount=5.00, winningBid=True)
        self.global_auction_listing1.endTime = timezone.localtime(timezone.now())
        self.global_auction_listing1.save()

    #Test to ensure that a user must be logged in to view listings
    def test_redirect_if_not_logged_in(self):
        listing = self.auctionListing
        response = self.client.get(reverse('auction-listing-detail', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in and is within 50 miles
    #of owner of listing
    def test_no_redirect_if_logged_in_nearby_user(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        listing = self.auctionListing
        response = self.client.get(reverse('auction-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is not redirected if logged in and is within 50 miles
    #of owner of listing
    def test_no_redirect_if_logged_in_not_nearby_user(self):
        login = self.client.login(username='mike4', password='example')
        self.assertTrue(login)
        listing = self.auctionListing
        response = self.client.get(reverse('auction-listing-detail', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        listing = self.auctionListing
        response = self.client.get(reverse('auction-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/auction_listing_detail.html')

    #Test to ensure user is not redirected if logged in and own the listing if
    #the listing has ended
    def test_no_redirect_if_logged_in_owner_listing_ended(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.global_auction_listing1
        response = self.client.get(reverse('auction-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is not redirected if logged in and if listing has
    #ended, the are owner of winning bid
    def test_no_redirect_if_logged_in_winning_bid_user_listing_ended(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        listing = self.global_auction_listing1
        response = self.client.get(reverse('auction-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in and if listing has
    #ended and they do not own listing or have the winning bid
    def test_redirect_if_logged_in_not_owner_or_winning_bid_user_listing_ended(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        listing = self.global_auction_listing1
        response = self.client.get(reverse('auction-listing-detail', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

#Tests for a user to view all auction listings within 20 miles of them
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

        #Set the locations of the users
        self.global_user1.profile.latitude = 40.0000
        self.global_user1.profile.longitude = -75.0000
        self.global_user1.profile.save()

        self.global_user2.profile.latitude = 41.0000
        self.global_user2.profile.longitude = -69.0000
        self.global_user2.profile.save()

        for num in range(number_of_active_listings_user1):
            listing = AuctionListing.objects.create(owner=self.global_user1, name='Test Auction Listing',
                description="Just a test listing", startingBid=5.00, minimumIncrement=1.00, autobuy=25.00,
                endTime=date_active, latitude=40.0000, longitude=-75.0000)
            listing.items.add(self.global_item1)
            listing.save

        for num in range(number_of_active_listings_user2):
            listing = AuctionListing.objects.create(owner=self.global_user2, name='Test Auction Listing',
                description="Just a test listing", startingBid=5.00, minimumIncrement=1.00, autobuy=25.00,
                endTime=date_active, latitude=41.0000, longitude=-69.0000)
            listing.items.add(self.global_item2)
            listing.save
            print(num)

        for num in range(number_of_inactive_listings_user1):
            listing = AuctionListing.objects.create(owner=self.global_user1, name='Test Auction Listing',
                description="Just a test listing", startingBid=5.00, minimumIncrement=1.00, autobuy=25.00,
                endTime=date_ended, latitude=40.0000, longitude=-75.0000)
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

    #Test to ensure that a user sees the correct amount of active listings
    #for first page relative to their location
    def test_list_only_active_listings_page_1(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('all-auction-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['auctionlistings']), 8)

    #Test to ensure that a different user sees the correct amount of active
    #listings for first page  relative to their location
    def test_list_only_active_listings_new_user_page_1(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('all-auction-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['auctionlistings']), 5)

#Tests for a user to view all bids they have placed
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
        self.assertTrue(len(response.context['bids']) == 1)

    #Test to ensure that the user only sees offers they have made for the second user
    def test_list_only_current_users_bids_user2(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('my-bids'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['bids']) == 1)

#Tests for a user to create an auction listing
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

        user.profile.latitude = 44.0265
        user.profile.longitude = -75.8499
        user.profile.save()

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

    #Test to ensure a user is able to create an auction listing and have it
    #relate to them.  Also test to ensure receipt for listing was created
    #and an ending notification was made
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
        self.assertEqual(str(new_auction_listing.latitude), '44.0265')
        self.assertEqual(str(new_auction_listing.longitude), '-75.8499')
        self.assertTrue(Receipt.objects.filter(listing=new_auction_listing).exists())
        receipt = Receipt.objects.get(listing=new_auction_listing)
        self.assertEqual(receipt.owner, post_response.wsgi_request.user)
        new_notification = ListingNotification.objects.last()
        self.assertEqual(new_notification.listing.name, new_auction_listing.name)
        self.assertEqual(new_notification.creationDate, new_auction_listing.endTime)
        self.assertEqual(new_notification.user, post_response.wsgi_request.user)

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

#Tests for a user to relist an expired auction listing they own
class RelistAuctionListingViewTest(MyTestCase):
    def setUp(self):
        super(RelistAuctionListingViewTest, self).setUp()

        #Ending notification for the listing
        content = ('Your listing "' + self.global_auction_listing2.name
            + '" has expired.')
        self.ending_notification = ListingNotification.objects.create(
            listing=self.global_auction_listing2, user=self.global_user1,
            creationDate=self.global_auction_listing2.endTime,
            content=content, type="Listing Ended")

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

    #Test to ensure that relisting the listing works, and that the ending
    #notification is updated
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
        updated_notification = ListingNotification.objects.get(id=self.ending_notification.id)
        self.assertEqual(updated_notification.listing.name, relisted_listing.name)
        self.assertEqual(updated_notification.creationDate, relisted_listing.endTime)

#Tests for a user to create an offer on an offer listing
class CreateOfferViewTest(MyTestCase):
    def setUp(self):
        super(CreateOfferViewTest, self).setUp()
        self.active_listing = self.global_offer_listing1
        self.inactive_listing = self.global_offer_listing2
        self.completed_listing = self.global_offer_listing3

        #Set the locations of the global users
        self.global_user1.profile.latitude = 40.0000
        self.global_user1.profile.longitude = -75.0000
        self.global_user1.profile.save()

        self.global_user2.profile.latitude = 40.5000
        self.global_user2.profile.longitude = -75.5000
        self.global_user2.profile.save()

        #Create an additional user for testing with
        self.new_user = User.objects.create_user(username="mike4",
            password="example", email="example5@text.com",
            paypalEmail="example5@text.com", invitesOpen=True,
            inquiriesOpen=True)

        self.new_user.profile.latitude = 42.0000
        self.new_user.profile.longitude = -77.000
        self.new_user.profile.save()

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
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        listing = self.active_listing
        login = self.client.login(username='mike3', password='example')
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

    #Test to ensure that notifications are made when an offer is created
    def test_succesful_offer_creation_notifications_made(self):
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
        self.assertTrue(OfferNotification.objects.filter(
            listing=created_offer.offerListing, offer=created_offer,
            user=created_offer.offerListing.owner).exists())
        self.assertTrue(OfferNotification.objects.filter(
            listing=created_offer.offerListing, offer=created_offer,
            user=created_offer.owner).exists())
        self.assertRedirects(post_response, '/listings/offer-listings/offer/{0}'.format(created_offer.id))

    #Test to ensure a user is redirected if a listing has ended
    def test_redirect_if_listing_ended(self):
        listing = self.inactive_listing
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure a user is redirected if a listing has been completed
    def test_redirect_if_listing_completed(self):
        listing = self.completed_listing
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure a user is redirected if not within a 50m radius of listing
    def test_redirect_if_not_nearby_user(self):
        listing = self.active_listing
        login = self.client.login(username='mike4', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-offer', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

#Tests for a user to create a bid on an auction listing
class CreateBidViewTest(MyTestCase):
    def setUp(self):
        super(CreateBidViewTest, self).setUp()
        self.new_user1 = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

        self.active_listing = self.global_auction_listing1

        #Ending notification for the listing
        content = ('Your listing "' + self.active_listing.name
            + '" has expired.')
        self.ending_notification = ListingNotification.objects.create(
            listing=self.active_listing, user=self.global_user1,
            creationDate=self.active_listing.endTime,
            content=content, type="Listing Ended")

        self.inactive_listing = self.global_auction_listing2

        #Ending notification for the listing
        content = ('Your listing "' + self.inactive_listing.name
            + '" has expired.')
        self.ending_notification = ListingNotification.objects.create(
            listing=self.inactive_listing, user=self.global_user1,
            creationDate=self.inactive_listing.endTime,
            content=content, type="Listing Ended")

        #Set the locations of the global users and new user
        self.global_user1.profile.latitude = 40.0000
        self.global_user1.profile.longitude = -75.0000
        self.global_user1.profile.save()

        self.global_user2.profile.latitude = 40.5000
        self.global_user2.profile.longitude = -75.5000
        self.global_user2.profile.save()

        self.new_user1.profile.latitude = 40.5000
        self.new_user1.profile.longitude = -75.5000
        self.new_user1.profile.save()

        #Create an additional user for testing with
        self.new_user2 = User.objects.create_user(username="mike4",
            password="example", email="example5@text.com",
            paypalEmail="example5@text.com", invitesOpen=True,
            inquiriesOpen=True)

        self.new_user2.profile.latitude = 42.0000
        self.new_user2.profile.longitude = -77.000
        self.new_user2.profile.save()

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

    #Test to ensure user is not redirected if logged in and is within a 50 mile
    #radius of listing
    def test_no_redirect_if_logged_in_nearby_user(self):
        listing = self.active_listing
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-bid', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in and is not within a 50 mile
    #radius of listing
    def test_no_redirect_if_logged_in_not_nearby_user(self):
        listing = self.active_listing
        login = self.client.login(username='mike4', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-bid', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        listing = self.active_listing
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-bid', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/create_bid.html')

    #Test to ensure that a user is redirected if the listing has ended
    def test_redirect_if_listing_ended(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        listing = self.inactive_listing
        response = self.client.get(reverse('create-bid', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure that a bid is created succesfully and relates to the
    #current user
    def test_successful_bid_creation_related_to_user(self):
        listing = self.active_listing
        login = self.client.login(username='mike3', password='example')
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
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-bid', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-bid', args=[str(listing.id)]),
            data={'amount': 5.00})
        self.assertEqual(post_response.status_code, 302)
        created_bid = Bid.objects.last()
        self.assertEqual(created_bid.auctionListing, listing)

    #Test to ensure that a bid is created succesfully and a notification is
    #made for the bidder and the ending notification for listing is updated
    def test_successful_bid_creation_notification_made_and_updated(self):
        listing = self.active_listing
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-bid', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-bid', args=[str(listing.id)]),
            data={'amount': 5.00})
        self.assertEqual(post_response.status_code, 302)
        created_bid = Bid.objects.last()
        listing_notification = ListingNotification.objects.filter(listing=listing).first()
        content = ('Your listing "' + listing.name
            + '" has ended with a winning bid of $' + str(created_bid.amount) + '.')
        self.assertEqual(listing_notification.content, content)
        bid_notification = BidNotification.objects.last()
        self.assertEqual(bid_notification.bid, created_bid)
        self.assertEqual(bid_notification.listing.name, listing.name)
        self.assertEqual(bid_notification.user, post_response.wsgi_request.user)

    #Test to ensure that listing receipt is updated when bid is placed
    def test_successful_bid_receipt_is_updated(self):
        listing = self.active_listing
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-bid', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-bid', args=[str(listing.id)]),
            data={'amount': 5.00})
        self.assertEqual(post_response.status_code, 302)
        created_bid = Bid.objects.last()
        self.assertEqual(created_bid.amount, 5.00)
        receipt = Receipt.objects.get(listing=listing)
        self.assertEqual(receipt.exchangee, created_bid.bidder)

    #Test to ensure that a auction ends if autobuy bid is made
    def test_successful_bid_creation_autobuy_ends_listing(self):
        listing = self.active_listing
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-bid', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-bid', args=[str(listing.id)]),
            data={'amount': 25.00})
        self.assertEqual(post_response.status_code, 302)
        updated_listing = AuctionListing.objects.get(id=listing.id)
        self.assertEqual(updated_listing.listingEnded, True)
        listing_notification = ListingNotification.objects.filter(listing=listing).first()
        self.assertEqual(listing_notification.active, True)

    #Test to ensure that rating tickets are made upon creation of the first bid
    def test_successful_bid_creation_rating_tickets_made(self):
        listing = self.active_listing
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-bid', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-bid', args=[str(listing.id)]),
            data={'amount': 5.00})
        self.assertEqual(post_response.status_code, 302)
        created_bid = Bid.objects.last()
        self.assertTrue(RatingTicket.objects.filter(rater=created_bid.bidder,
            receivingUser=listing.owner, listing=listing).exists())
        self.assertTrue(RatingTicket.objects.filter(rater=listing.owner,
            receivingUser=created_bid.bidder, listing=listing).exists())

    #Test to ensure that previous winning bid is set to false and current bid
    #is winning bid, andthat a new notification is made for new bid and
    #notification for previous bid is updated, and rating tickets are updated
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
        self.assertTrue(RatingTicket.objects.filter(rater=created_bid1.bidder,
            receivingUser=listing.owner, listing=listing).exists())
        self.assertTrue(RatingTicket.objects.filter(rater=listing.owner,
            receivingUser=created_bid1.bidder, listing=listing).exists())
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        post_response = self.client.post(reverse('create-bid', args=[str(listing.id)]),
            data={'amount': 6.00})
        self.assertEqual(post_response.status_code, 302)
        edited_bid1 = Bid.objects.get(id=created_bid1.id)
        created_bid2 = Bid.objects.last()
        self.assertEqual(edited_bid1.winningBid, False)
        self.assertEqual(created_bid2.winningBid, True)
        bid_notification = BidNotification.objects.last()
        self.assertEqual(bid_notification.bid, created_bid2)
        self.assertEqual(bid_notification.listing.name, listing.name)
        self.assertEqual(bid_notification.user, post_response.wsgi_request.user)
        previous_bid_notification = BidNotification.objects.get(bid=edited_bid1)
        content = ('Your bid of $' + str(created_bid1.amount) +
            ' has been outbidded by a bid of $' + str(created_bid2.amount) + '.')
        self.assertEqual(previous_bid_notification.content, content)
        self.assertEqual(previous_bid_notification.active, True)
        self.assertTrue(RatingTicket.objects.filter(rater=created_bid2.bidder,
            receivingUser=listing.owner, listing=listing).exists())
        self.assertTrue(RatingTicket.objects.filter(rater=listing.owner,
            receivingUser=created_bid2.bidder, listing=listing).exists())

#Tests for a user to view details on an offer
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

#Tests for a user to accept an offer made on their offer listing
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

            #Create ending notifications for each offer
            content = ('Your offer on "' + self.global_offer_listing1.name
                + '" has expired.')
            OfferNotification.objects.create(
                listing=self.global_offer_listing1, user=self.global_user2,
                creationDate=self.global_offer_listing1.endTime,
                content=content)

        #create offers for an inactive listing to test that a user cannot accept an offer once ended
        self.expired_offer = Offer.objects.create(offerListing=self.global_offer_listing2,
            owner=self.global_user2, amount=7.00)
        expired_offer2 = Offer.objects.create(offerListing=self.global_offer_listing2,
            owner=self.global_user2, amount=7.00)

        content = ('Your listing "' + self.global_offer_listing1.name
            + '" has expired.')
        self.ending_notification = ListingNotification.objects.create(
            listing=self.global_offer_listing1, user=self.global_user1,
            creationDate=self.global_offer_listing1.endTime,
            content=content)
        self.ending_notification_id = self.ending_notification.id

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
    #and that a notification is created for the offer owner
    def test_offer_accepted_field_becomes_true(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.offer
        post_response = self.client.post(reverse('accept-offer', args=[str(offer.id)]))
        self.assertEqual(post_response.status_code, 302)
        updated_offer = Offer.objects.get(id=offer.id)
        self.assertEqual(updated_offer.offerAccepted, True)
        self.assertTrue(OfferNotification.objects.filter(
            listing=self.offer.offerListing, offer=self.offer).exists())

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

    #Test to ensure that the listing receipt is updated
    def test_listing_receipt_is_updated(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.offer
        post_response = self.client.post(reverse('accept-offer', args=[str(offer.id)]))
        self.assertEqual(post_response.status_code, 302)
        listing = OfferListing.objects.get(id=offer.offerListing.id)
        receipt = Receipt.objects.get(listing=listing)
        self.assertEqual(receipt.exchangee, offer.owner)

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

    #Test to ensure that a user cannot accept an offer once listing has ended,
    #also ensure the same amount of offers remain
    def test_offer_not_accepted_listing_ended(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.expired_offer
        response = self.client.get(reverse('accept-offer', args=[str(offer.id)]))
        self.assertRedirects(response, '/listings/offer-listings/{0}'.format(offer.offerListing.id))
        all_listing_offers = Offer.objects.filter(offerListing=self.global_offer_listing2)
        self.assertEqual(len(all_listing_offers), 2)

    #Test to ensure that the ending notification for the listing was deleted
    def test_offer_accepted_ending_notification_deleted(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.offer
        post_response = self.client.post(reverse('accept-offer', args=[str(offer.id)]))
        self.assertEqual(post_response.status_code, 302)
        self.assertFalse(ListingNotification.objects.filter(id=self.ending_notification_id).exists())

    #Test to ensure that the correct number of notifications was made for offers
    #of the listing
    def test_offer_accepted_notifications_made(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.offer
        post_response = self.client.post(reverse('accept-offer', args=[str(offer.id)]))
        self.assertEqual(post_response.status_code, 302)
        self.assertEqual(len(OfferNotification.objects.filter(listing=self.offer.offerListing)), 1)
        acceptance_content = (self.offer.offerListing.owner.username + ' has accepted your' +
            ' offer on the listing "' + self.offer.offerListing.name + '".')
        rejection_content = (self.offer.offerListing.owner.username + ' has accepted a' +
            ' different offer on the listing "' + self.offer.offerListing.name + '".')
        self.assertEqual(len(OfferNotification.objects.filter(
            listing=self.offer.offerListing, content=rejection_content)), 0)
        self.assertEqual(len(OfferNotification.objects.filter(
            listing=self.offer.offerListing, content=acceptance_content)), 1)

    #Test to ensure that Rating Tickets are made upon accepting an offer
    def test_rating_tickets_made_upon_acceptance(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.offer
        post_response = self.client.post(reverse('accept-offer', args=[str(offer.id)]))
        self.assertEqual(post_response.status_code, 302)
        updated_listing = OfferListing.objects.get(id=offer.offerListing.id)
        self.assertTrue(RatingTicket.objects.filter(rater=offer.owner,
            receivingUser=offer.offerListing.owner, listing=offer.offerListing).exists())
        self.assertTrue(RatingTicket.objects.filter(rater=offer.offerListing.owner,
            receivingUser=offer.owner, listing=offer.offerListing).exists())

#Tests for a user to rejector retract an offer they received or made
class OfferDeleteViewTest(MyTestCase):
    def setUp(self):
        super(OfferDeleteViewTest, self).setUp()
        #User that is not associated with offer
        user = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

        #Create offers for testing deletion with along with ending notifications
        self.regular_offer = Offer.objects.create(offerListing=self.global_offer_listing1,
            owner=self.global_user2, amount=7.00, offerAccepted=False)
        content = ('Your offer on the listing "' + self.regular_offer.offerListing.name
            + '" has expired.')
        self.regular_offer_notification = OfferNotification.objects.create(
            listing=self.regular_offer.offerListing, offer=self.regular_offer,
            user=self.regular_offer.owner, content=content,
            creationDate=self.regular_offer.offerListing.endTime,
            type="Listing Expired")
        self.regular_offer_notification_id = self.regular_offer_notification.id

        self.accepted_offer = Offer.objects.create(offerListing=self.global_offer_listing1,
            owner=self.global_user2, amount=7.00, offerAccepted=True)
        content = ('Your offer on the listing "' + self.accepted_offer.offerListing.name
            + '" has expired.')
        self.accepted_offer_notification = OfferNotification.objects.create(
            listing=self.accepted_offer.offerListing, offer=self.accepted_offer,
            user=self.accepted_offer.owner, content=content,
            creationDate=self.accepted_offer.offerListing.endTime,
            type="Listing Expired")
        self.accepted_offer_notification_id = self.accepted_offer_notification.id

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

    #Test to ensure object can be deleted by listing owner, and that a notification
    #is made for offer owner and end notification for offer was deleted
    def test_successful_deletion_by_listing_owner(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.regular_offer
        offer_id = self.regular_offer.id
        offer_owner = offer.owner
        offer_listing = offer.offerListing
        post_response = self.client.post(reverse('delete-offer', args=[str(offer.id)]))
        self.assertRedirects(post_response, reverse('offer-listing-detail', args=[str(self.global_offer_listing1.id)]))
        self.assertFalse(Offer.objects.filter(id=offer_id).exists())
        notification = OfferNotification.objects.last()
        self.assertTrue(notification.listing, offer_listing)
        self.assertTrue(notification.user, offer_owner)
        self.assertTrue(notification.type, "Offer Rejected")
        self.assertFalse(OfferNotification.objects.filter(id=self.regular_offer_notification_id).exists())

    #Test to ensure object can be deleted by offer owner, and that a notification
    #is made for listing owner and end notification for offer was deleted
    def test_successful_deletion_by_offer_owner(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        offer = self.regular_offer
        offer_id = self.regular_offer.id
        listing_owner = offer.offerListing.owner
        offer_listing = offer.offerListing
        post_response = self.client.post(reverse('delete-offer', args=[str(offer.id)]))
        self.assertRedirects(post_response, '/listings/offer-listings/my-offers')
        self.assertFalse(Offer.objects.filter(id=offer_id).exists())
        notification = OfferNotification.objects.last()
        self.assertTrue(notification.listing, offer_listing)
        self.assertTrue(notification.user, listing_owner)
        self.assertTrue(notification.type, "Offer Retracted")
        self.assertFalse(OfferNotification.objects.filter(id=self.regular_offer_notification_id).exists())

    #Test to ensure an accepted offer cannot be soft deleted by listing owner
    def test_unsuccessful_soft_deletion_accepted_offer_by_listing_owner(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.accepted_offer
        offer_id = self.accepted_offer.id
        post_response = self.client.post(reverse('delete-offer', args=[str(offer.id)]))
        self.assertRedirects(post_response, reverse('offer-detail', args=[str(offer.id)]))
        self.assertTrue(Offer.objects.filter(id=offer_id).exists())
        updated_offer = Offer.objects.get(id=offer_id)
        self.assertEqual(updated_offer.owner, self.global_user2)

    #Test to ensure an accepted offer can be soft deleted by offer owner
    def test_successful_soft_deletion_accepted_offer_by_offer_owner(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        offer = self.accepted_offer
        offer_id = self.accepted_offer.id
        post_response = self.client.post(reverse('delete-offer', args=[str(offer.id)]))
        self.assertRedirects(post_response, '/listings/offer-listings/my-offers')
        self.assertTrue(Offer.objects.filter(id=offer_id).exists())
        updated_offer = Offer.objects.get(id=offer_id)
        self.assertEqual(updated_offer.owner, None)

#Tests for a user to edit an offer they have made
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

    #Test to ensure object is edited and listing owner receives notification
    #that offer was updated
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
        notification = OfferNotification.objects.last()
        self.assertTrue(notification.listing, offer.offerListing)
        self.assertTrue(notification.user, offer.offerListing.owner)
        self.assertTrue(notification.type, "Offer Updated")

#Tests for a user to delete a completed or expired auction listing
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
        self.inactive_auction_listing_id = self.inactive_auction_listing.id

        content = ('Your listing "' + self.inactive_auction_listing.name
            + '" has expired.')
        self.inactive_auction_listing_notification = ListingNotification.objects.create(
            listing=self.inactive_auction_listing, user=self.global_user1,
            creationDate=self.inactive_auction_listing.endTime,
            content=content, type="Listing Ended")
        self.inactive_auction_listing_notification_id = self.inactive_auction_listing_notification.id

        self.inactive_auction_listing_no_bids = AuctionListing.objects.create(owner=self.global_user1,
            name='Test Auction Listing', description="Just a test listing", startingBid=5.00,
            minimumIncrement=1.00, autobuy=25.00, endTime=date_inactive)
        self.inactive_auction_listing_no_bids.items.add = self.global_item1
        self.inactive_auction_listing_no_bids.save
        self.inactive_auction_listing_no_bids_id = self.inactive_auction_listing_no_bids.id

        content = ('Your listing "' + self.inactive_auction_listing_no_bids.name
            + '" has expired.')
        self.inactive_auction_listing_no_bids_notification = ListingNotification.objects.create(
            listing=self.inactive_auction_listing_no_bids, user=self.global_user1,
            creationDate=self.inactive_auction_listing_no_bids.endTime,
            content=content, type="Listing Ended")
        self.inactive_auction_listing_no_bids_notification_id = self.inactive_auction_listing_no_bids_notification.id

        self.active_auction_listing = AuctionListing.objects.create(owner=self.global_user1,
            name='Test Auction Listing', description="Just a test listing", startingBid=5.00,
            minimumIncrement=1.00, autobuy=25.00, endTime=date_active)
        self.active_auction_listing.items.add = self.global_item1
        self.active_auction_listing.save

        content = ('Your listing "' + self.active_auction_listing.name
            + '" has expired.')
        self.active_auction_listing_notification = ListingNotification.objects.create(
            listing=self.active_auction_listing, user=self.global_user1,
            creationDate=self.active_auction_listing.endTime,
            content=content, type="Listing Ended")
        self.active_auction_listing_notification_id = self.active_auction_listing_notification.id

        #create some bids for the listing
        number_of_bids = 3

        self.bid_IDs = [0 for number in range(number_of_bids)]

        #Create the winning bid notification
        content = "Nothing"
        self.auction_completed_winner_notification = BidNotification.objects.create(
            listing=self.inactive_auction_listing, user=self.global_user1,
            creationDate=self.inactive_auction_listing.endTime,
            content=content, type="Listing Completed")
        self.auction_completed_winner_notification_id = self.auction_completed_winner_notification.id

        for count in range(number_of_bids):
            new_bid = Bid.objects.create(auctionListing=self.inactive_auction_listing, bidder=self.global_user2,
                amount=(5.00 + (1.00 * count)))
            self.bid_IDs[count] = new_bid.id

            #Update the winning bid notification to match new bid
            content = ('Your bid of $' + str(new_bid.amount) + ' won the listing "' +
                self.inactive_auction_listing.name + '".')
            self.auction_completed_winner_notification.owner = self.global_user2
            self.auction_completed_winner_notification.content = content
            self.auction_completed_winner_notification.bid = new_bid
            self.auction_completed_winner_notification.save()

            #Update the listing ending notification to show what bid won
            content = ('Your listing "' + self.active_auction_listing.name
                + '" has ended with a winning bid of $' + str(new_bid.amount) + '.')
            self.inactive_auction_listing_notification.content = content
            self.inactive_auction_listing_notification.save()

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

    #Test to ensure that user can delete an expired auction listing
    #with no bids
    def test_successful_deletion_expired_listing_no_bids(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.inactive_auction_listing_no_bids
        post_response = self.client.post(reverse('delete-auction-listing', args=[str(listing.id)]))
        self.assertRedirects(post_response, reverse('auction-listings'))
        self.assertFalse(AuctionListing.objects.filter(id=self.inactive_auction_listing_no_bids_id).exists())
        self.assertFalse(ListingNotification.objects.filter(id=self.inactive_auction_listing_no_bids_notification_id).exists())

    #Test to ensure that user can soft delete an expired auction listing
    #with bids
    def test_successful_soft_deletion_expired_listing_bids(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.inactive_auction_listing
        post_response = self.client.post(reverse('delete-auction-listing', args=[str(listing.id)]))
        self.assertRedirects(post_response, reverse('auction-listings'))
        self.assertTrue(AuctionListing.objects.filter(id=self.inactive_auction_listing_id).exists())
        updated_listing = AuctionListing.objects.get(id=self.inactive_auction_listing_id)
        self.assertEqual(updated_listing.owner, None)
        self.assertFalse(ListingNotification.objects.filter(id=self.inactive_auction_listing_id).exists())

#Tests for a user to view events they're hosting and participating in
class EventListViewTest(MyTestCase):
    def setUp(self):
        super(EventListViewTest, self).setUp()

        #Create a user to invite to an event
        user1 = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

        self.number_of_events_user1 = 3 #1 global event
        self.number_of_events_user2 = 6 #1 global event
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
        self.assertEqual(len(response.context['events']), 4)

    #Test to ensure that the user only sees events they're hosting for user2
    def test_list_only_current_users_events_user2(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['events']), 7)

    #Test to ensure that the user only sees events they've been invited to for user3
    def test_list_only_current_users_events_user3(self):
        login = self.client.login(username='mike', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['events']), self.number_of_events_user3)

#Tests for a user to view details on an event
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

    #Test to ensure user is redirected if they are not part of the event
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

#Tests for a user to create an event
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

#Tests for a user to edit an event they're hosting
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

#Tests for a user to remove a user from an event they're hosting
class RemoveParticipantViewTest(MyTestCase):
    def setUp(self):
        super(RemoveParticipantViewTest, self).setUp()

        #Create a user to add to event
        self.user1 = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)
        self.global_event.participants.add(self.user1)
        self.global_event.save()

        self.user12 = User.objects.create_user(username="mikey", password="example",
            email="exampley@text.com", paypalEmail="exampley@text.com",
            invitesOpen=True, inquiriesOpen=True)

    #Test to ensure that a user must be logged in to remove a participant
    def test_redirect_if_not_logged_in(self):
        event = self.global_event
        response = self.client.get(reverse('remove-participant', args=[str(event.id), str(self.user1.id)]))
        self.assertRedirects(response, '/accounts/login/?next=/listings/events/{0}/remove-participant/{1}'.format(event.id, self.user1.id))

    #Test to ensure user is redirected to event detail page if logged in if they are the host after removing participant
    def test_redirect_to_event_if_logged_in_host(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('remove-participant', args=[str(event.id), str(self.user1.id)]))
        self.assertRedirects(response, '/listings/events/{0}'.format(event.id))

    #Test to ensure user is redirected to events list view if logged in if they are a participant
    #after removing themselves
    def test_no_redirect_if_logged_in_participant(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('remove-participant', args=[str(event.id), str(self.global_user2.id)]))
        self.assertRedirects(response, '/listings/events/')

    #Test to ensure user is redirected if they are not part of the event
    def test_redirect_if_logged_in_not_host_or_participant(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('remove-participant', args=[str(event.id), str(self.global_user2.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is redirected if they are trying to remove a different user
    def test_redirect_if_logged_in_not_host_or_participant(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('remove-participant', args=[str(event.id), str(self.user1.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure that the host can remove a participant from the event, and
    #removed user receives a notification
    def test_user_is_removed_by_host(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        event = self.global_event
        post_response = self.client.post(reverse('remove-participant', args=[str(event.id), str(self.user1.id)]))
        self.assertEqual(post_response.status_code, 302)
        updated_event = Event.objects.get(id=event.id)
        self.assertFalse(event.participants.filter(pk=self.user1.pk).exists())
        notification = EventNotification.objects.last()
        self.assertEqual(notification.event, event)
        self.assertEqual(notification.user, self.user1)
        self.assertEqual(notification.type, "Participant Removed")

    #Test to ensure that a participant can remove themselves from the event,
    #and that the host receives a notification
    def test_user_can_remove_themselves(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        event = self.global_event
        post_response = self.client.post(reverse('remove-participant', args=[str(event.id), str(self.global_user2.id)]))
        self.assertEqual(post_response.status_code, 302)
        updated_event = Event.objects.get(id=event.id)
        self.assertFalse(event.participants.filter(pk=self.global_user2.pk).exists())
        notification = EventNotification.objects.last()
        self.assertEqual(notification.event, event)
        self.assertEqual(notification.user, event.host)
        self.assertEqual(notification.type, "Participant Left")

#Tests for a user to delete an event they're hosting
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

#Tests for a user to view invites they have received
class InvitationListViewTest(MyTestCase):
    def setUp(self):
        super(InvitationListViewTest, self).setUp()

        #Create a user to host an event
        user1 = User.objects.create_user(username="mike", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

        self.number_of_events1 = 5
        self.number_of_events2 = 3

        #Create the events invitations for the 1st user
        for num in range(self.number_of_events1):
            event = Event.objects.create(host=user1,
                title="My Awesome Event", context="Please come to my event.",
                date="2020-11-06 15:00", location="1234 Sesame Street")
            Invitation.objects.create(event=event, recipient=self.global_user1)
            Invitation.objects.create(event=event, recipient=self.global_user2)

        #Create the events for the 2nd user
        for num in range(self.number_of_events2):
            event = Event.objects.create(host=user1,
                title="My Cool Event", context="Please come to my event.",
                date="2020-11-06 15:00", location="1234 Sesame Street")
            Invitation.objects.create(event=event, recipient=self.global_user1)

    #Test to ensure that a user must be logged in to view invitations
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('invitations'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/invitations/')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('invitations'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('invitations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/invitations.html')

    #Test to ensure that the user only sees invitations they've received for user1
    def test_list_only_invitations_for_user1(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('invitations'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['invitations']), 8)

    #Test to ensure that the user only sees invitations they've received for user2
    def test_list_only_invitations_for_user2(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('invitations'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['invitations']), 5)

#Tests for a user to create invitations for users to an event they're hosting
class CreateInvitationsViewTest(MyTestCase):
    def setUp(self):
        super(CreateInvitationsViewTest, self).setUp()
        self.user1 = User.objects.create(username="mikey", password="example",
            email="exampley@text.com", paypalEmail="exampley@text.com",
            invitesOpen=True, inquiriesOpen=True)
        self.user2 = User.objects.create(username="mikel", password="example",
            email="examplel@text.com", paypalEmail="examplel@text.com",
            invitesOpen=True, inquiriesOpen=True)
        self.user3 = User.objects.create(username="mikes", password="example",
            email="examples@text.com", paypalEmail="examples@text.com",
            invitesOpen=True, inquiriesOpen=True)

        #Set the locations of the global users
        self.global_user1.profile.latitude = 40.0000
        self.global_user1.profile.longitude = -75.0000
        self.global_user1.profile.save()

        self.user1.profile.latitude = 40.5000
        self.user1.profile.longitude = -75.5000
        self.user1.profile.save()

        self.user2.profile.latitude = 40.6000
        self.user2.profile.longitude = -75.6000
        self.user2.profile.save()

        self.user3.profile.latitude = 40.7000
        self.user3.profile.longitude = -75.7000
        self.user3.profile.save()

    #Test to ensure that a user must be logged in to create invitations
    def test_redirect_if_not_logged_in(self):
        event = self.global_event
        response = self.client.get(reverse('create-invitations', args=[str(event.id)]))
        self.assertRedirects(response, '/accounts/login/?next=/listings/events/{0}/create-invitations'.format(event.id))

    #Test to ensure user is not redirected if logged in and are the host of the event
    def test_no_redirect_if_logged_in_host(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('create-invitations', args=[str(event.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged but are not the host of the event
    def test_redirect_if_logged_in_not_host(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('create-invitations', args=[str(event.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('create-invitations', args=[str(event.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/create_invitations.html')

    #Test to ensure that a user is able to create invitations for all users,
    #and that notifications are created for the users
    def test_invitations_are_created(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('create-invitations', args=[str(event.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-invitations', args=[str(event.id)]),
            data={'users': [str(self.user1.id), str(self.user2.id), str(self.user3.id)]})
        self.assertEqual(post_response.status_code, 302)
        self.assertTrue(Invitation.objects.filter(event=event,
            recipient=self.user1).exists())
        self.assertTrue(Invitation.objects.filter(event=event,
            recipient=self.user2).exists())
        self.assertTrue(Invitation.objects.filter(event=event,
            recipient=self.user3).exists())
        self.assertTrue(InvitationNotification.objects.filter(event=event,
            user=self.user1).exists())
        self.assertTrue(InvitationNotification.objects.filter(event=event,
            user=self.user2).exists())
        self.assertTrue(InvitationNotification.objects.filter(event=event,
            user=self.user3).exists())

    #Test to ensure user is redirected to event detail if form was valid
    def test_invitations_are_created_redirect(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('create-invitations', args=[str(event.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-invitations', args=[str(event.id)]),
            data={'users': [str(self.user1.id), str(self.user2.id), str(self.user3.id)]})
        self.assertEqual(post_response.status_code, 302)
        self.assertRedirects(post_response, '/listings/events/{0}'.format(event.id))

#Tests for a user to accept an invitation they have received
class AcceptInvitationViewTest(MyTestCase):
    def setUp(self):
        super(AcceptInvitationViewTest, self).setUp()

        #Create user to test with
        self.user1 = User.objects.create_user(username="mikey", password="example",
            email="exampley@text.com", paypalEmail="exampley@text.com",
            invitesOpen=True, inquiriesOpen=True)

        #create an invitation for testing
        self.invitation = Invitation.objects.create(event=self.global_event,
            recipient=self.user1)

    #Test to ensure that a user must be logged in to accept an invitation
    def test_redirect_if_not_logged_in(self):
        invitation = self.invitation
        response = self.client.get(reverse('accept-invitation', args=[str(invitation.id)]))
        self.assertRedirects(response, '/accounts/login/?next=/listings/invitations/{0}/accept'.format(invitation.id))

    #Test to ensure user if logged in is redirected to event after accepting if they are recipient
    def test_redirect_to_event_if_logged_in_recipient(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        invitation = self.invitation
        event = invitation.event
        response = self.client.get(reverse('accept-invitation', args=[str(invitation.id)]))
        self.assertRedirects(response, '/listings/events/{0}'.format(event.id))

    #Test to ensure user is redirected if they are not the recipient of the invitation
    def test_redirect_if_logged_in_not_recipient(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        invitation = self.invitation
        response = self.client.get(reverse('accept-invitation', args=[str(invitation.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure that the event's participants are updated with the user
    #that accepted, and host receives notification
    def test_user_is_added_to_event(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        invitation = self.invitation
        event = invitation.event
        post_response = self.client.post(reverse('accept-invitation', args=[str(invitation.id)]))
        self.assertEqual(post_response.status_code, 302)
        updated_event = Event.objects.get(id=event.id)
        self.assertTrue(event.participants.filter(pk=self.user1.pk).exists())
        notification = EventNotification.objects.last()
        self.assertEqual(notification.event, event)
        self.assertEqual(notification.user, event.host)
        self.assertEqual(notification.type, "Participant Joined")

    #Test to ensure that the invitation is destroyed after user accepts it
    def test_invitation_destroyed_after_acceptance(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        invitation = self.invitation
        invitation_id = invitation.id
        post_response = self.client.post(reverse('accept-invitation', args=[str(invitation.id)]))
        self.assertEqual(post_response.status_code, 302)
        self.assertFalse(Invitation.objects.filter(id=invitation_id).exists())

#Tests for a user to deceline an invitation they received
class DeclineInvitationViewTest(MyTestCase):
    def setUp(self):
        super(DeclineInvitationViewTest, self).setUp()

        #Create user to test with
        self.user1 = User.objects.create_user(username="mikey", password="example",
            email="exampley@text.com", paypalEmail="exampley@text.com",
            invitesOpen=True, inquiriesOpen=True)

        #create an invitation for testing
        self.invitation = Invitation.objects.create(event=self.global_event,
            recipient=self.user1)

    #Test to ensure that a user must be logged in to decline an invitation
    def test_redirect_if_not_logged_in(self):
        invitation = self.invitation
        response = self.client.get(reverse('decline-invitation', args=[str(invitation.id)]))
        self.assertRedirects(response, '/accounts/login/?next=/listings/invitations/{0}/decline'.format(invitation.id))

    #Test to ensure user if logged in is redirected to invitations after rejecting invite
    def test_redirect_to_invitations_if_logged_in_recipient(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        invitation = self.invitation
        post_response = self.client.post(reverse('decline-invitation', args=[str(invitation.id)]))
        self.assertRedirects(post_response, '/listings/invitations/')

    #Test to ensure user is redirected if they are not the recipient of the invitation
    def test_redirect_if_logged_in_not_recipient(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        invitation = self.invitation
        response = self.client.get(reverse('decline-invitation', args=[str(invitation.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure that the user is not added to event after declining, and
    #that host receives a notification
    def test_user_is_not_added_to_event(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        invitation = self.invitation
        event = invitation.event
        post_response = self.client.post(reverse('decline-invitation', args=[str(invitation.id)]))
        self.assertEqual(post_response.status_code, 302)
        refreshed_event = Event.objects.get(id=event.id)
        self.assertFalse(event.participants.filter(pk=self.user1.pk).exists())
        notification = EventNotification.objects.last()
        self.assertEqual(notification.event, event)
        self.assertEqual(notification.user, event.host)
        self.assertEqual(notification.type, "Participant Declined")

    #Test to ensure that the invitation is destroyed after user declines it
    def test_invitation_destroyed_after_declining(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        invitation = self.invitation
        invitation_id = invitation.id
        post_response = self.client.post(reverse('decline-invitation', args=[str(invitation.id)]))
        self.assertEqual(post_response.status_code, 302)
        self.assertFalse(Invitation.objects.filter(id=invitation_id).exists())

#Tests for a user to view details of a wishlist
class WishlistDetailViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to view wishlists
    def test_redirect_if_not_logged_in(self):
        wishlist = self.global_wishlist
        response = self.client.get(reverse('wishlist-detail', args=[str(wishlist.id)]))
        self.assertRedirects(response, '/accounts/login/?next=/listings/wishlists/{0}'.format(wishlist.id))

    #Test to ensure owner is not redirected if logged in
    def test_no_redirect_if_logged_in_owner(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        wishlist = self.global_wishlist
        response = self.client.get(reverse('wishlist-detail', args=[str(wishlist.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure non owner is not redirected if logged in
    def test_no_redirect_if_logged_in_not_owner(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        wishlist = self.global_wishlist
        response = self.client.get(reverse('wishlist-detail', args=[str(wishlist.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        wishlist = self.global_wishlist
        response = self.client.get(reverse('wishlist-detail', args=[str(wishlist.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlists/wishlist_detail.html')

#Tests for a user to create a wishlist
class CreateWishlistViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to create a wishlist
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('create-wishlist'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/wishlists/create-wishlist')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-wishlist'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlists/create_wishlist.html')

    #Test to ensure that a user is able to create a wishlist and have it relate to them
    def test_wishlist_is_created(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-wishlist'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-wishlist'),
            data={'title': "My Wishlist", 'description': "I want this stuff.",
                'items': [str(self.global_item2.id)]})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist = Wishlist.objects.last()
        self.assertEqual(new_wishlist.owner, post_response.wsgi_request.user)

    #Test to ensure user is redirected to wishlist detail view if form was valid
    def test_wishlist_is_created_redirect(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-wishlist'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-wishlist'),
            data={'title': "My Wishlist", 'description': "I want this stuff.",
                'items': [str(self.global_item2.id)]})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist = Wishlist.objects.last()
        self.assertRedirects(post_response, '/listings/wishlists/{0}'.format(new_wishlist.id))

    #Test to ensure that a user is redirected if they already have a wishlist
    def test_redirect_if_user_has_already_made_wishlist(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-wishlist'))
        self.assertRedirects(response, '/listings/')

#Tests for a user to edit their wishlist
class EditWishlistViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to edit their wishlist
    def test_redirect_if_not_logged_in(self):
        wishlist = self.global_wishlist
        response = self.client.get(reverse('edit-wishlist', args=[str(wishlist.id)]))
        self.assertRedirects(response, '/accounts/login/?next=/listings/wishlists/{0}/edit'.format(wishlist.id))

    #Test to ensure user is not redirected if logged in and owns the wishlist
    def test_no_redirect_if_logged_in_owner(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        wishlist = self.global_wishlist
        response = self.client.get(reverse('edit-wishlist', args=[str(wishlist.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in but does not own the wishlist
    def test_redirect_if_logged_in_not_owner(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        wishlist = self.global_wishlist
        response = self.client.get(reverse('edit-wishlist', args=[str(wishlist.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        wishlist = self.global_wishlist
        response = self.client.get(reverse('edit-wishlist', args=[str(wishlist.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlists/edit_wishlist.html')

    #Test to ensure that a user is able to edit the wishlist successfully
    def test_wishlist_is_updated(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        wishlist = self.global_wishlist
        response = self.client.get(reverse('edit-wishlist', args=[str(wishlist.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('edit-wishlist', args=[str(wishlist.id)]),
            data={'title': "My Cool Wishlist", 'description': "Stuff I would love to buy"})
        self.assertEqual(post_response.status_code, 302)
        edited_wishlist = Wishlist.objects.get(id=wishlist.id)
        self.assertEqual(edited_wishlist.title, 'My Cool Wishlist')
        self.assertEqual(edited_wishlist.description, 'Stuff I would love to buy')
        self.assertEqual(edited_wishlist.items.count(), 0)

#Tests for a user to remove an item from their wishlist
class RemoveWishlistItemViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to remove an tem from wishlist
    def test_redirect_if_not_logged_in(self):
        wishlist = self.global_wishlist
        item = self.global_item1
        response = self.client.get(reverse('remove-wishlist-item',
            args=[str(wishlist.id), str(item.id)]))
        self.assertRedirects(response,
            '/accounts/login/?next=/listings/wishlists/{0}/remove-wishlist-item/{1}'.format(wishlist.id, item.id))

    #Test to ensure user is redirected to wishlist detail page if logged in if
    #they are the owner after removing an item
    def test_redirect_to_wishlist_if_logged_in_owner(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        wishlist = self.global_wishlist
        item = self.global_item1
        response = self.client.get(reverse('remove-wishlist-item',
            args=[str(wishlist.id), str(item.id)]))
        self.assertRedirects(response, '/listings/wishlists/{0}'.format(wishlist.id))

    #Test to ensure user is redirected if they do not own the wishlist
    def test_redirect_if_logged_in_not_owner(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        wishlist = self.global_wishlist
        item = self.global_item1
        response = self.client.get(reverse('remove-wishlist-item',
            args=[str(wishlist.id), str(item.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure that the user can remove an item succesfully from wishlist
    def test_item_is_removed_succesfully(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        wishlist = self.global_wishlist
        item = self.global_item1
        post_response = self.client.post(reverse('remove-wishlist-item',
            args=[str(wishlist.id), str(item.id)]))
        self.assertEqual(post_response.status_code, 302)
        updated_wishlist = Wishlist.objects.get(id=wishlist.id)
        self.assertFalse(wishlist.items.filter(pk=item.id).exists())

    #Test to ensure that removal fails if user tries to remove an item that is not in wihslist
    def test_invalid_removal_item_does_not_exist(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        wishlist = self.global_wishlist
        item = self.global_item2
        post_response = self.client.post(reverse('remove-wishlist-item',
            args=[str(wishlist.id), str(item.id)]))
        self.assertRedirects(post_response, '/listings/')

#Tests for a user to view wishlist listings they have made
class WishlistListingsViewTest(MyTestCase):
    def setUp(self):
        super(WishlistListingsViewTest, self).setUp()

        #Set number of listings for each user
        number_of_listings_user1 = 6
        number_of_listings_user2 = 9

        #Get the current date and time for testing and create active endTimes
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        for num in range(number_of_listings_user1):
            listing = WishlistListing.objects.create(owner=self.global_user1,
                name='My Wishlist Listing #{0}'.format(num), endTime=date_active,
                moneyOffer=5.00, notes="Just a test")
            listing.items.add(self.global_item1)
            listing.itemsOffer.add(self.global_item1)
            listing.save

        for num in range(number_of_listings_user2):
            listing = WishlistListing.objects.create(owner=self.global_user2,
                name='My Wishlist Listing #{0}'.format(num), endTime=date_active,
                moneyOffer=15.00, notes="Just a test")
            listing.items.add(self.global_item2)
            listing.itemsOffer.add(self.global_item2)
            listing.save

    #Test to ensure that a user must be logged in to view their wishlist listings
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('wishlist-listings'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/wishlists/wishlist-listings')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('wishlist-listings'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('wishlist-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlists/wishlist_listings.html')

    #Test to ensure that the user only sees wishlist listings they've uploaded for user1
    def test_list_only_current_users_listings_user1(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('wishlist-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['wishlistlistings']) == 6)

    #Test to ensure that the user only sees wishlist listings they've uploaded for user2
    def test_list_only_current_users_listings_user2(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('wishlist-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['wishlistlistings']) == 9)

#Tests for a user to view details on a wishlist listing
class WishlistListingDetailViewTest(MyTestCase):
    def setUp(self):
        super(WishlistListingDetailViewTest, self).setUp()

        #Get the current date and time for testing and create active endTimes
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        #Set the locations of the global users
        self.global_user1.profile.latitude = 40.0000
        self.global_user1.profile.longitude = -75.0000
        self.global_user1.profile.save()

        self.global_user2.profile.latitude = 40.5000
        self.global_user2.profile.longitude = -75.5000
        self.global_user2.profile.save()

        #Wishlist listing to test with
        self.listing = WishlistListing.objects.create(owner=self.global_user1,
            name='My Wishlist Listing', endTime=date_active,
            moneyOffer=5.00, notes="Just a test",
            latitude=self.global_user1.profile.latitude,
            longitude=self.global_user1.profile.longitude)
        self.listing.items.add(self.global_item1)
        self.listing.save

        #Create an additional user for testing with
        self.new_user2 = User.objects.create_user(username="mike4",
            password="example", email="example5@text.com",
            paypalEmail="example5@text.com", invitesOpen=True,
            inquiriesOpen=True)

        self.new_user2.profile.latitude = 42.0000
        self.new_user2.profile.longitude = -77.000
        self.new_user2.profile.save()

    #Test to ensure that a user must be logged in to view wishlist listings
    def test_redirect_if_not_logged_in(self):
        listing = self.listing
        response = self.client.get(reverse('wishlist-listing-detail', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure owner is not redirected if logged in
    def test_no_redirect_if_logged_in_owner(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.listing
        response = self.client.get(reverse('wishlist-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure non owner is not redirected if logged in and is within a
    #50 mile radius of listing owner
    def test_no_redirect_if_logged_in_not_owner_nearby(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        listing = self.listing
        response = self.client.get(reverse('wishlist-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure non owner is redirected if logged in and is within a
    #50 mile radius of listing owner
    def test_redirect_if_logged_in_not_owner_not_nearby(self):
        login = self.client.login(username='mike4', password='example')
        self.assertTrue(login)
        listing = self.listing
        response = self.client.get(reverse('wishlist-listing-detail', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.listing
        response = self.client.get(reverse('wishlist-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlists/wishlist_listing_detail.html')

    #Test to ensure owner is not redirected if logged in and listing has ended
    def test_no_redirect_if_logged_in_owner_listing_ended(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        self.listing.endTime = timezone.localtime(timezone.now())
        self.listing.save()
        listing = self.listing
        response = self.client.get(reverse('wishlist-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure non owner is redirected if logged in but listing has
    #ended
    def test_no_redirect_if_logged_in_not_owner_nearby(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        self.listing.endTime = timezone.localtime(timezone.now())
        self.listing.save()
        listing = self.listing
        response = self.client.get(reverse('wishlist-listing-detail', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

#Tests for a user to view wishlist listngs within a 20 mile radius of them
class AllWishlistListingsViewTest(MyTestCase):
    def setUp(self):
        super(AllWishlistListingsViewTest, self).setUp()

        #Create a variety of listings to test with
        #Number of active listings should be 9
        number_of_active_listings_user1 = 3
        number_of_active_listings_user2 = 6
        number_of_inactive_listings_user1 = 7

        #Set the locations of the users
        self.global_user1.profile.latitude = 40.0000
        self.global_user1.profile.longitude = -75.0000
        self.global_user1.profile.save()

        self.global_user2.profile.latitude = 41.0000
        self.global_user2.profile.longitude = -69.0000
        self.global_user2.profile.save()

        date_ended = timezone.localtime(timezone.now()) - timedelta(hours=1)
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        for num in range(number_of_active_listings_user1):
            listing = WishlistListing.objects.create(owner=self.global_user1,
                name='My Wishlist Listing #{0}'.format(num), endTime=date_active,
                moneyOffer=5.00, notes="Just a test", latitude=40.0300,
                longitude=-74.9800)
            listing.items.add(self.global_item1)
            listing.itemsOffer.add(self.global_non_wishlist_item)
            listing.save

        for num in range(number_of_active_listings_user2):
            listing = WishlistListing.objects.create(owner=self.global_user2,
                name='My Wishlist Listing #{0}'.format(num), endTime=date_active,
                moneyOffer=5.00, notes="Just a test", latitude=40.9800,
                longitude=-69.0200)
            listing.items.add(self.global_item2)
            listing.save

        for num in range(number_of_inactive_listings_user1):
            listing = WishlistListing.objects.create(owner=self.global_user1,
                name='My Wishlist Listing #{0}'.format(num), endTime=date_ended,
                moneyOffer=5.00, notes="Just a test", latitude=40.0300,
                longitude=-74.9800)
            listing.items.add(self.global_item1)
            listing.save

    #Test to ensure that a user must be logged in to view listings
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('all-wishlist-listings'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/wishlists/wishlist-listings/all')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('all-wishlist-listings'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('all-wishlist-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlists/all_wishlist_listings.html')

    #Test to ensure that a user sees the correct amount of active listings
    def test_list_only_active_listings_page_1(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('all-wishlist-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['wishlistlistings']), 3)

    #Test to ensure that different user sees the correct amount of active listings
    def test_list_only_active_listings_new_user_page_1(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('all-wishlist-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['wishlistlistings']), 6)

#Tests for a user to create a wishlist listing
class CreateWishlistListingViewTest(MyTestCase):
    def setUp(self):
        super(CreateWishlistListingViewTest, self).setUp()

        self.global_user1.profile.latitude = 44.0265
        self.global_user1.profile.longitude = -75.8499
        self.global_user1.profile.save()

    #Test to ensure that a user must be logged in to create wishlist listing
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('create-wishlist-listing'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/wishlists/wishlist-listings/create-wishlist-listing')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-wishlist-listing'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in but have not made a wishlist
    def test_redirect_if_logged_in_no_wishlist(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-wishlist-listing'))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-wishlist-listing'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlists/create_wishlist_listing.html')

    #Test to ensure that a user is able to create an wishlist listing and have it relate to them
    def test_wishlist_listing_is_created(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-wishlist-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-wishlist-listing'),
            data={'name': "My Wishlist Listing", 'endTimeChoices': "1h",
                'items': [str(self.global_item1.id)],
                'moneyOffer': 10.00, 'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Only looking for items that haven't been used."})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist_listing = WishlistListing.objects.last()
        self.assertEqual(new_wishlist_listing.owner, post_response.wsgi_request.user)
        self.assertEqual(str(new_wishlist_listing.latitude), '44.0265')
        self.assertEqual(str(new_wishlist_listing.longitude), '-75.8499')

    #Test to ensure that a user is able to create an wishlist listing and have it
    #end in 1 hour if endtime choice is 1h
    def test_wishlist_listing_is_created_correct_1h(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-wishlist-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-wishlist-listing'),
            data={'name': "My Wishlist Listing", 'endTimeChoices': "1h",
                'items': [str(self.global_item1.id)],
                'moneyOffer': 10.00, 'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Only looking for items that haven't been used."})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist_listing = WishlistListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=1)
        to_tz = timezone.get_default_timezone()
        new_wishlist_listing_endtime = new_wishlist_listing.endTime
        new_wishlist_listing_endtime = new_wishlist_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_wishlist_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that a user is able to create an wishlist listing and have it
    #end in 2 hours if endtime choice is 2h
    def test_wishlist_listing_is_created_correct_2h(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-wishlist-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-wishlist-listing'),
            data={'name': "My Wishlist Listing", 'endTimeChoices': "2h",
                'items': [str(self.global_item1.id)],
                'moneyOffer': 10.00, 'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Only looking for items that haven't been used."})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist_listing = WishlistListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=2)
        to_tz = timezone.get_default_timezone()
        new_wishlist_listing_endtime = new_wishlist_listing.endTime
        new_wishlist_listing_endtime = new_wishlist_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_wishlist_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that a user is able to create an wishlist listing and have it
    #end in 4 hours if endtime choice is 4h
    def test_wishlist_listing_is_created_correct_4h(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-wishlist-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-wishlist-listing'),
            data={'name': "My Wishlist Listing", 'endTimeChoices': "4h",
                'items': [str(self.global_item1.id)],
                'moneyOffer': 10.00, 'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Only looking for items that haven't been used."})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist_listing = WishlistListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=4)
        to_tz = timezone.get_default_timezone()
        new_wishlist_listing_endtime = new_wishlist_listing.endTime
        new_wishlist_listing_endtime = new_wishlist_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_wishlist_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that a user is able to create an wishlist listing and have it
    #end in 8 hours if endtime choice is 8h
    def test_wishlist_listing_is_created_correct_8h(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-wishlist-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-wishlist-listing'),
            data={'name': "My Wishlist Listing", 'endTimeChoices': "8h",
                'items': [str(self.global_item1.id)],
                'moneyOffer': 10.00, 'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Only looking for items that haven't been used."})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist_listing = WishlistListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=8)
        to_tz = timezone.get_default_timezone()
        new_wishlist_listing_endtime = new_wishlist_listing.endTime
        new_wishlist_listing_endtime = new_wishlist_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_wishlist_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that a user is able to create an wishlist listing and have it
    #end in 12 hours if endtime choice is 12h
    def test_wishlist_listing_is_created_correct_12h(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-wishlist-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-wishlist-listing'),
            data={'name': "My Wishlist Listing", 'endTimeChoices': "12h",
                'items': [str(self.global_item1.id)],
                'moneyOffer': 10.00, 'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Only looking for items that haven't been used."})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist_listing = WishlistListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=12)
        to_tz = timezone.get_default_timezone()
        new_wishlist_listing_endtime = new_wishlist_listing.endTime
        new_wishlist_listing_endtime = new_wishlist_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_wishlist_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that a user is able to create an wishlist listing and have it
    #end in 1 day if endtime choice is 1d
    def test_wishlist_listing_is_created_correct_1d(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-wishlist-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-wishlist-listing'),
            data={'name': "My Wishlist Listing", 'endTimeChoices': "1d",
                'items': [str(self.global_item1.id)],
                'moneyOffer': 10.00, 'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Only looking for items that haven't been used."})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist_listing = WishlistListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(days=1)
        to_tz = timezone.get_default_timezone()
        new_wishlist_listing_endtime = new_wishlist_listing.endTime
        new_wishlist_listing_endtime = new_wishlist_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_wishlist_listing_endtime.day, end_time_check.day)

    #Test to ensure that a user is able to create an wishlist listing and have it
    #end in 3 days if endtime choice is 3d
    def test_wishlist_listing_is_created_correct_3d(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-wishlist-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-wishlist-listing'),
            data={'name': "My Wishlist Listing", 'endTimeChoices': "3d",
                'items': [str(self.global_item1.id)],
                'moneyOffer': 10.00, 'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Only looking for items that haven't been used."})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist_listing = WishlistListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(days=3)
        to_tz = timezone.get_default_timezone()
        new_wishlist_listing_endtime = new_wishlist_listing.endTime
        new_wishlist_listing_endtime = new_wishlist_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_wishlist_listing_endtime.day, end_time_check.day)

    #Test to ensure that a user is able to create an wishlist listing and have it
    #end in 7 days if endtime choice is 7d
    def test_wishlist_listing_is_created_correct_7d(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-wishlist-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-wishlist-listing'),
            data={'name': "My Wishlist Listing", 'endTimeChoices': "7d",
                'items': [str(self.global_item1.id)],
                'moneyOffer': 10.00, 'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Only looking for items that haven't been used."})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist_listing = WishlistListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(days=7)
        to_tz = timezone.get_default_timezone()
        new_wishlist_listing_endtime = new_wishlist_listing.endTime
        new_wishlist_listing_endtime = new_wishlist_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_wishlist_listing_endtime.day, end_time_check.day)

    #Test to ensure that a user is able to create an wishlist listing and if moneyOffer
    #is left blank, it becomes $0.00
    def test_wishlist_listing_is_created_no_money_offer(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-wishlist-listing'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-wishlist-listing'),
            data={'name': "My Wishlist Listing", 'endTimeChoices': "1h",
                'items': [str(self.global_item1.id)],
                'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Only looking for items that haven't been used."})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist_listing = WishlistListing.objects.last()
        self.assertEqual(new_wishlist_listing.moneyOffer, 0.00)

#Tests for a user to edit a wishlist listing they own
class EditWishlistListingViewTest(MyTestCase):
    def setUp(self):
        super(EditWishlistListingViewTest, self).setUp()

        #Get the current date and time for testing and create active and
        #inactive endTimes
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)
        date_ended = timezone.localtime(timezone.now()) - timedelta(days=1)

        #Wishlist listings to test with
        self.listing = WishlistListing.objects.create(owner=self.global_user1,
            name='My Wishlist Listing', endTime=date_active,
            moneyOffer=5.00, notes="Just a test")
        self.listing.items.add(self.global_item1)
        self.listing.save

        self.expired_listing = WishlistListing.objects.create(owner=self.global_user1,
            name='My Wishlist Listing', endTime=date_ended,
            moneyOffer=5.00, notes="Just a test")
        self.expired_listing.items.add(self.global_item1)
        self.expired_listing.save

    #Test to ensure that a user must be logged in to edit a  wishlist listings
    def test_redirect_if_not_logged_in(self):
        listing = self.listing
        response = self.client.get(reverse('edit-wishlist-listing', args=[str(listing.id)]))
        self.assertRedirects(response,
            '/accounts/login/?next=/listings/wishlists/wishlist-listings/{0}/edit'.format(listing.id))

    #Test to ensure owner is not redirected if logged in
    def test_no_redirect_if_logged_in_owner(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.listing
        response = self.client.get(reverse('edit-wishlist-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure non owner is redirected if logged in
    def test_redirect_if_logged_in_not_owner(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        listing = self.listing
        response = self.client.get(reverse('edit-wishlist-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure owner is redirected if listing has expired
    def test_redirect_if_logged_in_owner_listing_expired(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.expired_listing
        response = self.client.get(reverse('edit-wishlist-listing', args=[str(listing.id)]))
        self.assertRedirects(response,
            '/listings/wishlists/{0}'.format(self.global_user1.wishlist.id))

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.listing
        response = self.client.get(reverse('edit-wishlist-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlists/edit_wishlist_listing.html')

    #Test to ensure that a user is able to edit a wishlist listing sucessfully
    def test_wishlist_listing_is_edited_sucessfully(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.listing
        response = self.client.get(reverse('edit-wishlist-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('edit-wishlist-listing', args=[str(listing.id)]),
            data={'name': "My Awesome Wishlist Listing",  'items': [str(self.global_item1.id)],
                'moneyOffer': 10.00, 'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Just a simple update"})
        self.assertEqual(post_response.status_code, 302)
        updated_wishlist_listing = WishlistListing.objects.get(id=listing.id)
        self.assertEqual(updated_wishlist_listing.name, "My Awesome Wishlist Listing")
        self.assertEqual(updated_wishlist_listing.moneyOffer, 10.00)
        self.assertEqual(updated_wishlist_listing.notes, "Just a simple update")

#Tests for a user to relist an expired wishlist listing
class RelistWishlistListingViewTest(MyTestCase):
    def setUp(self):
        super(RelistWishlistListingViewTest, self).setUp()

        #Get the current date and time for testing and create active and
        #inactive endTimes
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)
        date_ended = timezone.localtime(timezone.now()) - timedelta(days=1)

        #Wishlist listings to test with
        self.active_listing = WishlistListing.objects.create(owner=self.global_user1,
            name='My Wishlist Listing', endTime=date_active,
            moneyOffer=5.00, notes="Just a test")
        self.active_listing.items.add(self.global_item1)
        self.active_listing.save

        self.expired_listing = WishlistListing.objects.create(owner=self.global_user1,
            name='My Wishlist Listing', endTime=date_ended,
            moneyOffer=5.00, notes="Just a test")
        self.expired_listing.items.add(self.global_item1)
        self.expired_listing.save

    #Test to ensure that a user must be logged in to relist a wishlist listings
    def test_redirect_if_not_logged_in(self):
        listing = self.expired_listing
        response = self.client.get(reverse('relist-wishlist-listing', args=[str(listing.id)]))
        self.assertRedirects(response,
            '/accounts/login/?next=/listings/wishlists/wishlist-listings/{0}/relist'.format(listing.id))

    #Test to ensure owner is not redirected if logged in
    def test_no_redirect_if_logged_in_owner(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.expired_listing
        response = self.client.get(reverse('relist-wishlist-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure non owner is redirected if logged in
    def test_redirect_if_logged_in_not_owner(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        listing = self.expired_listing
        response = self.client.get(reverse('relist-wishlist-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure owner is redirected if listing has not yet ended
    def test_redirect_if_logged_in_owner_listing_stll_active(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.active_listing
        response = self.client.get(reverse('relist-wishlist-listing', args=[str(listing.id)]))
        self.assertRedirects(response,
            '/listings/wishlists/{0}'.format(self.global_user1.wishlist.id))

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.expired_listing
        response = self.client.get(reverse('relist-wishlist-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlists/relist_wishlist_listing.html')

    #Test to ensure that a user is able to edit a wishlist listing sucessfully
    def test_wishlist_listing_is_edited_sucessfully(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.expired_listing
        response = self.client.get(reverse('relist-wishlist-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('relist-wishlist-listing', args=[str(listing.id)]),
            data={'name': "My Relisted Wishlist Listing",  'items': [str(self.global_item1.id)],
                'endTimeChoices': '8h', 'moneyOffer': 10.00,
                'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Just a simple update"})
        self.assertEqual(post_response.status_code, 302)
        updated_wishlist_listing = WishlistListing.objects.get(id=listing.id)
        self.assertEqual(updated_wishlist_listing.name, "My Relisted Wishlist Listing")
        self.assertEqual(updated_wishlist_listing.listingEnded, False)
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=8)
        to_tz = timezone.get_default_timezone()
        new_wishlist_listing_endtime = updated_wishlist_listing.endTime
        new_wishlist_listing_endtime = new_wishlist_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_wishlist_listing_endtime.hour, end_time_check.hour)

#Tests for a user to quickly list an item from their wishlist
class QuickWishlistListingViewTest(MyTestCase):
    def setUp(self):
        super(QuickWishlistListingViewTest, self).setUp()

        #Create a user with a wishlist for testing with
        self.user1 = User.objects.create_user(username="mikey", password="example",
            email="exampley@text.com", paypalEmail="exampley@text.com",
            invitesOpen=True, inquiriesOpen=True)
        Wishlist.objects.create(owner=self.user1,
            title="My Small Wishlist",
            description="I would be interested in getting these items in a trade.")

        self.global_user1.profile.latitude = 44.0265
        self.global_user1.profile.longitude = -75.8499
        self.global_user1.profile.save()

    #Test to ensure that a user must be logged in to quickly create wishlist listing
    def test_redirect_if_not_logged_in(self):
        item = self.global_item1
        response = self.client.get(reverse('quick-wishlist-listing', args=[str(item.id)]))
        self.assertRedirects(response,
            ('/accounts/login/?next=/listings/wishlists/wishlist-listings/' +
                '{0}/quick-wishlist-listing'.format(item.id)))

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.global_item1
        response = self.client.get(reverse('quick-wishlist-listing', args=[str(item.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in but have not made a wishlist
    def test_redirect_if_logged_in_no_wishlist(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        item = self.global_item1
        response = self.client.get(reverse('quick-wishlist-listing', args=[str(item.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is redirected if logged and has a wishlist but does
    #not own the item
    def test_redirect_if_logged_in_does_not_own_item(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        item = self.global_item1
        response = self.client.get(reverse('quick-wishlist-listing', args=[str(item.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.global_item1
        response = self.client.get(reverse('quick-wishlist-listing', args=[str(item.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlists/quick_wishlist_listing.html')

    #Test to ensure that a user is able to quick create wishlist listing,
    #have it relate to them, and contains the item quick added
    def test_quick_wishlist_listing_is_created(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.global_item1
        response = self.client.get(reverse('quick-wishlist-listing', args=[str(item.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('quick-wishlist-listing', args=[str(item.id)]),
            data={'name': "My Wishlist Listing", 'endTimeChoices': "1h",
                'moneyOffer': 10.00, 'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Only looking for items that haven't been used."})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist_listing = WishlistListing.objects.last()
        self.assertEqual(new_wishlist_listing.owner, post_response.wsgi_request.user)
        print(new_wishlist_listing.items)
        self.assertTrue(new_wishlist_listing.items.filter(pk=item.id).exists())
        self.assertEqual(str(new_wishlist_listing.latitude), '44.0265')
        self.assertEqual(str(new_wishlist_listing.longitude), '-75.8499')

    #Test to ensure that a user is able to quick create an wishlist listing and have it
    #end in 1 hour if endtime choice is 1h
    def test_quick_wishlist_listing_is_created_correct_1h(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.global_item1
        response = self.client.get(reverse('quick-wishlist-listing', args=[str(item.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('quick-wishlist-listing', args=[str(item.id)]),
            data={'name': "My Wishlist Listing", 'endTimeChoices': "1h",
                'moneyOffer': 10.00, 'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Only looking for items that haven't been used."})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist_listing = WishlistListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=1)
        to_tz = timezone.get_default_timezone()
        new_wishlist_listing_endtime = new_wishlist_listing.endTime
        new_wishlist_listing_endtime = new_wishlist_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_wishlist_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that a user is able to quick create an wishlist listing and have it
    #end in 2 hours if endtime choice is 2h
    def test_quick_wishlist_listing_is_created_correct_2h(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.global_item1
        response = self.client.get(reverse('quick-wishlist-listing', args=[str(item.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('quick-wishlist-listing', args=[str(item.id)]),
            data={'name': "My Wishlist Listing", 'endTimeChoices': "2h",
                'moneyOffer': 10.00, 'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Only looking for items that haven't been used."})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist_listing = WishlistListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=2)
        to_tz = timezone.get_default_timezone()
        new_wishlist_listing_endtime = new_wishlist_listing.endTime
        new_wishlist_listing_endtime = new_wishlist_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_wishlist_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that a user is able to quick create an wishlist listing and have it
    #end in 4 hours if endtime choice is 4h
    def test_quick_wishlist_listing_is_created_correct_4h(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.global_item1
        response = self.client.get(reverse('quick-wishlist-listing', args=[str(item.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('quick-wishlist-listing', args=[str(item.id)]),
            data={'name': "My Wishlist Listing", 'endTimeChoices': "4h",
                'moneyOffer': 10.00, 'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Only looking for items that haven't been used."})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist_listing = WishlistListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=4)
        to_tz = timezone.get_default_timezone()
        new_wishlist_listing_endtime = new_wishlist_listing.endTime
        new_wishlist_listing_endtime = new_wishlist_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_wishlist_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that a user is able to quick create an wishlist listing and have it
    #end in 8 hours if endtime choice is 8h
    def test_quick_wishlist_listing_is_created_correct_8h(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.global_item1
        response = self.client.get(reverse('quick-wishlist-listing', args=[str(item.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('quick-wishlist-listing', args=[str(item.id)]),
            data={'name': "My Wishlist Listing", 'endTimeChoices': "8h",
                'moneyOffer': 10.00, 'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Only looking for items that haven't been used."})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist_listing = WishlistListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=8)
        to_tz = timezone.get_default_timezone()
        new_wishlist_listing_endtime = new_wishlist_listing.endTime
        new_wishlist_listing_endtime = new_wishlist_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_wishlist_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that a user is able to quick create an wishlist listing and have it
    #end in 12 hours if endtime choice is 12h
    def test_quick_wishlist_listing_is_created_correct_12h(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.global_item1
        response = self.client.get(reverse('quick-wishlist-listing', args=[str(item.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('quick-wishlist-listing', args=[str(item.id)]),
            data={'name': "My Wishlist Listing", 'endTimeChoices': "12h",
                'moneyOffer': 10.00, 'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Only looking for items that haven't been used."})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist_listing = WishlistListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(hours=12)
        to_tz = timezone.get_default_timezone()
        new_wishlist_listing_endtime = new_wishlist_listing.endTime
        new_wishlist_listing_endtime = new_wishlist_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_wishlist_listing_endtime.hour, end_time_check.hour)

    #Test to ensure that a user is able to quick create an wishlist listing and have it
    #end in 1 day if endtime choice is 1d
    def test_quick_wishlist_listing_is_created_correct_1d(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.global_item1
        response = self.client.get(reverse('quick-wishlist-listing', args=[str(item.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('quick-wishlist-listing', args=[str(item.id)]),
            data={'name': "My Wishlist Listing", 'endTimeChoices': "1d",
                'moneyOffer': 10.00, 'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Only looking for items that haven't been used."})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist_listing = WishlistListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(days=1)
        to_tz = timezone.get_default_timezone()
        new_wishlist_listing_endtime = new_wishlist_listing.endTime
        new_wishlist_listing_endtime = new_wishlist_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_wishlist_listing_endtime.day, end_time_check.day)

    #Test to ensure that a user is able to quick create an wishlist listing and have it
    #end in 3 days if endtime choice is 3d
    def test_quick_wishlist_listing_is_created_correct_3d(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.global_item1
        response = self.client.get(reverse('quick-wishlist-listing', args=[str(item.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('quick-wishlist-listing', args=[str(item.id)]),
            data={'name': "My Wishlist Listing", 'endTimeChoices': "3d",
                'moneyOffer': 10.00, 'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Only looking for items that haven't been used."})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist_listing = WishlistListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(days=3)
        to_tz = timezone.get_default_timezone()
        new_wishlist_listing_endtime = new_wishlist_listing.endTime
        new_wishlist_listing_endtime = new_wishlist_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_wishlist_listing_endtime.day, end_time_check.day)

    #Test to ensure that a user is able to quick create an wishlist listing and have it
    #end in 7 days if endtime choice is 7d
    def test_quick_wishlist_listing_is_created_correct_7d(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.global_item1
        response = self.client.get(reverse('quick-wishlist-listing', args=[str(item.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('quick-wishlist-listing', args=[str(item.id)]),
            data={'name': "My Wishlist Listing", 'endTimeChoices': "7d",
                'moneyOffer': 10.00, 'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Only looking for items that haven't been used."})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist_listing = WishlistListing.objects.last()
        end_time_check = timezone.localtime(timezone.now()) + timedelta(days=7)
        to_tz = timezone.get_default_timezone()
        new_wishlist_listing_endtime = new_wishlist_listing.endTime
        new_wishlist_listing_endtime = new_wishlist_listing_endtime.astimezone(to_tz)
        self.assertEqual(new_wishlist_listing_endtime.day, end_time_check.day)

    #Test to ensure that a user is able to quick create an wishlist listing and
    #if moneyOffer is left blank, it becomes $0.00
    def test_quick_wishlist_listing_is_created_no_money_offer(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.global_item1
        response = self.client.get(reverse('quick-wishlist-listing', args=[str(item.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('quick-wishlist-listing', args=[str(item.id)]),
            data={'name': "My Wishlist Listing", 'endTimeChoices': "1h",
                'itemsOffer': [str(self.global_non_wishlist_item.id)],
                'notes': "Only looking for items that haven't been used."})
        self.assertEqual(post_response.status_code, 302)
        new_wishlist_listing = WishlistListing.objects.last()
        self.assertEqual(new_wishlist_listing.moneyOffer, 0.00)

#Tests for a user to delete a wihslist listing they own
class WishlistListingDeleteViewTest(MyTestCase):
    def setUp(self):
        super(WishlistListingDeleteViewTest, self).setUp()
        #Get the current date and time for testing and create active and
        #inactive endTimes
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)
        date_ended = timezone.localtime(timezone.now()) - timedelta(days=1)

        #Create active and inactive wishlist listing objects to test for deletion
        self.active_listing = WishlistListing.objects.create(owner=self.global_user1,
            name='My Wishlist Listing', endTime=date_active,
            moneyOffer=5.00, notes="Just a test")
        self.active_listing.items.add(self.global_item1)
        self.active_listing.save

        self.expired_listing = WishlistListing.objects.create(owner=self.global_user1,
            name='My Wishlist Listing', endTime=date_ended,
            moneyOffer=5.00, notes="Just a test")
        self.expired_listing.items.add(self.global_item1)
        self.expired_listing.save

    #Test to ensure that a user must be logged in to delete a wishlist listing
    def test_redirect_if_not_logged_in(self):
        listing = self.active_listing
        response = self.client.get(reverse('delete-wishlist-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in if they own the listing
    def test_no_redirect_if_logged_in_owner(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.active_listing
        response = self.client.get(reverse('delete-wishlist-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged but they do not own the listing
    def test_no_redirect_if_logged_in_not_owner(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        listing = self.active_listing
        response = self.client.get(reverse('delete-wishlist-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.active_listing
        response = self.client.get(reverse('delete-wishlist-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlists/wishlist_listing_delete.html')

    #Test to ensure an active listing can be deleted if user confirms
    def test_succesful_deletion_active_listing(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.active_listing
        listing_id = listing.id
        post_response = self.client.post(reverse('delete-wishlist-listing', args=[str(listing.id)]))
        self.assertRedirects(post_response, reverse('wishlist-listings'))
        self.assertFalse(WishlistListing.objects.filter(id=listing_id).exists())

    #Test to ensure an inactive listing can be deleted if user confirms
    def test_succesful_deletion_inactive_listing(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.expired_listing
        listing_id = listing.id
        post_response = self.client.post(reverse('delete-wishlist-listing', args=[str(listing.id)]))
        self.assertRedirects(post_response, reverse('wishlist-listings'))
        self.assertFalse(WishlistListing.objects.filter(id=listing_id).exists())

#Tests for a user to quickly add another user owned item to their wishlist
class QuickAddItemToWishlistViewTest(MyTestCase):
    def setUp(self):
        super(QuickAddItemToWishlistViewTest, self).setUp()

        #Create an item for testing with
        self.owned_item = Item.objects.create(name="Owned Item",
            description="An item for testing", owner=self.global_user1)
        self.owned_item.images.add(self.global_image1)
        self.owned_item.save

        self.unowned_item = self.global_item2

    #Test to ensure that a user must be logged in to quickly add item to wishlist
    def test_redirect_if_not_logged_in(self):
        item = self.owned_item
        response = self.client.get(reverse('quick-add-item-to-wishlist',
            args=[str(item.id)]))
        self.assertRedirects(response,
            '/accounts/login/?next=/listings/wishlists/{0}/quick-add'.format(item.id))

    #Test to ensure user is redirected to wishlist if logged in and item was
    #added succesfully
    def test_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.owned_item
        response = self.client.get(reverse('quick-add-item-to-wishlist',
            args=[str(item.id)]))
        self.assertRedirects(response,
            '/listings/wishlists/{0}'.format(self.global_user1.wishlist.id))

    #Test to ensure user is redirected if logged in but they dont have wishlist
    def test_redirect_if_logged_in_no_wishlist(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        item = self.owned_item
        response = self.client.get(reverse('quick-add-item-to-wishlist',
            args=[str(item.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure that the user can add an item they own succesfully to wishlist
    def test_owned_item_is_added_successfully(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.owned_item
        post_response = self.client.post(reverse('quick-add-item-to-wishlist',
            args=[str(item.id)]))
        self.assertEqual(post_response.status_code, 302)
        wishlist = Wishlist.objects.get(id=self.global_user1.wishlist.id)
        self.assertTrue(wishlist.items.filter(pk=item.id).exists())

    #Test to ensure that the user can add an item they do not own
    #succesfully to wishlist
    def test_unowned_item_is_added_successfully(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        item = self.owned_item
        post_response = self.client.post(reverse('quick-add-item-to-wishlist',
            args=[str(item.id)]))
        self.assertEqual(post_response.status_code, 302)
        wishlist = Wishlist.objects.get(id=self.global_user1.wishlist.id)
        new_item = Item.objects.last()
        self.assertTrue(wishlist.items.filter(pk=new_item.id).exists())
        self.assertTrue(self.global_user1.items.filter(pk=new_item.id).exists())

#Tests for a user to view a profile's details
class ProfileDetailViewTest(MyTestCase):
    def setUp(self):
        super(ProfileDetailViewTest, self).setUp()

        #Set the locations of the global users
        self.global_user1.profile.latitude = 40.0000
        self.global_user1.profile.longitude = -75.0000
        self.global_user1.profile.save()

        self.global_user2.profile.latitude = 40.5000
        self.global_user2.profile.longitude = -75.5000
        self.global_user2.profile.save()

        #Create an additional user for testing with
        self.new_user = User.objects.create_user(username="mike4",
            password="example", email="example5@text.com",
            paypalEmail="example5@text.com", invitesOpen=True,
            inquiriesOpen=True)

        self.new_user.profile.latitude = 41.0000
        self.new_user.profile.longitude = -76.000
        self.new_user.profile.save()

        #Set number of listings for each user
        #Must account for the global listings
        number_of_offer_listings = 2
        number_of_auction_listings = 3
        number_of_wishlist_listings = 5

        #Get the current date and time for testing and create active
        #and inactive endTimes
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)
        date_ended = timezone.localtime(timezone.now()) - timedelta(days=1)

        #Create the offer listings
        for num in range(number_of_offer_listings):
            listing = OfferListing.objects.create(owner=self.global_user1,
                name='Test Offer Listing #{0}'.format(num),
                description="Just a test listing", openToMoneyOffers=True,
                minRange=5.00, maxRange=10.00, notes="Just offer",
                endTime=date_active)
            listing.items.add(self.global_item1)
            listing.save

        #Create an inactive offer listing
        OfferListing.objects.create(owner=self.global_user1,
            name='Test Offer Listing #{0}'.format(num),
            description="Just a test listing", openToMoneyOffers=True,
            minRange=5.00, maxRange=10.00, notes="Just offer",
            endTime=date_ended)

        #Create the auction listings
        for num in range(number_of_auction_listings):
            listing = AuctionListing.objects.create(owner=self.global_user1,
                name="Test Auction", description="Just a test auction",
                startingBid=5.00, minimumIncrement=2.50, autobuy=50.00,
                endTime=date_active)
            listing.items.add(self.global_item1)
            listing.save

        #Create an inactive auction listing
        AuctionListing.objects.create(owner=self.global_user1,
            name="Test Auction", description="Just a test auction",
            startingBid=5.00, minimumIncrement=2.50, autobuy=50.00,
            endTime=date_ended)

        #Create the wishlist listings
        for num in range(number_of_wishlist_listings):
            listing = WishlistListing.objects.create(owner=self.global_user1,
                name='My Wishlist Listing #{0}'.format(num), endTime=date_active,
                moneyOffer=5.00, notes="Just a test")
            listing.items.add(self.global_item1)
            listing.itemsOffer.add(self.global_item1)
            listing.save

        #create an inactive wishlist listing
        WishlistListing.objects.create(owner=self.global_user1,
            name='My Wishlist Listing', endTime=date_ended,
            moneyOffer=5.00, notes="Just a test")

        #Create some ratings
        for num in range(12):
            Rating.objects.create(profile=self.global_user1.profile,
                reviewer=self.global_user2, ratingValue=3,
                feedback=("User was good on getting me the items on time" +
                " but did not communicate with me well."),
                listingName=self.global_offer_listing2.name)

        #Create a rating ticket to use
        self.ticket = RatingTicket.objects.create(rater=self.global_user2,
            receivingUser=self.global_user1, listing=self.global_offer_listing2)
        self.ticket_id = self.ticket.id

    #Test to ensure that a user must be logged in to view a profile
    def test_redirect_if_not_logged_in(self):
        profile = self.global_user1.profile
        response = self.client.get(reverse('profile-detail', args=[str(profile.id)]))
        self.assertRedirects(response, '/accounts/login/?next=/listings/profile/{0}'.format(profile.id))

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        profile = self.global_user1.profile
        response = self.client.get(reverse('profile-detail', args=[str(profile.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        profile = self.global_user1.profile
        response = self.client.get(reverse('profile-detail', args=[str(profile.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile_detail.html')

    #Test that a user can see the user that owns the profile's listings if they
    #are in a location at most 50m aways
    def test_user_can_see_listings_nearby_user(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        profile = self.global_user1.profile
        response = self.client.get(reverse('profile-detail', args=[str(profile.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['offer_listings']) == 3)
        self.assertTrue(len(response.context['auction_listings']) == 4)
        self.assertTrue(len(response.context['wishlist_listings']) == 5)

    #Test that a user can not see the user that owns the profile's listings if they
    #are in a location further than 50m aways
    def test_user_can_not_see_listings_non_nearby_user(self):
        login = self.client.login(username='mike4', password='example')
        self.assertTrue(login)
        profile = self.global_user1.profile
        response = self.client.get(reverse('profile-detail', args=[str(profile.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['offer_listings']) == 0)
        self.assertTrue(len(response.context['auction_listings']) == 0)
        self.assertTrue(len(response.context['wishlist_listings']) == 0)

    #Test that a user can see the user that owns the profile's ratings on page 1
    def test_user_can_see_ratings_pg1(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        profile = self.global_user1.profile
        response = self.client.get(reverse('profile-detail', args=[str(profile.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['ratings']) == 10)

    #Test that a user can see the user that owns the profile's ratings on page 2
    def test_user_can_see_ratings_pg2(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        profile = self.global_user1.profile
        response = self.client.get(reverse('profile-detail', args=[str(profile.id)])+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['ratings']) == 2)

    #Test to ensure that a user can create a rating succesfully and that the
    #rating ticket used was deleted
    def test_rating_is_created(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        profile = self.global_user1.profile
        response = self.client.get(reverse('profile-detail', args=[str(profile.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('profile-detail', args=[str(profile.id)]),
            data={
                'ratingValue': 5,
                'feedback': "User was very kind and delivered my items on time.",
                'ratingTicket': str(self.ticket.id)
            })
        self.assertEqual(post_response.status_code, 302)
        new_rating = Rating.objects.last()
        self.assertEqual(new_rating.ratingValue, 5)
        self.assertEqual(new_rating.feedback,
            "User was very kind and delivered my items on time.")
        self.assertEqual(new_rating.reviewer, self.global_user2)
        self.assertEqual(new_rating.listingName, self.global_offer_listing2.name)
        self.assertFalse(RatingTicket.objects.filter(id=self.ticket_id).exists())

    #Test that a notification is created after rating is made
    def test_notification_created(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        profile = self.global_user1.profile
        response = self.client.get(reverse('profile-detail', args=[str(profile.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('profile-detail', args=[str(profile.id)]),
            data={
                'ratingValue': 5,
                'feedback': "User was very kind and delivered my items on time.",
                'ratingTicket': str(self.ticket.id)
            })
        self.assertEqual(post_response.status_code, 302)
        notification = RatingNotification.objects.last()
        content = self.global_user2.username + " has left a rating on your profile."
        self.assertEqual(notification.profile, profile)
        self.assertEqual(notification.user, profile.user)
        self.assertEqual(notification.rater, self.global_user2)
        self.assertEqual(notification.type, "Feedback Left")
        self.assertEqual(notification.content, content)

#Tests for a user to edit their profile
class EditProfileViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to edit profile
    def test_redirect_if_not_logged_in(self):
        profile = self.global_user1.profile
        response = self.client.get(reverse('edit-profile', args=[str(profile.id)]))
        self.assertRedirects(response,
            '/accounts/login/?next=/listings/profile/{0}/edit'.format(profile.id))

    #Test to ensure user is not redirected if logged in and is the user
    #of the profile
    def test_no_redirect_if_logged_in_profile_user(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        profile = self.global_user1.profile
        response = self.client.get(reverse('edit-profile', args=[str(profile.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in but is not the profile user
    def test_redirect_if_logged_in_not_profile_user(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        profile = self.global_user1.profile
        response = self.client.get(reverse('edit-profile', args=[str(profile.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        profile = self.global_user1.profile
        response = self.client.get(reverse('edit-profile', args=[str(profile.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/edit_profile.html')

    #Test to ensure that a user is able to edit their profile successfully
    def test_profile_is_updated(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        profile = self.global_user1.profile
        response = self.client.get(reverse('edit-profile', args=[str(profile.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('edit-profile', args=[str(profile.id)]),
            data={'bio': "My Updated Profile", 'delivery': True,
                'deliveryAddress': "SUNY Potsdam"})
        self.assertEqual(post_response.status_code, 302)
        edited_profile = Profile.objects.get(id=profile.id)
        self.assertEqual(edited_profile.bio, 'My Updated Profile')
        self.assertEqual(edited_profile.deliveryAddress, 'SUNY Potsdam')

#Tests for a user to view a list of users on the site
class UsersViewTest(MyTestCase):
    def setUp(self):
        super(UsersViewTest, self).setUp()

        #Create a variety of users to test with
        #Number of users should be 9 as there are 2 global users
        number_of_users = 7

        for num in range(number_of_users):
            User.objects.create_user(username='mike#{0}'.format(num), password="example",
                email="example#{0}@text.com".format(num),
                paypalEmail="example#{0}@text.com".format(num),
                invitesOpen=True, inquiriesOpen=True)

    #Test to ensure that a user must be logged in to view listings
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('users'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/users/')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/users.html')

    #Test to ensure that a user sees the correct amount of users on site
    def test_list_users_page_1(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['users']), 9)

    #Test to ensure that different user sees the correct amount of active listings
    def test_list_users_new_user_page_1(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['users']), 9)

#Tests for a user to edit their account details
class EditAccountViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to edit account
    def test_redirect_if_not_logged_in(self):
        user = self.global_user1
        response = self.client.get(reverse('edit-account', args=[str(user.id)]))
        self.assertRedirects(response,
            '/accounts/login/?next=/listings/users/{0}/edit'.format(user.id))

    #Test to ensure user is not redirected if logged in and is correct user
    #for the account
    def test_no_redirect_if_logged_in_correct_user(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        user = self.global_user1
        response = self.client.get(reverse('edit-account', args=[str(user.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in but is not the correct user
    def test_redirect_if_logged_in_not_correct_user(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        user = self.global_user1
        response = self.client.get(reverse('edit-account', args=[str(user.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        user = self.global_user1
        response = self.client.get(reverse('edit-account', args=[str(user.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/edit_account.html')

    #Test to ensure that a user is able to edit their account successfully
    def test_account_is_updated(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        user = self.global_user1
        response = self.client.get(reverse('edit-account', args=[str(user.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('edit-account', args=[str(user.id)]),
            data={'paypalEmail': "paypalexample4@text.com", 'first_name': "Michael",
                'last_name': "Lopez", 'invitesOpen': True, 'inquiriesOpen': False})
        self.assertEqual(post_response.status_code, 302)
        edited_user = User.objects.get(id=user.id)
        self.assertEqual(edited_user.paypalEmail, 'paypalexample4@text.com')
        self.assertEqual(edited_user.first_name, 'Michael')
        self.assertEqual(edited_user.last_name, 'Lopez')

#Tests for a user to view a list of conversations they're in
class ConversationsViewTest(MyTestCase):
    def setUp(self):
        super(ConversationsViewTest, self).setUp()

        #Create a new user for testing with
        self.user1 = User.objects.create_user(username="mikey", password="example",
            email="exampley@text.com", paypalEmail="exampley@text.com",
            invitesOpen=True, inquiriesOpen=True)

        #Set number of conversations between users
        number_of_conversations_user1_user2 = 3
        number_of_conversations_user1_user3 = 2

        for num in range(number_of_conversations_user1_user2):
            conversation = Conversation.objects.create(sender=self.global_user1,
                recipient=self.global_user2, topic="For a test")
            Message.objects.create(content="Hello",
                author=self.global_user1,
                dateSent=timezone.localtime(timezone.now()), unread=True,
                conversation=conversation)

        for num in range(number_of_conversations_user1_user3):
            conversation = Conversation.objects.create(sender=self.global_user1,
                recipient=self.user1, topic="For a test")
            Message.objects.create(content="Hello",
                author=self.global_user1,
                dateSent=timezone.localtime(timezone.now()), unread=True,
                conversation=conversation)

    #Test to ensure that a user must be logged in to view conversations
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('conversations'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/conversations/')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('conversations'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('conversations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conversations/conversations.html')

    #Test to ensure that the user 1 only sees conversations they are a sender
    #or recipient for
    def test_list_only_conversations_related_to_user1(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('conversations'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['conversations']) == 5)

    #Test to ensure that the user 2 only sees conversations they are a sender
    #or recipient for
    def test_list_only_conversations_related_to_user2(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('conversations'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['conversations']) == 3)

    #Test to ensure that the user 3 only sees conversations they are a sender
    #or recipient for
    def test_list_only_conversations_related_to_user3(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('conversations'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['conversations']) == 2)

#Tests for a user to start a conversation with another user
class StartConversationViewTest(MyTestCase):
    def setUp(self):
        super(StartConversationViewTest, self).setUp()

        #create a user that is not open to messages
        self.no_messages_user = User.objects.create_user(username="mikey", password="example",
            email="example5@text.com", paypalEmail="example5@text.com",
            invitesOpen=True, inquiriesOpen=False)

    #Test to ensure that a user must be logged in to start a conversation
    def test_redirect_if_not_logged_in(self):
        recipient = self.global_user2
        response = self.client.get(reverse('start-conversation',
            args=[str(recipient.id)]))
        self.assertRedirects(response,
            ('/accounts/login/?next=/listings/conversations/' +
                '{0}/start-conversation'.format(recipient.id)))

    #Test to ensure user is not redirected if logged in and is starting a
    #conversation with a different user
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        recipient = self.global_user2
        response = self.client.get(reverse('start-conversation',
            args=[str(recipient.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in but is trying to start
    #a conversation with themselves
    def test_redirect_if_logged_in_no_conversation_with_self(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        recipient = self.global_user1
        response = self.client.get(reverse('start-conversation',
            args=[str(recipient.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is redirected if logged in but is trying to start
    #a conversation with a user not open to messages
    def test_redirect_if_logged_in_recipient_not_open_to_messages(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        recipient = self.no_messages_user
        response = self.client.get(reverse('start-conversation',
            args=[str(recipient.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        recipient = self.global_user2
        response = self.client.get(reverse('start-conversation',
            args=[str(recipient.id)]))
        self.assertTemplateUsed(response, 'conversations/start_conversation.html')

    #Test to ensure that a user is able to start a conversation and have it
    #relate to them and the recipient, as well as message being created
    def test_conversation_is_started(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        recipient = self.global_user2
        response = self.client.get(reverse('start-conversation',
            args=[str(recipient.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('start-conversation',
            args=[str(recipient.id)]), data={'topic': "I want your item",
                'message': "Sell me your item now."})
        self.assertEqual(post_response.status_code, 302)
        new_conversation = Conversation.objects.last()
        self.assertEqual(new_conversation.sender, post_response.wsgi_request.user)
        self.assertEqual(new_conversation.recipient, self.global_user2)
        new_message = Message.objects.last()
        self.assertEqual(new_message.author, post_response.wsgi_request.user)
        self.assertEqual(new_message.conversation, new_conversation)

#Tests for a user to view a conversation
class ConversationDetailViewTest(MyTestCase):
    def setUp(self):
        super(ConversationDetailViewTest, self).setUp()

        #Create a new user for testing with
        self.user1 = User.objects.create_user(username="mikey", password="example",
            email="exampley@text.com", paypalEmail="exampley@text.com",
            invitesOpen=True, inquiriesOpen=True)

        #Create a conversation for testing with
        self.conversation = Conversation.objects.create(sender=self.global_user1,
            recipient=self.global_user2, topic="For a test")
        self.inactive_conversation = Conversation.objects.create(sender=self.global_user1,
            topic="For a test")

        #create a message for testing with
        self.unread_message = Message.objects.create(content="Hello",
            author=self.global_user1,
            dateSent=timezone.localtime(timezone.now()), unread=True,
            conversation=self.conversation)

    #Test to ensure that a user must be logged in to view a conversation
    def test_redirect_if_not_logged_in(self):
        conversation = self.conversation
        response = self.client.get(reverse('conversation-detail',
            args=[str(conversation.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in and is sender of
    #conversation
    def test_no_redirect_if_logged_in_sender(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        conversation = self.conversation
        response = self.client.get(reverse('conversation-detail',
            args=[str(conversation.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is not redirected if logged in and is recipient of
    #conversation
    def test_no_redirect_if_logged_in_recipient(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        conversation = self.conversation
        response = self.client.get(reverse('conversation-detail',
            args=[str(conversation.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in but is not recipient or
    #sender of conversation
    def test_redirect_if_logged_in_not_sender_or_recipient(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        conversation = self.conversation
        response = self.client.get(reverse('conversation-detail',
            args=[str(conversation.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        conversation = self.conversation
        response = self.client.get(reverse('conversation-detail',
            args=[str(conversation.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conversations/conversation_detail.html')

    #Test to ensure that unread messages remain unread if author views
    #conversation
    def test_messages_remain_unread_for_author(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        conversation = self.conversation
        response = self.client.get(reverse('conversation-detail',
            args=[str(conversation.id)]))
        self.assertEqual(response.status_code, 200)
        message = Message.objects.get(id=self.unread_message.id)
        self.assertEqual(message.unread, True)

    #Test to ensure that unread messages become read if non author views
    #conversation
    def test_messages_become_read_for_non_author(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        conversation = self.conversation
        response = self.client.get(reverse('conversation-detail',
            args=[str(conversation.id)]))
        self.assertEqual(response.status_code, 200)
        message = Message.objects.get(id=self.unread_message.id)
        self.assertEqual(message.unread, False)

    #Test to ensure that a user can create a message succesfully
    def test_message_is_created(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        conversation = self.conversation
        response = self.client.get(reverse('conversation-detail',
            args=[str(conversation.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('conversation-detail',
            args=[str(conversation.id)]),
            data={
                'content': "I hope this message reaches you."
            })
        self.assertEqual(post_response.status_code, 302)
        new_message = Message.objects.last()
        self.assertEqual(new_message.author, post_response.wsgi_request.user)
        self.assertEqual(new_message.conversation, conversation)
        self.assertEqual(new_message.content, "I hope this message reaches you.")
        self.assertEqual(new_message.unread, True)

    #Test to ensure that a user can not create a message if the other user
    #is no longer part of the conversation
    def test_message_is_not_created_other_user_no_longer_in_conversation(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        conversation = self.inactive_conversation
        response = self.client.get(reverse('conversation-detail',
            args=[str(conversation.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('conversation-detail',
            args=[str(conversation.id)]),
            data={
                'content': "I hope this message reaches you."
            })
        self.assertEqual(post_response.status_code, 404)

#Tests for a user to remove themselves from or delete a conversation
class ConversationDeleteViewTest(MyTestCase):
    def setUp(self):
        super(ConversationDeleteViewTest, self).setUp()
        #Create a new user for testing with
        self.user = User.objects.create_user(username="mikey", password="example",
            email="exampley@text.com", paypalEmail="exampley@text.com",
            invitesOpen=True, inquiriesOpen=True)

        #Create an conversation to test for deletion
        self.conversation = Conversation.objects.create(sender=self.global_user1,
            recipient=self.global_user2, topic="For a test")
        self.inactive_conversation = Conversation.objects.create(sender=self.global_user1,
            recipient=None, topic="For a test")
        self.conversation_id = self.conversation.id
        self.inactive_conversation_id = self.inactive_conversation.id

        #create some messages for the conversations
        number_of_messages_conversation_1 = 3
        number_of_messages_conversation_2 = 5

        self.active_message_ids = [0 for number in range(number_of_messages_conversation_1)]
        self.inactive_message_ids = [0 for number in range(number_of_messages_conversation_2)]

        #Messages for the active conversation
        for num in range(number_of_messages_conversation_1):
            message = Message.objects.create(content="Hello",
                author=self.global_user1,
                dateSent=timezone.localtime(timezone.now()), unread=True,
                conversation=self.conversation)
            self.active_message_ids[num] = message.id

        #Messages for the inactive conversation
        for num in range(number_of_messages_conversation_2):
            message = Message.objects.create(content="Hello",
                author=self.global_user1,
                dateSent=timezone.localtime(timezone.now()), unread=True,
                conversation=self.inactive_conversation)
            self.inactive_message_ids[num] = message.id

    #Test to ensure that a user must be logged in to delete a conversation
    def test_redirect_if_not_logged_in(self):
        conversation = self.conversation
        response = self.client.get(reverse('delete-conversation',
            args=[str(conversation.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in if the are the sender
    def test_no_redirect_if_logged_in_sender(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        conversation = self.conversation
        response = self.client.get(reverse('delete-conversation',
            args=[str(conversation.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is not redirected if logged in if the are the recipient
    def test_no_redirect_if_logged_in_recipient(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        conversation = self.conversation
        response = self.client.get(reverse('delete-conversation',
            args=[str(conversation.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged but they are not sender
    #or recipient
    def test_no_redirect_if_logged_in_not_sender_or_recipient(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        conversation = self.conversation
        response = self.client.get(reverse('delete-conversation',
            args=[str(conversation.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        conversation = self.conversation
        response = self.client.get(reverse('delete-conversation',
            args=[str(conversation.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conversations/conversation_delete.html')

    #Test to ensure conversation is not deleted if one user removes themselves
    #from conversation but other user hasn't yet
    def test_successful_removal_of_user(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        conversation = self.conversation
        post_response = self.client.post(reverse('delete-conversation',
            args=[str(conversation.id)]))
        self.assertRedirects(post_response, reverse('conversations'))
        self.assertTrue(Conversation.objects.filter(id=self.conversation_id).exists())
        for message_id in self.active_message_ids:
            self.assertTrue(Message.objects.filter(id=message_id).exists())

    #Test to ensure conversation is deleted if the last user removes themselves
    #from the conversation
    def test_successful_deletion(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        conversation = self.inactive_conversation
        post_response = self.client.post(reverse('delete-conversation',
            args=[str(conversation.id)]))
        self.assertRedirects(post_response, reverse('conversations'))
        self.assertFalse(Conversation.objects.filter(id=self.inactive_conversation_id).exists())
        for message_id in self.inactive_message_ids:
            self.assertFalse(Message.objects.filter(id=message_id).exists())

#Tests for a user to view their receipts
class ReceiptListViewTest(MyTestCase):
    def setUp(self):
        super(ReceiptListViewTest, self).setUp()

        #Create users for testing with
        self.user1 = User.objects.create_user(username="mikey", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)
        self.user2 = User.objects.create_user(username="mikea", password="example",
            email="example5@text.com", paypalEmail="example5@text.com",
            invitesOpen=True, inquiriesOpen=True)

        #Global user 2 should have 15 receipts, 14 from here and 1 global
        #completed listing
        self.number_of_receipts_user1 = 6
        self.number_of_receipts_user2 = 8

        #Get the current date and time for testing and create active and inactive endtimes
        date_ended = timezone.localtime(timezone.now()) - timedelta(hours=1)
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        #Create the receipts for the 1st user
        for num in range(self.number_of_receipts_user1):
            remainder = num % 2
            if remainder == 0:
                listing = OfferListing.objects.create(owner=self.global_user1,
                    name='Test Offer Listing', description="Just a test listing",
                    openToMoneyOffers=True, minRange=5.00, maxRange=10.00,
                    notes="Just offer", endTime=date_ended, listingCompleted=True)
                Offer.objects.create(offerListing=listing, owner=self.user1,
                    amount=5.00, offerAccepted=True)
                receipt = Receipt.objects.get(listing=listing)
                receipt.owner = self.global_user1
                receipt.exchangee = self.user1
                receipt.save()
            else:
                listing = AuctionListing.objects.create(owner=self.global_user1,
                    name='Test Auction Listing', description="Just a test listing",
                    startingBid=5.00, minimumIncrement=1.00, autobuy=25.00,
                    endTime=date_ended)
                Bid.objects.create(auctionListing=listing, bidder=self.user1,
                    amount=5.00, winningBid=True)
                receipt = Receipt.objects.get(listing=listing)
                receipt.owner = self.global_user1
                receipt.exchangee = self.user1
                receipt.save()

        #Create the receipts for the 2nd user
        for num in range(self.number_of_receipts_user2):
            remainder = num % 2
            if remainder == 0:
                listing = OfferListing.objects.create(owner=self.global_user1,
                    name='Test Offer Listing', description="Just a test listing",
                    openToMoneyOffers=True, minRange=5.00, maxRange=10.00,
                    notes="Just offer", endTime=date_ended, listingCompleted=True)
                Offer.objects.create(offerListing=listing, owner=self.global_user2,
                    amount=5.00, offerAccepted=True)
                receipt = Receipt.objects.get(listing=listing)
                receipt.owner = self.global_user1
                receipt.exchangee = self.global_user2
                receipt.save()
            else:
                listing = AuctionListing.objects.create(owner=self.global_user1,
                    name='Test Auction Listing', description="Just a test listing",
                    startingBid=5.00, minimumIncrement=1.00, autobuy=25.00,
                    endTime=date_ended)
                Bid.objects.create(auctionListing=listing, bidder=self.global_user2,
                    amount=5.00, winningBid=True)
                receipt = Receipt.objects.get(listing=listing)
                receipt.owner = self.global_user1
                receipt.exchangee = self.global_user2
                receipt.save()

        #Create some active listings for testing
        listing = OfferListing.objects.create(owner=self.global_user1,
            name='Test Offer Listing', description="Just a test listing",
            openToMoneyOffers=True, minRange=5.00, maxRange=10.00,
            notes="Just offer", endTime=date_active, listingCompleted=False)
        Offer.objects.create(offerListing=listing, owner=self.global_user2,
            amount=5.00, offerAccepted=False)
        receipt = Receipt.objects.get(listing=listing)
        receipt.owner = self.global_user1
        receipt.exchangee = self.global_user2
        receipt.save()

        listing = AuctionListing.objects.create(owner=self.global_user1,
            name='Test Auction Listing', description="Just a test listing",
            startingBid=5.00, minimumIncrement=1.00, autobuy=25.00,
            endTime=date_active)
        Bid.objects.create(auctionListing=listing, bidder=self.user1,
            amount=5.00, winningBid=True)
        receipt = Receipt.objects.get(listing=listing)
        receipt.owner = self.global_user1
        receipt.exchangee = self.user1
        receipt.save()

        receipt = Receipt.objects.get(listing=self.global_offer_listing3)
        receipt.owner = self.global_user1
        receipt.exchangee = self.global_user2
        receipt.save()

    #Test to ensure that a user must be logged in to view receipts
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('receipts'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/receipts/')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('receipts'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('receipts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'receipts/receipts.html')

    #Test to ensure that the user only sees receipts related to them for
    # completed listings for user1
    def test_list_only_receipts_for_completed_listings_user1(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('receipts'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['receipts']), 6)

    #Test to ensure that the user only sees receipts related to them for
    # completed listings for user2
    def test_list_only_receipts_for_completed_listings_user2(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('receipts'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['receipts']), 8)

    #Test to ensure that the user only sees receipts related to them for
    # completed listings for user3 on page 1
    def test_list_only_receipts_for_completed_listings_user3_page_1(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('receipts'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['receipts']), 10)

    #Test to ensure that the user only sees receipts related to them for
    # completed listings for user3 on page 2
    def test_list_only_receipts_for_completed_listings_user3_page_2(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('receipts')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['receipts']), 5)

    #Test to ensure that the user only sees receipts related to them for
    # completed listings for user4
    def test_list_only_receipts_for_completed_listings_user4(self):
        login = self.client.login(username='mikea', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('receipts'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['receipts']), 0)

#Tests for a user to make a payment to another user
class MakePaypalPaymentViewTest(MyTestCase):
    def setUp(self):
        super(MakePaypalPaymentViewTest, self).setUp()

        #Create users for testing with
        self.user1 = User.objects.create_user(username="mikey", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)
        self.user2 = User.objects.create_user(username="mikea", password="example",
            email="example5@text.com", paypalEmail="example5@text.com",
            invitesOpen=True, inquiriesOpen=True)

        #Get the current date and time for testing and create active and inactive endtimes
        date_ended = timezone.localtime(timezone.now()) - timedelta(hours=1)
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        #Create completed offer listings
        self.completed_offer_listing = OfferListing.objects.create(owner=self.global_user1,
            name='Test Offer Listing', description="Just a test listing",
            openToMoneyOffers=True, minRange=5.00, maxRange=10.00,
            notes="Just offer", endTime=date_ended, listingCompleted=True)
        self.completed_offer_listing_2 = OfferListing.objects.create(owner=self.global_user1,
            name='Test Offer Listing', description="Just a test listing",
            openToMoneyOffers=True, minRange=5.00, maxRange=10.00,
            notes="Just offer", endTime=date_ended, listingCompleted=True)

        #Create active and completed auction listings
        self.active_auction_listing = AuctionListing.objects.create(owner=self.global_user1,
            name='Test Auction Listing', description="Just a test listing",
            startingBid=5.00, minimumIncrement=1.00, autobuy=25.00,
            endTime=date_active)
        self.completed_auction_listing = AuctionListing.objects.create(owner=self.global_user1,
            name='Test Auction Listing', description="Just a test listing",
            startingBid=5.00, minimumIncrement=1.00, autobuy=25.00,
            endTime=date_ended)

        #Create objects related to listings
        self.accepted_offer = Offer.objects.create(offerListing=self.completed_offer_listing,
            owner=self.global_user2, amount=5.00, offerAccepted=True)
        self.accepted_offer_2 = Offer.objects.create(offerListing=self.completed_offer_listing_2,
            owner=self.global_user2, amount=0.00, offerAccepted=True)
        self.winning_final_bid = Bid.objects.create(auctionListing=self.completed_auction_listing,
            bidder=self.global_user2, amount=5.00, winningBid=True)
        self.winning_non_final_bid = Bid.objects.create(auctionListing=self.active_auction_listing,
            bidder=self.global_user2, amount=5.00, winningBid=True)

        #Update the related receipts
        self.completed_offer_listing_receipt = Receipt.objects.get(
            listing=self.completed_offer_listing)
        self.completed_offer_listing_receipt.owner = self.global_user1
        self.completed_offer_listing_receipt.exchangee = self.global_user2
        self.completed_offer_listing_receipt.save()

        self.completed_offer_listing_receipt_2 = Receipt.objects.get(
            listing=self.completed_offer_listing_2)
        self.completed_offer_listing_receipt_2.owner = self.global_user1
        self.completed_offer_listing_receipt_2.exchangee = self.global_user2
        self.completed_offer_listing_receipt_2.save()

        self.completed_auction_listing_receipt = Receipt.objects.get(
            listing=self.completed_auction_listing)
        self.completed_auction_listing_receipt.owner = self.global_user1
        self.completed_auction_listing_receipt.exchangee = self.global_user2
        self.completed_auction_listing_receipt.save()

        self.active_auction_listing_receipt = Receipt.objects.get(
            listing=self.active_auction_listing)
        self.active_auction_listing_receipt.owner = self.global_user1
        self.active_auction_listing_receipt.exchangee = self.global_user2
        self.active_auction_listing_receipt.save()

    #Test to ensure that a user must be logged in to make payment
    def test_redirect_if_not_logged_in(self):
        receipt = self.completed_offer_listing_receipt
        response = self.client.get(reverse('send-payment', args=[str(receipt.id)]))
        self.assertRedirects(response,
            '/accounts/login/?next=/listings/receipts/{0}/send-payment'.format(receipt.id))

    #Test to ensure user is redirected if logged in and is not the
    #receipt exchangee for an offer listing
    def test_redirect_if_logged_in_offer_listing_not_exchangee(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        receipt = self.completed_offer_listing_receipt
        response = self.client.get(reverse('send-payment', args=[str(receipt.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is redirected if logged in and is the
    #receipt exchangee, and that the listing is completed but an amount
    #was not offered for an offer listing
    def test_redirect_if_logged_in_offer_listing_exchangee_no_amount_offered(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        receipt = self.completed_offer_listing_receipt_2
        response = self.client.get(reverse('send-payment', args=[str(receipt.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in and is the
    #receipt exchangee, and that the listing is completed and an amount
    #was offered for an offer listing
    def test_no_redirect_if_logged_offer_listing_in_exchangee(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        receipt = self.completed_offer_listing_receipt
        response = self.client.get(reverse('send-payment', args=[str(receipt.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in and is not the
    #receipt exchangee for an auction listing
    def test_redirect_if_logged_in_auction_listing_not_exchangee(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        receipt = self.completed_auction_listing_receipt
        response = self.client.get(reverse('send-payment', args=[str(receipt.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is redirected if logged in and is the
    #receipt exchangee, but the listing is still active for an auction listing
    def test_redirect_if_logged_in_offer_listing_exchangee_listing_still_active(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        receipt = self.active_auction_listing_receipt
        response = self.client.get(reverse('send-payment', args=[str(receipt.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in and is the
    #receipt exchangee, and that the listing is completed for an
    #auction listing
    def test_no_redirect_if_logged_in_auction_listing_exchangee(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        receipt = self.completed_auction_listing_receipt
        response = self.client.get(reverse('send-payment', args=[str(receipt.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        receipt = self.completed_offer_listing_receipt
        response = self.client.get(reverse('send-payment', args=[str(receipt.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'receipts/make_payment.html')

    #Test to ensure user is redirected if a payment receipt exists for the receipt
    def test_redirect_if_payment_receipt_exists(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        receipt = self.completed_offer_listing_receipt
        payment_receipt = PaymentReceipt.objects.create(
            receipt=self.completed_offer_listing_receipt,
            orderID="Dkjid62d5tg41g", status="Completed", amountPaid=5.00,
            paymentDate="October 31st, 5:00 P.M.")
        response = self.client.get(reverse('send-payment', args=[str(receipt.id)]))
        self.assertRedirects(response, '/listings/')

#Tests for a user to see details on payment
class PaypalPaymentMadeViewTest(MyTestCase):
    def setUp(self):
        super(PaypalPaymentMadeViewTest, self).setUp()

        #Create user for testing with
        self.user1 = User.objects.create_user(username="mikey", password="example",
            email="example@text.com", paypalEmail="example@text.com",
            invitesOpen=True, inquiriesOpen=True)

        #Get the current date and time for testing and create inactive endtime
        date_ended = timezone.localtime(timezone.now()) - timedelta(hours=1)

        #Create completed listings for testing with
        self.completed_offer_listing_payment_made = OfferListing.objects.create(owner=self.global_user1,
            name='Test Offer Listing', description="Just a test listing",
            openToMoneyOffers=True, minRange=5.00, maxRange=10.00,
            notes="Just offer", endTime=date_ended, listingCompleted=True)
        self.completed_offer_listing_payment_not_made = OfferListing.objects.create(owner=self.global_user1,
            name='Test Offer Listing', description="Just a test listing",
            openToMoneyOffers=True, minRange=5.00, maxRange=10.00,
            notes="Just offer", endTime=date_ended, listingCompleted=True)

        #Create accepted offers associated with listings
        self.accepted_offer_payment_made = Offer.objects.create(
            offerListing=self.completed_offer_listing_payment_made,
            owner=self.global_user2, amount=5.00, offerAccepted=True)
        self.accepted_offer_payment_not_made = Offer.objects.create(
            offerListing=self.completed_offer_listing_payment_not_made,
            owner=self.global_user2, amount=5.00, offerAccepted=True)

        #Edit the receipts associated with the listings
        self.payment_made_receipt = Receipt.objects.get(
            listing=self.completed_offer_listing_payment_made)
        self.payment_made_receipt.owner = self.global_user1
        self.payment_made_receipt.exchangee = self.global_user2
        self.payment_made_receipt.save()

        self.payment_not_made_receipt = Receipt.objects.get(
            listing=self.completed_offer_listing_payment_not_made)
        self.payment_not_made_receipt.owner = self.global_user1
        self.payment_not_made_receipt.exchangee = self.global_user2
        self.payment_not_made_receipt.save()

        #Create payment receipt
        self.payment_receipt = PaymentReceipt.objects.create(
            receipt=self.payment_made_receipt, orderID="15c55f7vb3",
            status="COMPLETE", amountPaid="5.00",
            paymentDate="October 31st 2020, 5:00 PM")

    #Test to ensure that a user must be logged in to view payment receipt
    def test_redirect_if_not_logged_in(self):
        receipt = self.payment_made_receipt
        response = self.client.get(reverse('payment-made', args=[str(receipt.id)]))
        self.assertRedirects(response,
            '/accounts/login/?next=/listings/receipts/{0}/payment-made'.format(receipt.id))

    #Test to ensure user is redirected if logged in and is not the
    #receipt exchangee or owner for receipt
    def test_redirect_if_logged_in_not_owner_or_exchangee_on_receipt(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        receipt = self.payment_made_receipt
        response = self.client.get(reverse('payment-made', args=[str(receipt.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in and is the
    #receipt exchangee for receipt for receipt that has been paid
    def test_no_redirect_if_logged_in_exchangee_on_receipt(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        receipt = self.payment_made_receipt
        response = self.client.get(reverse('payment-made', args=[str(receipt.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is not redirected if logged in and is the
    #receipt owner for receipt for receipt that has been paid
    def test_no_redirect_if_logged_in_owner_on_receipt(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        receipt = self.payment_made_receipt
        response = self.client.get(reverse('payment-made', args=[str(receipt.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in and is the receipt
    #exchangee for receipt, but receipt has not been paid
    def test_redirect_if_logged_in_exchangee_on_receipt_no_payment(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        receipt = self.payment_not_made_receipt
        response = self.client.get(reverse('payment-made', args=[str(receipt.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is redirected if logged in and is the receipt
    #owner for receipt, but receipt has not been paid
    def test_redirect_if_logged_in_owner_on_receipt_no_payment(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        receipt = self.payment_not_made_receipt
        response = self.client.get(reverse('payment-made', args=[str(receipt.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        receipt = self.payment_made_receipt
        response = self.client.get(reverse('payment-made', args=[str(receipt.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'receipts/payment_made.html')

#Tests for the view that creates payment details
class CreatePaymentReceiptViewTest(MyTestCase):
    def setUp(self):
        super(CreatePaymentReceiptViewTest, self).setUp()

        #Get the current date and time for testing and create inactive endtimes
        date_ended = timezone.localtime(timezone.now()) - timedelta(hours=1)

        #Create a listing for testing with
        self.completed_offer_listing = OfferListing.objects.create(owner=self.global_user1,
            name='Test Offer Listing', description="Just a test listing",
            openToMoneyOffers=True, minRange=5.00, maxRange=10.00,
            notes="Just offer", endTime=date_ended, listingCompleted=True)

        #Create objects related to listings
        self.accepted_offer = Offer.objects.create(offerListing=self.completed_offer_listing,
            owner=self.global_user2, amount=5.00, offerAccepted=True)

        #Update the related receipts
        self.completed_offer_listing_receipt = Receipt.objects.get(
            listing=self.completed_offer_listing)
        self.completed_offer_listing_receipt.owner = self.global_user1
        self.completed_offer_listing_receipt.exchangee = self.global_user2
        self.completed_offer_listing_receipt.save()

    #Test to ensure that the view canbe called called
    def test_view_is_called(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-payment-receipt'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure that the view responds negatively to call if no data
    #was sent
    def test_view_responds_fail_no_data_sent(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-payment-receipt'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-payment-receipt'),
            data={})
        self.assertEqual(post_response.status_code, 404)

    #Test to ensure that the view responds positevely to call if receipt
    #id is sent
    def test_view_responds_success_receipt_id_sent(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-payment-receipt'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-payment-receipt'),
            data={'receipt_id': [str(self.completed_offer_listing_receipt.id)]})
        self.assertEqual(post_response.status_code, 200)

    #Test to ensure that a payment receipt is made using details from paypal,
    #and that receipt owner receives a notificationthat payment was made
    def test_view_creates_payment_receipt(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('create-payment-receipt'))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-payment-receipt'),
            data={'receipt_id': [str(self.completed_offer_listing_receipt.id)],
                'order_id': "f5g1g5ghh5v26d", 'status': "Complete",
                'amount': 5.00})
        self.assertEqual(post_response.status_code, 200)
        payment_receipt = PaymentReceipt.objects.last()
        self.assertTrue(payment_receipt.receipt, self.completed_offer_listing_receipt)
        self.assertTrue(payment_receipt.orderID, "f5g1g5ghh5v26d")
        self.assertTrue(payment_receipt.status, "Complete")
        self.assertTrue(payment_receipt.amountPaid, 5.00)
        payment_notification = PaymentNotification.objects.last()
        content = (self.completed_offer_listing_receipt.exchangee.username +
            ' has made a ' + 'payment of $5.00' + ' on the listing "' +
            self.completed_offer_listing_receipt.listing.name + '".')
        self.assertEqual(payment_notification.content, content)
        self.assertEqual(payment_notification.user,
            self.completed_offer_listing_receipt.owner)
        self.assertEqual(payment_notification.receipt,
            self.completed_offer_listing_receipt)
        self.assertEqual(payment_notification.type, "Payment Made")

#Tests for a user to delete a receipt
class ReceiptDeleteViewTest(MyTestCase):
    def setUp(self):
        super(ReceiptDeleteViewTest, self).setUp()

        #Create a new user for testing with
        self.user = User.objects.create_user(username="mikey", password="example",
            email="exampley@text.com", paypalEmail="exampley@text.com",
            invitesOpen=True, inquiriesOpen=True)

        #Get the current date and time for testing and create active and inactive endtimes
        date_ended = timezone.localtime(timezone.now()) - timedelta(hours=1)
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        #Create objects that will be deleted upon receipt deletion
        #if the last remaining user deletes it
        test_image_1 = SimpleUploadedFile(name='art1.png', content=open('listings/imagetest/art1.png', 'rb').read(), content_type='image/png')
        self.image_to_delete_1 = Image.objects.create(owner=None,
            image=test_image_1, name="Image to be deleted")
        self.image_to_delete_1_id = self.image_to_delete_1.id
        test_image_2 = SimpleUploadedFile(name='art1.png', content=open('listings/imagetest/art1.png', 'rb').read(), content_type='image/png')
        self.image_to_delete_2 = Image.objects.create(owner=None,
            image=test_image_2, name="Image to be deleted")
        self.image_to_delete_2_id = self.image_to_delete_2.id

        self.item_to_delete_1 = Item.objects.create(name="Item to Delete",
            description="An item to test with deletion", owner=None)
        self.item_to_delete_1.images.add(self.image_to_delete_1)
        self.item_to_delete_1.save
        self.item_to_delete_1_id = self.item_to_delete_1.id

        self.item_to_delete_2 = Item.objects.create(name="Item to Delete",
            description="An item to test with deletion", owner=None)
        self.item_to_delete_2.images.add(self.image_to_delete_2)
        self.item_to_delete_2.save
        self.item_to_delete_2_id = self.item_to_delete_2.id

        self.offer_listing_to_delete = OfferListing.objects.create(owner=None,
            name='Offer Listing to delete', description="To test deletion",
            openToMoneyOffers=True, minRange=5.00, maxRange=10.00,
            notes="Just offer", endTime=date_ended, listingCompleted=True)
        self.offer_listing_to_delete.items.add(self.item_to_delete_1)
        self.offer_listing_to_delete.save
        self.offer_listing_to_delete_id = self.offer_listing_to_delete.id

        self.offer_to_delete = Offer.objects.create(
            offerListing=self.offer_listing_to_delete,
            owner=None, amount=5.00, offerAccepted=True)
        self.offer_to_delete.items.add(self.item_to_delete_2)
        self.offer_to_delete.save
        self.offer_to_delete_id = self.offer_to_delete.id

        self.ol_receipt = Receipt.objects.get(listing=self.offer_listing_to_delete)
        self.ol_receipt.owner = self.global_user1
        self.ol_receipt.exchangee = self.global_user2
        self.ol_receipt.save()
        self.ol_receipt_id = self.ol_receipt.id

        self.ol_payment_receipt = PaymentReceipt.objects.create(
            receipt=self.ol_receipt, orderID="15c55f7vb3",
            status="COMPLETE", amountPaid="5.00",
            paymentDate="October 31st 2020, 5:00 PM")
        self.ol_payment_receipt_id = self.ol_payment_receipt.id

        self.auction_listing_to_delete = AuctionListing.objects.create(
            owner=None, name='auction listing to delete',
            description="To test for deletion", startingBid=5.00,
            minimumIncrement=1.00, autobuy=25.00, endTime=date_ended)
        self.auction_listing_to_delete.items.add(self.item_to_delete_1)
        self.auction_listing_to_delete.save
        self.auction_listing_to_delete_id = self.auction_listing_to_delete.id

        self.bid_to_delete = Bid.objects.create(
            auctionListing=self.auction_listing_to_delete,
            bidder=self.global_user2, amount=5.00, winningBid=True)
        self.bid_to_delete_id = self.bid_to_delete.id

        self.al_receipt = Receipt.objects.get(listing=self.auction_listing_to_delete)
        self.al_receipt.owner = self.global_user1
        self.al_receipt.exchangee = self.global_user2
        self.al_receipt.save()
        self.al_receipt_id = self.al_receipt.id

        self.al_payment_receipt = PaymentReceipt.objects.create(
            receipt=self.al_receipt, orderID="15c55f7vb3",
            status="COMPLETE", amountPaid="5.00",
            paymentDate="October 31st 2020, 5:00 PM")
        self.al_payment_receipt_id = self.al_payment_receipt.id

        self.active_receipt = Receipt.objects.get(listing=self.global_offer_listing1)
        self.active_receipt.owner = self.global_user1
        self.active_receipt.exchangee = self.global_user2
        self.active_receipt.save()
        self.active_receipt_id = self.active_receipt.id

        #Create notifications related to objects
        #Offer Notification
        content = ('Test Notification')
        self.offer_notification = OfferNotification.objects.create(
            listing=self.offer_to_delete.offerListing,
            offer=self.offer_to_delete, user=self.offer_to_delete.owner,
            content=content, creationDate=timezone.localtime(timezone.now()),
            type="Offer Accepted")

        #Payment notification for offer listing
        PaymentNotification.objects.create(receipt=self.ol_receipt,
            user=self.ol_receipt.owner, content=content,
            type="Payment Made",
            creationDate=timezone.localtime(timezone.now()))

        #Bid notification
        BidNotification.objects.create(
            listing=self.bid_to_delete.auctionListing,
            user=self.bid_to_delete.bidder, bid=self.bid_to_delete,
            creationDate=self.bid_to_delete.auctionListing.endTime,
            content=content, type="Winning Bid")

        #Payment notification for auction listing
        PaymentNotification.objects.create(receipt=self.al_receipt,
            user=self.al_receipt.owner, content=content,
            type="Payment Made",
            creationDate=timezone.localtime(timezone.now()))

        #Listing Notifications
        ListingNotification.objects.create(
            user=self.auction_listing_to_delete.owner,
            listing=self.auction_listing_to_delete, content=content,
            creationDate=self.auction_listing_to_delete.endTime,
            type="Listing Ended")
        ListingNotification.objects.create(
            user=self.offer_listing_to_delete.owner,
            listing=self.offer_listing_to_delete, content=content,
            creationDate=self.offer_listing_to_delete.endTime,
            type="Listing Ended")

    #Test to ensure that a user must be logged in to delete a receipt
    def test_redirect_if_not_logged_in(self):
        receipt = self.ol_receipt
        response = self.client.get(reverse('delete-receipt', args=[str(receipt.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure that a user is redirected if they are not the owner
    #or exchangee of the receipt
    def test_redirect_if_logged_in_not_owner_or_exchangee(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        receipt = self.ol_receipt
        response = self.client.get(reverse('delete-receipt', args=[str(receipt.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in if the are the owner
    #on the receipt
    def test_no_redirect_if_logged_in_owner(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        receipt = self.ol_receipt
        response = self.client.get(reverse('delete-receipt', args=[str(receipt.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is not redirected if logged in if the are the exchangee
    #on the receipt
    def test_no_redirect_if_logged_in_exchangee(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        receipt = self.ol_receipt
        response = self.client.get(reverse('delete-receipt', args=[str(receipt.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        receipt = self.ol_receipt
        response = self.client.get(reverse('delete-receipt', args=[str(receipt.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'receipts/receipt_delete.html')

    #Test to ensure receipt is not deleted if one user removes themselves
    #from receipt but other user hasn't yet, for offer listing receipts
    def test_successful_removal_of_user_ol_receipt(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        receipt = self.ol_receipt
        post_response = self.client.post(reverse('delete-receipt', args=[str(receipt.id)]))
        self.assertRedirects(post_response, reverse('receipts'))
        self.assertTrue(Receipt.objects.filter(id=self.ol_receipt_id).exists())

    #Test to ensure conversation is deleted if the last user removes themselves
    #from the conversation, for offer listing receipts
    def test_successful_deletion_ol_receipt(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        receipt = self.ol_receipt
        post_response = self.client.post(reverse('delete-receipt', args=[str(receipt.id)]))
        self.assertRedirects(post_response, reverse('receipts'))
        self.assertTrue(Receipt.objects.filter(id=self.ol_receipt_id).exists())
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        post_response = self.client.post(reverse('delete-receipt', args=[str(receipt.id)]))
        self.assertRedirects(post_response, reverse('receipts'))
        self.assertFalse(Receipt.objects.filter(id=self.ol_receipt_id).exists())

    #Test to ensure receipt is not deleted if one user removes themselves
    #from receipt but other user hasn't yet, for auction listing receipts
    def test_successful_removal_of_user_al_receipt(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        receipt = self.al_receipt
        post_response = self.client.post(reverse('delete-receipt', args=[str(receipt.id)]))
        self.assertRedirects(post_response, reverse('receipts'))
        self.assertTrue(Receipt.objects.filter(id=self.al_receipt_id).exists())

    #Test to ensure conversation is deleted if the last user removes themselves
    #from the conversation, for auction listing receipts
    def test_successful_deletion_al_receipt(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        receipt = self.al_receipt
        post_response = self.client.post(reverse('delete-receipt', args=[str(receipt.id)]))
        self.assertRedirects(post_response, reverse('receipts'))
        self.assertTrue(Receipt.objects.filter(id=self.al_receipt_id).exists())
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        post_response = self.client.post(reverse('delete-receipt', args=[str(receipt.id)]))
        self.assertRedirects(post_response, reverse('receipts'))
        self.assertFalse(Receipt.objects.filter(id=self.al_receipt_id).exists())

    #Test to ensure related items to receipt are deleted if owner is none,
    #unless object has relations to other objects, for offer listing receipts
    def test_successful_deletion_ol_receipt_relationships_deleted(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        receipt = self.ol_receipt
        post_response = self.client.post(reverse('delete-receipt', args=[str(receipt.id)]))
        self.assertRedirects(post_response, reverse('receipts'))
        self.assertTrue(Receipt.objects.filter(id=self.ol_receipt_id).exists())
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        post_response = self.client.post(reverse('delete-receipt', args=[str(receipt.id)]))
        self.assertRedirects(post_response, reverse('receipts'))
        self.assertFalse(Receipt.objects.filter(id=self.ol_receipt_id).exists())
        self.assertFalse(PaymentReceipt.objects.filter(id=self.ol_payment_receipt_id).exists())
        self.assertFalse(Listing.objects.filter(id=self.offer_listing_to_delete_id).exists())
        self.assertFalse(Offer.objects.filter(id=self.offer_to_delete_id).exists())
        self.assertTrue(Item.objects.filter(id=self.item_to_delete_1_id).exists())
        self.assertFalse(Item.objects.filter(id=self.item_to_delete_2_id).exists())
        self.assertTrue(Image.objects.filter(id=self.image_to_delete_1_id).exists())
        self.assertFalse(Image.objects.filter(id=self.image_to_delete_2_id).exists())

    #Test to ensure related notifications to receipt are deleted,
    #for offer listing receipts
    def test_successful_deletion_ol_receipt_notifications_deleted(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        receipt = self.ol_receipt
        post_response = self.client.post(reverse('delete-receipt', args=[str(receipt.id)]))
        self.assertRedirects(post_response, reverse('receipts'))
        self.assertTrue(Receipt.objects.filter(id=self.ol_receipt_id).exists())
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        post_response = self.client.post(reverse('delete-receipt', args=[str(receipt.id)]))
        self.assertRedirects(post_response, reverse('receipts'))
        self.assertFalse(OfferNotification.objects.filter(
            listing__id=self.offer_listing_to_delete_id).exists())
        self.assertFalse(ListingNotification.objects.filter(
            listing__id=self.offer_listing_to_delete_id).exists())
        self.assertFalse(PaymentNotification.objects.filter(
            receipt__id=self.ol_receipt_id).exists())

    #Test to ensure related items to receipt are deleted if owner is none,
    #unless object has relations to other objects, for auction listing receipts
    def test_successful_deletion_al_receipt_relationships_deleted(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        receipt = self.al_receipt
        post_response = self.client.post(reverse('delete-receipt', args=[str(receipt.id)]))
        self.assertRedirects(post_response, reverse('receipts'))
        self.assertTrue(Receipt.objects.filter(id=self.al_receipt_id).exists())
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        post_response = self.client.post(reverse('delete-receipt', args=[str(receipt.id)]))
        self.assertRedirects(post_response, reverse('receipts'))
        self.assertFalse(Receipt.objects.filter(id=self.al_receipt_id).exists())
        self.assertFalse(PaymentReceipt.objects.filter(id=self.al_payment_receipt_id).exists())
        self.assertFalse(Listing.objects.filter(id=self.auction_listing_to_delete_id).exists())
        self.assertFalse(Bid.objects.filter(id=self.bid_to_delete_id).exists())
        self.assertTrue(Item.objects.filter(id=self.item_to_delete_1_id).exists())
        self.assertTrue(Image.objects.filter(id=self.image_to_delete_1_id).exists())

    #Test to ensure related notifications to receipt are deleted,
    #for auction listing receipts
    def test_successful_deletion_al_receipt_notifications_deleted(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        receipt = self.al_receipt
        post_response = self.client.post(reverse('delete-receipt', args=[str(receipt.id)]))
        self.assertRedirects(post_response, reverse('receipts'))
        self.assertTrue(Receipt.objects.filter(id=self.al_receipt_id).exists())
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        post_response = self.client.post(reverse('delete-receipt', args=[str(receipt.id)]))
        self.assertRedirects(post_response, reverse('receipts'))
        self.assertFalse(BidNotification.objects.filter(
            listing__id=self.auction_listing_to_delete_id).exists())
        self.assertFalse(ListingNotification.objects.filter(
            listing__id=self.auction_listing_to_delete_id).exists())
        self.assertFalse(PaymentNotification.objects.filter(
            receipt__id=self.al_receipt_id).exists())

    #Test to ensure user is redirected if trying to delete an active receipt
    def test_redirect_if_logged_in_active_receipt(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        receipt = self.active_receipt
        response = self.client.get(reverse('delete-receipt', args=[str(receipt.id)]))
        self.assertRedirects(response, '/listings/')

#Tests for a user to view notifications they have received
class NotificationListViewTest(MyTestCase):
    def setUp(self):
        super(NotificationListViewTest, self).setUp()

        #Create some notifications for testing
        content = "Test Content"
        future_time = timezone.localtime(timezone.now()) + timedelta(days=1)
        self.notification_1 = OfferNotification.objects.create(
            listing=self.global_offer_listing1, user=self.global_user1,
            content=content, creationDate=timezone.localtime(timezone.now()),
            type="Test")

        self.notification_2 = BidNotification.objects.create(
            listing=self.global_auction_listing1, user=self.global_user1,
            content=content, creationDate=timezone.localtime(timezone.now()),
            type="Test")

        self.receipt = Receipt.objects.get(listing=self.global_offer_listing3)
        self.notification_3 = PaymentNotification.objects.create(
            receipt=self.receipt, user=self.global_user1,
            content=content, creationDate=future_time,
            type="Test")

        ListingNotification.objects.create(
            listing=self.global_auction_listing2, user=self.global_user2,
            content=content, creationDate=timezone.localtime(timezone.now()),
            type="Test")

        EventNotification.objects.create(
            event=self.global_event, participant=self.global_user2,
            user=self.global_user2, content=content, creationDate=future_time,
            type="Test")

    #Test to ensure that a user must be logged in to view notifications
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('notifications'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/notifications/')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('notifications'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notifications/notifications.html')

    #Test to ensure that the user only sees notifications related to them
    #for user1
    def test_list_only_active_notifications_user1(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['notifications']), 2)

    #Test to ensure that the user only sees notifications related to them
    #for user2
    def test_list_only_active_notifications_user2(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['notifications']), 1)

    #Test to ensure that notifications become read when viewing notifications
    def test_active_notifications_become_read(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('notifications'))
        self.assertEqual(response.status_code, 200)
        notification = Notification.objects.get(id=self.notification_1.id)
        self.assertFalse(notification.unread)
        notification = Notification.objects.get(id=self.notification_2.id)
        self.assertFalse(notification.unread)
        notification = Notification.objects.get(id=self.notification_3.id)
        self.assertTrue(notification.unread)

#Tests for a user to delete notifications they have received
class DeleteNotificationsViewTest(MyTestCase):
    def setUp(self):
        super(DeleteNotificationsViewTest, self).setUp()

        #Create some notifications to test for deletion
        self.notification_id_list = []
        content = "Test Content"
        self.offer_notification = OfferNotification.objects.create(
            listing=self.global_offer_listing1, user=self.global_user1,
            content=content, creationDate=timezone.localtime(timezone.now()),
            type="Test")
        self.notification_id_list.append(self.offer_notification.id)
        self.offer_notification_id = self.offer_notification.id

        self.bid_notification = BidNotification.objects.create(
            listing=self.global_auction_listing1, user=self.global_user1,
            content=content, creationDate=timezone.localtime(timezone.now()),
            type="Test")
        self.notification_id_list.append(self.bid_notification.id)
        self.bid_notification_id = self.bid_notification.id

        self.receipt = Receipt.objects.get(listing=self.global_offer_listing3)
        self.payment_notification = PaymentNotification.objects.create(
            receipt=self.receipt, user=self.global_user1,
            content=content, creationDate=timezone.localtime(timezone.now()),
            type="Test")
        self.notification_id_list.append(self.payment_notification.id)
        self.payment_notification_id = self.payment_notification.id

    #Test to ensure view can be called
    def test_view_is_called(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('delete-notifications'))
        self.assertEqual(response.status_code, 404)

    #Test to ensure that the user can delete notifications successfully
    def test_notifications_deleted_succesfully(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        post_response = self.client.post(reverse('delete-notifications'),
            data={'data': self.notification_id_list})
        self.assertRedirects(post_response, '/listings/notifications/')
        self.assertFalse(OfferNotification.objects.filter(
            id=self.offer_notification_id).exists())
        self.assertFalse(BidNotification.objects.filter(
            id=self.bid_notification_id).exists())
        self.assertFalse(PaymentNotification.objects.filter(
            id=self.payment_notification_id).exists())

    #Test to ensure that the user can not delete notifications that are not
    #related to them
    def test_notifications_not_deleted_user_not_related(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        post_response = self.client.post(reverse('delete-notifications'),
            data={'data': self.notification_id_list})
        self.assertRedirects(post_response, '/listings/notifications/')
        self.assertTrue(OfferNotification.objects.filter(
            id=self.offer_notification_id).exists())
        self.assertTrue(BidNotification.objects.filter(
            id=self.bid_notification_id).exists())
        self.assertTrue(PaymentNotification.objects.filter(
            id=self.payment_notification_id).exists())

#Tests for a user to favorite a listing
class FavoriteListingTest(MyTestCase):
    def setUp(self):
        super(FavoriteListingTest, self).setUp()

        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        #Create a wishlist listing for testing with
        self.wishlist_listing = WishlistListing.objects.create(
            owner=self.global_user1, name='My Wishlist Listing',
            endTime=date_active, moneyOffer=5.00, notes="Just a test")
        self.wishlist_listing.items.add(self.global_item1)
        self.wishlist_listing.itemsOffer.add(self.global_item1)
        self.wishlist_listing.save

    #Test to ensure that the view canbe called called
    def test_view_is_called(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('favorite-listing'))
        self.assertEqual(response.status_code, 201)

    #Test to ensure that the view responds negatively to call if no data
    #was sent
    def test_view_responds_fail_no_data_sent(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('favorite-listing'))
        self.assertEqual(response.status_code, 201)
        post_response = self.client.post(reverse('favorite-listing'),
            data={})
        self.assertEqual(post_response.status_code, 404)

    #Test to ensure that the view responds positevely to call if data is sent
    def test_view_responds_success_data_sent(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('favorite-listing'))
        self.assertEqual(response.status_code, 201)
        post_response = self.client.post(reverse('favorite-listing'),
            data={'listing_id': [str(self.global_offer_listing1.id)]})
        self.assertEqual(post_response.status_code, 200)

    #Test to ensure that a listing favorite object is creating using the passed
    #listing ID for an offer listing
    def test_view_creates_favorite_object_offer_listing(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('favorite-listing'))
        self.assertEqual(response.status_code, 201)
        post_response = self.client.post(reverse('favorite-listing'),
            data={'listing_id': [str(self.global_offer_listing1.id)]})
        self.assertEqual(post_response.status_code, 200)
        favorite = Favorite.objects.last()
        self.assertEqual(favorite.user, post_response.wsgi_request.user)
        self.assertEqual(favorite.listingType, "Offer Listing")
        self.assertEqual(favorite.listing.name, self.global_offer_listing1.name)

    #Test to ensure that a listing favorite object is creating using the passed
    #listing ID for an auction listing
    def test_view_creates_favorite_object_auction_listing(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('favorite-listing'))
        self.assertEqual(response.status_code, 201)
        post_response = self.client.post(reverse('favorite-listing'),
            data={'listing_id': [str(self.global_auction_listing1.id)]})
        self.assertEqual(post_response.status_code, 200)
        favorite = Favorite.objects.last()
        self.assertEqual(favorite.user, post_response.wsgi_request.user)
        self.assertEqual(favorite.listingType, "Auction Listing")
        self.assertEqual(favorite.listing.name, self.global_auction_listing1.name)

    #Test to ensure that a listing favorite object is creating using the passed
    #listing ID for an wishlist listing
    def test_view_creates_favorite_object_wishlist_listing(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('favorite-listing'))
        self.assertEqual(response.status_code, 201)
        post_response = self.client.post(reverse('favorite-listing'),
            data={'listing_id': [str(self.wishlist_listing.id)]})
        self.assertEqual(post_response.status_code, 200)
        favorite = Favorite.objects.last()
        self.assertEqual(favorite.user, post_response.wsgi_request.user)
        self.assertEqual(favorite.listingType, "Wishlist Listing")
        self.assertEqual(favorite.listing.name, self.wishlist_listing.name)

    #Test to ensure that a user cannot favorite one of their own listings
    def test_view_user_cannot_favorite_owned_listing(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('favorite-listing'))
        self.assertEqual(response.status_code, 201)
        post_response = self.client.post(reverse('favorite-listing'),
            data={'listing_id': [str(self.wishlist_listing.id)]})
        self.assertEqual(post_response.status_code, 404)

    #Test to ensure that a user can unfavorite a previously favorited listing
    def test_view_user_can_unfavorite_listing(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('favorite-listing'))
        self.assertEqual(response.status_code, 201)
        post_response = self.client.post(reverse('favorite-listing'),
            data={'listing_id': [str(self.global_offer_listing1.id)]})
        self.assertEqual(post_response.status_code, 200)
        favorite = Favorite.objects.last()
        self.assertEqual(favorite.user, post_response.wsgi_request.user)
        self.assertEqual(favorite.listingType, "Offer Listing")
        self.assertEqual(favorite.listing.name, self.global_offer_listing1.name)
        favorite_id = favorite.id
        post_response = self.client.post(reverse('favorite-listing'),
            data={'listing_id': [str(self.global_offer_listing1.id)]})
        self.assertEqual(post_response.status_code, 200)
        self.assertFalse(Favorite.objects.filter(id=favorite_id).exists())

#Tests for a user to view a list of their favorites
class FavoritesViewTest(MyTestCase):
    def setUp(self):
        super(FavoritesViewTest, self).setUp()

        #Create favorite objects for different users
        Favorite.objects.create(listingType="Offer Listing",
            user=self.global_user2, listing=self.global_offer_listing1)
        Favorite.objects.create(listingType="Offer Listing",
            user=self.global_user2, listing=self.global_offer_listing2)
        Favorite.objects.create(listingType="Auction Listing",
            user=self.global_user2, listing=self.global_auction_listing1)
        Favorite.objects.create(listingType="Auction Listing",
            user=self.global_user2, listing=self.global_auction_listing2)

        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        #Create a wishlist listing for testing with
        self.new_listing = OfferListing.objects.create(owner=self.global_user2,
            name='Test Offer Listing', description="Just a test listing",
            openToMoneyOffers=True, minRange=5.00,
            maxRange=10.00, notes="Just offer", endTime=date_active,
            listingCompleted=False)
        self.new_listing.items.add(self.global_item2)
        self.new_listing.save

        Favorite.objects.create(listingType="Offer Listing",
            user=self.global_user1, listing=self.new_listing)

    #Test to ensure that a user must be logged in to view favorites
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('favorites'))
        self.assertRedirects(response, '/accounts/login/?next=/listings/favorites/')

    #Test to ensure user is not redirected if logged in
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'favorites/favorites.html')

    #Test to ensure that the user only sees favorites of active listings for
    #user 1
    def test_list_only_current_users_favorites_user1(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['favorites']) == 2)

    #Test to ensure that the user only sees favorites if active listings for
    #user 2
    def test_list_only_current_users_favorites_user2(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['favorites']) == 1)

#Tests for a user to search for listings
class SearchListingsViewTest(MyTestCase):
    def setUp(self):
        super(SearchListingsViewTest, self).setUp()

        #Set the locations of the users
        self.global_user1.profile.latitude = 40.0000
        self.global_user1.profile.longitude = -75.0000
        self.global_user1.profile.save()

        self.global_user2.profile.latitude = 40.6000
        self.global_user2.profile.longitude = -75.5500
        self.global_user2.profile.save()

        #Get the current date and time for testing and create active and inactive endtimes
        date_ended = timezone.localtime(timezone.now()) - timedelta(hours=1)
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        #Create a variety of images to test with
        test_image = SimpleUploadedFile(name='art1.png', content=open('listings/imagetest/art1.png', 'rb').read(), content_type='image/png')

        self.image1 = Image.objects.create(owner=self.global_user1,
            image=test_image, name="Test Image 1")
        self.home_tag = Tag.objects.create(name="Home")
        self.art_tag = Tag.objects.create(name="Art")
        self.lr_tag = Tag.objects.create(name="Living Room")
        self.image1.tags.add(self.home_tag)
        self.image1.tags.add(self.art_tag)
        self.image1.tags.add(self.lr_tag)
        self.image1.save

        self.image2 = Image.objects.create(owner=self.global_user1,
            image=test_image, name="Test Image 2")
        self.kitchen_tag = Tag.objects.create(name="Kitchen")
        self.image2.tags.add(self.home_tag)
        self.image2.tags.add(self.kitchen_tag)
        self.image2.save

        self.image3 = Image.objects.create(owner=self.global_user1,
            image=test_image, name="Test Image 3")
        self.bathroom_tag = Tag.objects.create(name="Bathroom")
        self.image3.tags.add(self.bathroom_tag)
        self.image3.save

        #Create items for testing with
        self.item1 = Item.objects.create(name="Art Item 1",
            description="Lovely art to test with", owner=self.global_user1)
        self.item1.images.add(self.image1)
        self.item1.images.add(self.image2)
        self.item1.save

        self.item2 = Item.objects.create(name="Art Item 2",
            description="Lovely art to test with", owner=self.global_user1)
        self.item2.images.add(self.image2)
        self.item2.save

        self.item3 = Item.objects.create(name="Art Item 3",
            description="Lovely art to test with", owner=self.global_user2)
        self.item3.images.add(self.image3)
        self.item3.save

        #Create a variety of listings to test for searching
        #Offer Listings for user 1
        self.offer_listing_1 = OfferListing.objects.create(owner=self.global_user1,
            name='Art for your living room and bathroom',
            description="Just a test listing", openToMoneyOffers=True,
            minRange=5.00, maxRange=10.00, notes="Just offer", endTime=date_active,
            listingCompleted=False, latitude=self.global_user1.profile.latitude,
            longitude=self.global_user1.profile.longitude)
        self.offer_listing_1.items.add(self.item1)
        self.offer_listing_1.save

        self.offer_listing_2 = OfferListing.objects.create(owner=self.global_user1,
            name='Just more art I guess',
            description="Just a test listing", openToMoneyOffers=True,
            minRange=5.00, maxRange=10.00, notes="Just offer", endTime=date_active,
            listingCompleted=False, latitude=self.global_user1.profile.latitude,
            longitude=self.global_user1.profile.longitude)
        self.offer_listing_2.items.add(self.item1)
        self.offer_listing_2.items.add(self.item2)
        self.offer_listing_2.save

        self.offer_listing_3 = OfferListing.objects.create(owner=self.global_user2,
            name="Guess what?  It's Art",
            description="Just a test listing", openToMoneyOffers=True,
            minRange=5.00, maxRange=10.00, notes="Just offer", endTime=date_active,
            listingCompleted=False, latitude=self.global_user2.profile.latitude,
            longitude=self.global_user2.profile.longitude)
        self.offer_listing_3.items.add(self.item3)
        self.offer_listing_3.save

        self.auction_listing_1 = AuctionListing.objects.create(owner=self.global_user1,
            name='Secret Listing', description="Just a test listing",
            startingBid=5.00, minimumIncrement=1.00, autobuy=25.00,
            endTime=date_active, latitude=self.global_user1.profile.latitude,
            longitude=self.global_user1.profile.longitude)
        self.auction_listing_1.items.add(self.item2)
        self.auction_listing_1.save

        self.auction_listing_2 = AuctionListing.objects.create(owner=self.global_user2,
            name='a r t', description="Just a test listing",
            startingBid=5.00, minimumIncrement=1.00, autobuy=25.00,
            endTime=date_active, latitude=self.global_user2.profile.latitude,
            longitude=self.global_user2.profile.longitude)
        self.auction_listing_2.items.add(self.item3)
        self.auction_listing_2.save

        self.auction_listing_3 = AuctionListing.objects.create(owner=self.global_user2,
            name='Just some art', description="Just a test listing",
            startingBid=5.00, minimumIncrement=1.00, autobuy=25.00,
            endTime=date_active, latitude=self.global_user2.profile.latitude,
            longitude=self.global_user2.profile.longitude)
        self.auction_listing_3.items.add(self.item3)
        self.auction_listing_3.save

        self.wishlist_listing_1 = WishlistListing.objects.create(
            owner=self.global_user1, name='I want this stuff', endTime=date_active,
            moneyOffer=5.00, notes="Just a test", latitude=self.global_user1.profile.latitude,
            longitude=self.global_user1.profile.longitude)
        self.wishlist_listing_1.items.add(self.item3)
        self.wishlist_listing_1.itemsOffer.add(self.item1)
        self.wishlist_listing_1.save

        self.wishlist_listing_2 = WishlistListing.objects.create(
            owner=self.global_user1, name='I would want to accuire this',
            endTime=date_active,
            moneyOffer=5.00, notes="Just a test", latitude=self.global_user1.profile.latitude,
            longitude=self.global_user1.profile.longitude)
        self.wishlist_listing_2.items.add(self.item3)
        self.wishlist_listing_2.itemsOffer.add(self.item2)
        self.wishlist_listing_2.save

        self.wishlist_listing_3 = WishlistListing.objects.create(
            owner=self.global_user1, name='Art I crave', endTime=date_active,
            moneyOffer=5.00, notes="Just a test", latitude=self.global_user1.profile.latitude,
            longitude=self.global_user1.profile.longitude)
        self.wishlist_listing_3.items.add(self.item3)
        self.wishlist_listing_3.itemsOffer.add(self.item1)
        self.wishlist_listing_3.itemsOffer.add(self.item2)
        self.wishlist_listing_3.save

    #Test to ensure that the view can be called called
    def test_view_is_called(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure that the view responds if data is sent
    def test_view_responds_with_data(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/', {'type': 'Offers'})
        self.assertEqual(response.status_code, 200)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of offers
    def test_view_responds_with_correct_listing_amount_for_offers(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/', {'type': 'Offers'})
        self.assertEqual(len(response.context['listings']), 3)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of offers for user in different location
    def test_view_responds_with_correct_listing_amount_for_offers_new_location(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/', {'type': 'Offers'})
        self.assertEqual(len(response.context['listings']), 1)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of offers including name
    def test_view_responds_with_correct_listing_amount_for_offers_and_name(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Offers', 'name': 'art for your'})
        self.assertEqual(len(response.context['listings']), 1)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of offers for user in different location including name
    def test_view_responds_with_correct_listing_amount_for_offers_and_name_new_location(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Offers', 'name': 'guess what'})
        self.assertEqual(len(response.context['listings']), 1)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of offers including tags
    def test_view_responds_with_correct_listing_amount_for_offers_and_tags(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Offers', 'tags': 'Home,Art'})
        self.assertEqual(len(response.context['listings']), 2)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of offers for user in different location including tags
    def test_view_responds_with_correct_listing_amount_for_offers_and_tags_new_location(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Offers', 'tags': 'Home,Art'})
        self.assertEqual(len(response.context['listings']), 0)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of offers including search radius
    def test_view_responds_with_correct_listing_amount_for_offers_and_radius(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Offers', 'searchRadius': '0.6700'})
        self.assertEqual(len(response.context['listings']), 4)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of offers for user in different location
    #including search radius
    def test_view_responds_with_correct_listing_amount_for_offers_and_raidus_new_location(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Offers', 'searchRadius': '0.6700'})
        self.assertEqual(len(response.context['listings']), 4)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of offers including all params
    def test_view_responds_with_correct_listing_amount_for_all_params(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Offers', 'name': 'art', 'tags': 'Bathroom',
            'searchRadius': '0.6700'})
        self.assertEqual(len(response.context['listings']), 1)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of offers for user in different location
    #including all params
    def test_view_responds_with_correct_listing_amount_for_all_params_new_location(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Offers', 'name': 'art', 'tags': 'Bathroom',
            'searchRadius': '0.6700'})
        self.assertEqual(len(response.context['listings']), 1)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of auctions
    def test_view_responds_with_correct_listing_amount_for_auctions(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/', {'type': 'Auctions'})
        self.assertEqual(len(response.context['listings']), 2)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of auctions for user in different location
    def test_view_responds_with_correct_listing_amount_for_auctions_new_location(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/', {'type': 'Auctions'})
        self.assertEqual(len(response.context['listings']), 2)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of auctions including name
    def test_view_responds_with_correct_listing_amount_for_auctions_and_name(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Auctions', 'name': 'secret'})
        self.assertEqual(len(response.context['listings']), 1)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of auctions for user in different location including name
    def test_view_responds_with_correct_listing_amount_for_auctions_and_name_new_location(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Auctions', 'name': 'art'})
        self.assertEqual(len(response.context['listings']), 1)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of auctions including tags
    def test_view_responds_with_correct_listing_amount_for_auctions_and_tags(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Auctions', 'tags': 'Living Room'})
        self.assertEqual(len(response.context['listings']), 0)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of auctions for user in different location including tags
    def test_view_responds_with_correct_listing_amount_for_auctions_and_tags_new_location(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Auctions', 'tags': 'Bathroom'})
        self.assertEqual(len(response.context['listings']), 2)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of auctions including search radius
    def test_view_responds_with_correct_listing_amount_for_auctions_and_radius(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Auctions', 'searchRadius': '0.5000'})
        self.assertEqual(len(response.context['listings']), 2)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of auctions for user in different location
    #including search radius
    def test_view_responds_with_correct_listing_amount_for_auctions_and_raidus_new_location(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Auctions', 'searchRadius': '0.5000'})
        self.assertEqual(len(response.context['listings']), 2)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of auctions including all params
    def test_view_responds_with_correct_listing_amount_for_all_params_auctions(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Auctions', 'name': 'secret', 'tags': 'Home',
            'searchRadius': '0.6700'})
        self.assertEqual(len(response.context['listings']), 1)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of auctions for user in different location
    #including all params
    def test_view_responds_with_correct_listing_amount_for_all_params_new_location_auctions(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Auctions', 'name': 'a r t', 'tags': 'Bathroom',
            'searchRadius': '0.6700'})
        self.assertEqual(len(response.context['listings']), 1)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of wishlistswishlists
    def test_view_responds_with_correct_listing_amount_for_wishlists(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/', {'type': 'Wishlists'})
        self.assertEqual(len(response.context['listings']), 3)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of wishlists for user in different location
    def test_view_responds_with_correct_listing_amount_for_wishlists_new_location(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/', {'type': 'Wishlists'})
        self.assertEqual(len(response.context['listings']), 0)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of wishlists including name
    def test_view_responds_with_correct_listing_amount_for_wishlists_and_name(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Wishlists', 'name': 'want'})
        self.assertEqual(len(response.context['listings']), 2)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of wishlists for user in different location including name
    def test_view_responds_with_correct_listing_amount_for_wishlists_and_name_new_location(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Wishlists', 'name': 'art'})
        self.assertEqual(len(response.context['listings']), 0)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of wishlists including tags
    def test_view_responds_with_correct_listing_amount_for_wishlists_and_tags(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Wishlists', 'tags': 'Home,Kitchen'})
        self.assertEqual(len(response.context['listings']), 3)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of wishlists for user in different location including tags
    def test_view_responds_with_correct_listing_amount_for_wishlists_and_tags_new_location(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Wishlists', 'tags': 'Home,Kitchen'})
        self.assertEqual(len(response.context['listings']), 0)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of wishlists including search radius
    def test_view_responds_with_correct_listing_amount_for_wishlists_and_radius(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Wishlists', 'searchRadius': '0.6700'})
        self.assertEqual(len(response.context['listings']), 3)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of wishlists for user in different location
    #including search radius
    def test_view_responds_with_correct_listing_amount_for_wishlists_and_raidus_new_location(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Wishlists', 'searchRadius': '0.6700'})
        self.assertEqual(len(response.context['listings']), 3)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of wishlists including all params
    def test_view_responds_with_correct_listing_amount_for_all_params_wishlists(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Wishlists', 'name': 'want', 'tags': 'Home,Art',
            'searchRadius': '0.6700'})
        self.assertEqual(len(response.context['listings']), 2)

    #Test to ensure that the view returns the correct amount of listings
    #for listing type of wishlists for user in different location
    #including all params
    def test_view_responds_with_correct_listing_amount_for_all_params_new_location_wishlists(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('search-listings'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listings/search-listings/',
            {'type': 'Wishlists', 'name': 'art', 'tags': 'Home',
            'searchRadius': '0.6700'})
        self.assertEqual(len(response.context['listings']), 1)

#Tests for a superuser to view reports
class ReportsViewTest(MyTestCase):
    def setUp(self):
        super(ReportsViewTest, self).setUp()

        #Set a user to be a super user
        self.global_user1.is_superuser = True
        self.global_user1.save()

        #Create some reports for testing with
        for num in range(6):
            ListingReport.objects.create(reason='Malicious Content',
                description="Illegally obtained items in listing",
                reportType="Listing", listing=self.global_offer_listing1)

    #Test to ensure that a user must be logged in to view reports
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('reports'))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in and is a superuser
    def test_no_redirect_if_logged_in_superuser(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('reports'))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in but is not a superuser
    def test_redirect_if_logged_in_not_superuser(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('reports'))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('reports'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/reports.html')

    #Test to ensure that the user can see all reports
    def test_list_all_reports(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('reports'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['reports']) == 6)

#Tests for a user to report a listing
class ReportListingViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to report listing
    def test_redirect_if_not_logged_in(self):
        listing = self.global_offer_listing1
        response = self.client.get(reverse('report-listing', args=[str(listing.id)]))
        self.assertRedirects(response,
            '/accounts/login/?next=/listings/report-listing/{0}'.format(listing.id))

    #Test to ensure user is not redirected if logged in and is not the owner
    def test_no_redirect_if_logged_in_does_not_own_listing(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        listing = self.global_offer_listing1
        response = self.client.get(reverse('report-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in but owns the listing
    def test_redirect_if_logged_in_owns_listing(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.global_offer_listing1
        response = self.client.get(reverse('report-listing', args=[str(listing.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        listing = self.global_offer_listing1
        response = self.client.get(reverse('report-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/report_listing.html')

    #Test to ensure that a user is able to report a listing successfully
    def test_listing_report_is_created(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        listing = self.global_offer_listing1
        response = self.client.get(reverse('report-listing', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('report-listing', args=[str(listing.id)]),
            data={'reason': "Malicious Content",
                'description': "The items in this listing are illegally obtained."})
        self.assertEqual(post_response.status_code, 302)
        new_report = ListingReport.objects.last()
        self.assertEqual(new_report.reason, 'Malicious Content')
        self.assertEqual(new_report.description, 'The items in this listing are illegally obtained.')
        self.assertEqual(new_report.reportType, "Listing")
        self.assertEqual(new_report.listing.name, listing.name)

#Tests for a user to report an event
class ReportEventViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to report event
    def test_redirect_if_not_logged_in(self):
        event = self.global_event
        response = self.client.get(reverse('report-event', args=[str(event.id)]))
        self.assertRedirects(response,
            '/accounts/login/?next=/listings/report-event/{0}'.format(event.id))

    #Test to ensure user is not redirected if logged in and is not the host of
    #the event
    def test_no_redirect_if_logged_in_does_not_host_event(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('report-event', args=[str(event.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in but is hosting the event
    def test_redirect_if_logged_in_owns_listing(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('report-event', args=[str(event.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('report-event', args=[str(event.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/report_event.html')

    #Test to ensure that a user is able to report an event successfully
    def test_event_report_is_created(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('report-event', args=[str(event.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('report-event', args=[str(event.id)]),
            data={'reason': "Malicious Event",
                'description': "The event is for a pyramid scheme"})
        self.assertEqual(post_response.status_code, 302)
        new_report = EventReport.objects.last()
        self.assertEqual(new_report.reason, 'Malicious Event')
        self.assertEqual(new_report.description, 'The event is for a pyramid scheme')
        self.assertEqual(new_report.reportType, "Event")
        self.assertEqual(new_report.event, event)

#Tests for a user to report a user
class ReportUserViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to report a user
    def test_redirect_if_not_logged_in(self):
        user = self.global_user1
        response = self.client.get(reverse('report-user', args=[str(user.id)]))
        self.assertRedirects(response,
            '/accounts/login/?next=/listings/report-user/{0}'.format(user.id))

    #Test to ensure user is not redirected if logged in and is not reporting
    #themselves
    def test_no_redirect_if_logged_in_not_reporting_self(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        user = self.global_user1
        response = self.client.get(reverse('report-user', args=[str(user.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in but is reporting themself
    def test_redirect_if_logged_in_reporting_self(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        user = self.global_user1
        response = self.client.get(reverse('report-user', args=[str(user.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        user = self.global_user1
        response = self.client.get(reverse('report-user', args=[str(user.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/report_user.html')

    #Test to ensure that a user is able to report a user successfully
    def test_user_report_is_created(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        user = self.global_user1
        response = self.client.get(reverse('report-user', args=[str(user.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('report-user', args=[str(user.id)]),
            data={'reason': "Malicious User",
                'description': "User tried to scam me."})
        self.assertEqual(post_response.status_code, 302)
        new_report = UserReport.objects.last()
        self.assertEqual(new_report.reason, 'Malicious User')
        self.assertEqual(new_report.description, 'User tried to scam me.')
        self.assertEqual(new_report.reportType, "User")
        self.assertEqual(new_report.user, user)

#Tests for a user to report a wishlist
class ReportWishlistViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to report a wishlist
    def test_redirect_if_not_logged_in(self):
        wishlist = self.global_wishlist
        response = self.client.get(reverse('report-wishlist', args=[str(wishlist.id)]))
        self.assertRedirects(response,
            '/accounts/login/?next=/listings/report-wishlist/{0}'.format(wishlist.id))

    #Test to ensure user is not redirected if logged in and is reporting a
    #wishlist that is not theirs
    def test_no_redirect_if_logged_in_not_reporting_own_wishlist(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        wishlist = self.global_wishlist
        response = self.client.get(reverse('report-wishlist', args=[str(wishlist.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in but is reporting their own
    #wishlist
    def test_redirect_if_logged_in_reporting_own_wishlist(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        wishlist = self.global_wishlist
        response = self.client.get(reverse('report-wishlist', args=[str(wishlist.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        wishlist = self.global_wishlist
        response = self.client.get(reverse('report-wishlist', args=[str(wishlist.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/report_wishlist.html')

    #Test to ensure that a user is able to report a wishlist successfully
    def test_wishlist_report_is_created(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        wishlist = self.global_wishlist
        response = self.client.get(reverse('report-wishlist', args=[str(wishlist.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('report-wishlist', args=[str(wishlist.id)]),
            data={'reason': "Malicious Content",
                'description': "Questionable items in wishlist"})
        self.assertEqual(post_response.status_code, 302)
        new_report = WishlistReport.objects.last()
        self.assertEqual(new_report.reason, 'Malicious Content')
        self.assertEqual(new_report.description, 'Questionable items in wishlist')
        self.assertEqual(new_report.reportType, "Wishlist")
        self.assertEqual(new_report.wishlist, wishlist)

#Tests for a user to report an image
class ReportImageViewTest(MyTestCase):
    #Test to ensure that a user must be logged in to report a image
    def test_redirect_if_not_logged_in(self):
        image = self.global_image1
        response = self.client.get(reverse('report-image', args=[str(image.id)]))
        self.assertRedirects(response,
            '/accounts/login/?next=/listings/report-image/{0}'.format(image.id))

    #Test to ensure user is not redirected if logged in and is reporting a
    #image that is not theirs
    def test_no_redirect_if_logged_in_not_reporting_own_image(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        image = self.global_image1
        response = self.client.get(reverse('report-image', args=[str(image.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in but is reporting their own
    #image
    def test_redirect_if_logged_in_reporting_own_image(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        image = self.global_image1
        response = self.client.get(reverse('report-image', args=[str(image.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        image = self.global_image1
        response = self.client.get(reverse('report-image', args=[str(image.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/report_image.html')

    #Test to ensure that a user is able to report a image successfully
    def test_image_report_is_created(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        image = self.global_image1
        response = self.client.get(reverse('report-image', args=[str(image.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('report-image', args=[str(image.id)]),
            data={'reason': "Malicious Image",
                'description': "Questionable items in image"})
        self.assertEqual(post_response.status_code, 302)
        new_report = ImageReport.objects.last()
        self.assertEqual(new_report.reason, 'Malicious Image')
        self.assertEqual(new_report.description, 'Questionable items in image')
        self.assertEqual(new_report.reportType, "Image")
        self.assertEqual(new_report.image, image)

#Tests for a user to report a rating
class ReportRatingViewTest(MyTestCase):
    def setUp(self):
        super(ReportRatingViewTest, self).setUp()

        #Create a rating for testing with
        self.rating = Rating.objects.create(profile=self.global_user1.profile,
            reviewer=self.global_user2, ratingValue=3,
            feedback=("User was good on getting me the items on time" +
            " but did not communicate with me well."),
            listingName=self.global_offer_listing2.name)

    #Test to ensure that a user must be logged in to report a rating
    def test_redirect_if_not_logged_in(self):
        rating = self.rating
        response = self.client.get(reverse('report-rating', args=[str(rating.id)]))
        self.assertRedirects(response,
            '/accounts/login/?next=/listings/report-rating/{0}'.format(rating.id))

    #Test to ensure user is not redirected if logged in and is reporting a
    #rating for them
    def test_no_redirect_if_logged_in_reporting_rating_for_them(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        rating = self.rating
        response = self.client.get(reverse('report-rating', args=[str(rating.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged in but are not reporting a
    #rating meant for them
    def test_redirect_if_logged_in_reporting_rating_not_for_them(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        rating = self.rating
        response = self.client.get(reverse('report-rating', args=[str(rating.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        rating = self.rating
        response = self.client.get(reverse('report-rating', args=[str(rating.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/report_rating.html')

    #Test to ensure that a user is able to report a rating successfully
    def test_rating_report_is_created(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        rating = self.rating
        response = self.client.get(reverse('report-rating', args=[str(rating.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('report-rating', args=[str(rating.id)]),
            data={'reason': "False Rating",
                'description': "This user is lying."})
        self.assertEqual(post_response.status_code, 302)
        new_report = RatingReport.objects.last()
        self.assertEqual(new_report.reason, 'False Rating')
        self.assertEqual(new_report.description, 'This user is lying.')
        self.assertEqual(new_report.reportType, "Rating")
        self.assertEqual(new_report.rating, rating)

#Tests for a superuser to delete a rating
class ReportDeleteViewTest(MyTestCase):
    def setUp(self):
        super(ReportDeleteViewTest, self).setUp()

        #Set a user to be a super user
        self.global_user1.is_superuser = True
        self.global_user1.save()

        #Create a report to test for deletion
        self.listing_report = ListingReport.objects.create(reason='Malicious Content',
            description="Illegally obtained items in listing", reportType="Listing")
        self.listing_report_id = self.listing_report.id

    #Test to ensure that a user must be logged in to delete a report
    def test_redirect_if_not_logged_in(self):
        report = self.listing_report
        response = self.client.get(reverse('delete-report', args=[str(report.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure user is not redirected if logged in if they are a
    #superuser
    def test_no_redirect_if_logged_in_superuser(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        report = self.listing_report
        response = self.client.get(reverse('delete-report', args=[str(report.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged but they are not a
    #superuser
    def test_no_redirect_if_logged_in_not_superuser(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        report = self.listing_report
        response = self.client.get(reverse('delete-report', args=[str(report.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        report = self.listing_report
        response = self.client.get(reverse('delete-report', args=[str(report.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/report_delete.html')

    #Test to ensure a report can be deleted if user confirms
    def test_succesful_deletion_of_report(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        report = self.listing_report
        post_response = self.client.post(reverse('delete-report', args=[str(report.id)]))
        self.assertRedirects(post_response, reverse('reports'))
        self.assertFalse(Report.objects.filter(id=self.listing_report_id).exists())

#tests for a superuser to take action on a report
class TakeActionOnReportViewTest(MyTestCase):
    def setUp(self):
        super(TakeActionOnReportViewTest, self).setUp()

        #Set a user to be a super user
        self.global_user1.is_superuser = True
        self.global_user1.save()

        #Create rating for testing with
        self.rating = Rating.objects.create(profile=self.global_user1.profile,
            reviewer=self.global_user2, ratingValue=3,
            feedback=("User was good on getting me the items on time" +
            " but did not communicate with me well."),
            listingName=self.global_offer_listing2.name)

        #Create some reports for testing with
        self.listing_report = ListingReport.objects.create(
            listing=self.global_offer_listing1, reason="Malicious Content",
            description="The items are of concern", reportType="Listing")
        self.user_report = UserReport.objects.create(
            user=self.global_user2, reason="Malicious User",
            description="This user has bad intentions", reportType="User")
        self.event_report = EventReport.objects.create(
            event=self.global_event, reason="Malicious Event",
            description="This event is a scam", reportType="Event")
        self.wishlist_report = WishlistReport.objects.create(
            wishlist=self.global_wishlist, reason="Malicious Content",
            description="This wishlist has illegal items", reportType="Wishlist")
        self.image_report = ImageReport.objects.create(
            image=self.global_image1, reason="Malicious Image",
            description="The image depicts harmful items", reportType="Image")
        self.rating_report = RatingReport.objects.create(
            rating=self.rating, reason="False Rating",
            description="This rating is inaccurate", reportType="Rating")

    #Test to ensure that a user must be logged in to take action on report
    def test_redirect_if_not_logged_in(self):
        report = self.listing_report
        response = self.client.get(reverse('take-action-on-report', args=[str(report.id)]))
        self.assertRedirects(response,
            '/accounts/login/?next=/listings/reports/{0}/take-action'.format(report.id))

    #Test to ensure user is not redirected if logged in if they are a
    #superuser
    def test_no_redirect_if_logged_in_superuser(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        report = self.listing_report
        response = self.client.get(reverse('take-action-on-report', args=[str(report.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure user is redirected if logged but they are not a
    #superuser
    def test_no_redirect_if_logged_in_not_superuser(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        report = self.listing_report
        response = self.client.get(reverse('take-action-on-report', args=[str(report.id)]))
        self.assertRedirects(response, '/listings/')

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        report = self.listing_report
        response = self.client.get(reverse('take-action-on-report', args=[str(report.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/take_action_on_report.html')

    #Test to ensure that a user is able to submit form and object is not deleted
    #if "Manual Action" is action taken, and a notification is created
    def test_manual_action_taken(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        report = self.listing_report
        response = self.client.get(reverse(
            'take-action-on-report', args=[str(report.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse(
            'take-action-on-report', args=[str(report.id)]),
            data={'action_taken': "Take Manual Action",
                'reason': ("Your listing was reported for malicious items " +
                "contained in it.  The items have been removed.")})
        self.assertEqual(post_response.status_code, 302)
        self.assertTrue(
            OfferListing.objects.filter(id=self.global_offer_listing1.id).exists())
        new_notification = ListingNotification.objects.last()
        self.assertEqual(new_notification.listing.name, self.global_offer_listing1.name)
        self.assertEqual(new_notification.user, self.global_offer_listing1.owner)
        self.assertEqual(new_notification.type, 'Listing')
        content = ("Your listing, " + self.global_offer_listing1.name + ", has " +
            "been changed.  Reason: Your listing was reported for malicious " +
            "items contained in it.  The items have been removed.")
        self.assertEqual(new_notification.content, content)

    #Test to ensure that a user is able to submit form and object is deleted
    #if "Delete" is action taken, and a notification is created
    def test_delete_action_taken(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        report = self.listing_report
        response = self.client.get(reverse(
            'take-action-on-report', args=[str(report.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse(
            'take-action-on-report', args=[str(report.id)]),
            data={'action_taken': "Delete",
                'reason': ("The listing contained malicious items.")})
        self.assertEqual(post_response.status_code, 302)
        self.assertFalse(
            OfferListing.objects.filter(id=self.global_offer_listing1.id).exists())
        new_notification = Notification.objects.last()
        self.assertEqual(new_notification.user, self.global_user1)
        self.assertEqual(new_notification.type, 'Deletion')
        content = ("Your listing, " + self.global_offer_listing1.name + ", has " +
            "been deleted.  Reason: The listing contained malicious " +
            "items.")
        self.assertEqual(new_notification.content, content)

    #Test to ensure that a user is able to submit form and object is not deleted
    #if "Manual Action" is action taken, and a notification is created for
    #user report
    def test_manual_action_taken_user(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        report = self.user_report
        response = self.client.get(reverse(
            'take-action-on-report', args=[str(report.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse(
            'take-action-on-report', args=[str(report.id)]),
            data={'action_taken': "Take Manual Action",
                'reason': ("You were reported due to suspicious content on " +
                "your profile.  Your profile has been cleared as a result.")})
        self.assertEqual(post_response.status_code, 302)
        self.assertTrue(
            User.objects.filter(id=self.global_user2.id).exists())
        new_notification = Notification.objects.last()
        self.assertEqual(new_notification.user, self.global_user2)
        self.assertEqual(new_notification.type, 'User')
        content = ("An action has been made on your account.  " +
            "Reason: You were reported due to suspicious content on your " +
            "profile.  Your profile has been cleared as a result.")
        self.assertEqual(new_notification.content, content)

    #Test to ensure that a user is able to submit form and object is deleted
    #if "Delete" is action taken for user report
    def test_delete_action_taken_user(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        report = self.user_report
        response = self.client.get(reverse(
            'take-action-on-report', args=[str(report.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse(
            'take-action-on-report', args=[str(report.id)]),
            data={'action_taken': "Delete"})
        self.assertEqual(post_response.status_code, 302)
        self.assertFalse(
            User.objects.filter(id=self.global_user2.id).exists())

    #Test to ensure that a user is able to submit form and object is not deleted
    #if "Manual Action" is action taken, and a notification is created for
    #event report
    def test_manual_action_taken_event(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        report = self.event_report
        response = self.client.get(reverse(
            'take-action-on-report', args=[str(report.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse(
            'take-action-on-report', args=[str(report.id)]),
            data={'action_taken': "Take Manual Action",
                'reason': ("The event was reported due to malicious content.  " +
                "The event has been changed as a result.")})
        self.assertEqual(post_response.status_code, 302)
        self.assertTrue(
            Event.objects.filter(id=self.global_event.id).exists())
        new_notification = EventNotification.objects.last()
        self.assertEqual(new_notification.event, self.global_event)
        self.assertEqual(new_notification.user, self.global_event.host)
        self.assertEqual(new_notification.type, 'Event')
        content = ("Your event, " + self.global_event.title + ", has " +
            "been changed.  Reason: The event was reported due to malicious " +
            "content.  The event has been changed as a result.")
        self.assertEqual(new_notification.content, content)

    #Test to ensure that a user is able to submit form and object is deleted
    #if "Delete" is action taken for event report
    def test_delete_action_taken_event(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        report = self.event_report
        response = self.client.get(reverse(
            'take-action-on-report', args=[str(report.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse(
            'take-action-on-report', args=[str(report.id)]),
            data={'action_taken': "Delete",
                'reason': ("The event contained malicious content.")})
        self.assertEqual(post_response.status_code, 302)
        self.assertFalse(
            Event.objects.filter(id=self.global_event.id).exists())
        new_notification = Notification.objects.last()
        self.assertEqual(new_notification.user, self.global_user1)
        self.assertEqual(new_notification.type, 'Deletion')
        content = ("Your event, " + self.global_event.title + ", has " +
            "been deleted.  Reason: The event contained malicious content.")
        self.assertEqual(new_notification.content, content)

    #Test to ensure that a user is able to submit form and object is not deleted
    #if "Manual Action" is action taken, and a notification is created for
    #wishlist report
    def test_manual_action_taken_wishlist(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        report = self.wishlist_report
        response = self.client.get(reverse(
            'take-action-on-report', args=[str(report.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse(
            'take-action-on-report', args=[str(report.id)]),
            data={'action_taken': "Take Manual Action",
                'reason': ("Your wishlist contained malicious content.")})
        self.assertEqual(post_response.status_code, 302)
        self.assertTrue(
            Wishlist.objects.filter(id=self.global_wishlist.id).exists())
        new_notification = Notification.objects.last()
        self.assertEqual(new_notification.user, self.global_wishlist.owner)
        self.assertEqual(new_notification.type, 'Wishlist')
        content = ("Your wishlist has been changed.  Reason: Your " +
            "wishlist contained malicious content.")
        self.assertEqual(new_notification.content, content)

    #Test to ensure that a user is able to submit form and object is cleared
    #if "Delete" is action taken for wishlist report
    def test_delete_action_taken_wishlist(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        report = self.wishlist_report
        response = self.client.get(reverse(
            'take-action-on-report', args=[str(report.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse(
            'take-action-on-report', args=[str(report.id)]),
            data={'action_taken': "Delete",
                'reason': ("Your wishlist contained malicious content.")})
        self.assertEqual(post_response.status_code, 302)
        self.assertTrue(
            Wishlist.objects.filter(id=self.global_wishlist.id).exists())
        new_notification = Notification.objects.last()
        self.assertEqual(new_notification.user, self.global_user1)
        self.assertEqual(new_notification.type, 'Deletion')
        content = ("Your wishlist has been cleared.  Reason: Your wishlist " +
            "contained malicious content.")
        self.assertEqual(new_notification.content, content)
        wishlist = Wishlist.objects.get(id=self.global_wishlist.id)
        self.assertEqual(wishlist.title, "None")
        self.assertEqual(wishlist.description, "None")
        self.assertEqual(wishlist.items.count(), 0)

    #Test to ensure that a user is able to submit form and object is not deleted
    #if "Manual Action" is action taken, and a notification is created for
    #image report
    def test_manual_action_taken_image(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        report = self.image_report
        response = self.client.get(reverse(
            'take-action-on-report', args=[str(report.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse(
            'take-action-on-report', args=[str(report.id)]),
            data={'action_taken': "Take Manual Action",
                'reason': ("The image depicted malicious content.")})
        self.assertEqual(post_response.status_code, 302)
        self.assertTrue(
            Image.objects.filter(id=self.global_image1.id).exists())
        new_notification = Notification.objects.last()
        self.assertEqual(new_notification.user, self.global_image1.owner)
        self.assertEqual(new_notification.type, 'Image')
        content = ("Your image, " + self.global_image1.name + ", has been " +
            "changed.  Reason: The image depicted malicious content.")
        self.assertEqual(new_notification.content, content)

    #Test to ensure that a user is able to submit form and object is cleared
    #if "Delete" is action taken for image report
    def test_delete_action_taken_image(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        report = self.image_report
        response = self.client.get(reverse(
            'take-action-on-report', args=[str(report.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse(
            'take-action-on-report', args=[str(report.id)]),
            data={'action_taken': "Delete",
                'reason': ("The image depicted malicious content.")})
        self.assertEqual(post_response.status_code, 302)
        self.assertFalse(
            Image.objects.filter(id=self.global_image1.id).exists())
        new_notification = Notification.objects.last()
        self.assertEqual(new_notification.user, self.global_user1)
        self.assertEqual(new_notification.type, 'Deletion')
        content = ("Your image, " + self.global_image1.name + ", has been " +
            "deleted.  Reason: The image depicted malicious content.")
        self.assertEqual(new_notification.content, content)

    #Test to ensure that a user is able to submit form and object is not deleted
    #if "Manual Action" is action taken, and a notification is created for
    #rating report
    def test_manual_action_taken_rating(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        report = self.rating_report
        response = self.client.get(reverse(
            'take-action-on-report', args=[str(report.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse(
            'take-action-on-report', args=[str(report.id)]),
            data={'action_taken': "Take Manual Action",
                'reason': ("The rating was misleading.")})
        self.assertEqual(post_response.status_code, 302)
        self.assertTrue(
            Rating.objects.filter(id=self.rating.id).exists())
        new_notification = RatingNotification.objects.last()
        self.assertEqual(new_notification.profile, self.rating.profile)
        self.assertEqual(new_notification.user, self.rating.reviewer)
        self.assertEqual(new_notification.type, 'Feedback Left')
        content = ("Your rating for the listing, " + self.rating.listingName +
            ", has been changed.  Reason: The rating was misleading.")
        self.assertEqual(new_notification.content, content)

    #Test to ensure that a user is able to submit form and object is deleted
    #if "Delete" is action taken for rating report
    def test_delete_action_taken_rating(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        report = self.rating_report
        response = self.client.get(reverse(
            'take-action-on-report', args=[str(report.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse(
            'take-action-on-report', args=[str(report.id)]),
            data={'action_taken': "Delete",
                'reason': ("The rating was misleading.")})
        self.assertEqual(post_response.status_code, 302)
        self.assertFalse(
            Rating.objects.filter(id=self.rating.id).exists())
        new_notification = Notification.objects.last()
        self.assertEqual(new_notification.user, self.global_user2)
        self.assertEqual(new_notification.type, 'Deletion')
        content = ("Your rating for the listing, " + self.rating.listingName +
            ", has been deleted.  Reason: The rating was misleading.")
        self.assertEqual(new_notification.content, content)
