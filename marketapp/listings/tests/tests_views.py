from django.test import TestCase
from listings.models import (User, Image, Tag, Item, Listing, OfferListing,
    AuctionListing, Offer, Bid, Event, Invitation, Wishlist, WishlistListing,
    Profile, Conversation, Message, Receipt)

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

        #Create a global wishlist
        self.global_wishlist = Wishlist.objects.create(owner=self.global_user1,
            title="My Wishlist", description="Stuff I would love to trade for")
        self.global_wishlist.items.add(self.global_item1)
        self.global_wishlist.save

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

    #Test to ensure that a user is able to create an offer listing and
    #have it relate to them, and that a receipt is made for the listing
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
        self.assertTrue(new_offer_listing.receipt.exists())
        receipt = Receipt.objects.get(listing=new_offer_listing)
        self.assertEqual(receipt.owner, post_response.wsgi_request.user)

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

        self.active_offer_listing_offers = OfferListing.objects.create(owner=self.global_user1,
            name="My Items For Offers", description="A few items up for offers",
            openToMoneyOffers=True, minRange=5.00, maxRange=10.00,
            notes="Just offer", endTime=date_active)
        self.active_offer_listing_offers.items.add = self.global_item1
        self.active_offer_listing_offers.save
        self.active_offer_listing_offers_id = self.active_offer_listing_offers.id

        #Inactive listings
        self.inactive_offer_listing_no_offers = OfferListing.objects.create(owner=self.global_user1,
            name="My Items For Offers", description="A few items up for offers",
            openToMoneyOffers=True, minRange=5.00, maxRange=10.00,
            notes="Just offer", endTime=date_ended)
        self.inactive_offer_listing_no_offers.items.add = self.global_item1
        self.inactive_offer_listing_no_offers.save
        self.inactive_offer_listing_no_offers_id = self.inactive_offer_listing_no_offers.id

        self.inactive_offer_listing_offers = OfferListing.objects.create(owner=self.global_user1,
            name="My Items For Offers", description="A few items up for offers",
            openToMoneyOffers=True, minRange=5.00, maxRange=10.00,
            notes="Just offer", endTime=date_ended, listingCompleted=False)
        self.inactive_offer_listing_offers.items.add = self.global_item1
        self.inactive_offer_listing_offers.save
        self.inactive_offer_listing_offers_id = self.inactive_offer_listing_offers.id

        self.inactive_offer_listing_completed = OfferListing.objects.create(owner=self.global_user1,
            name="My Items For Offers", description="A few items up for offers",
            openToMoneyOffers=True, minRange=5.00, maxRange=10.00,
            notes="Just offer", endTime=date_ended, listingCompleted=True)
        self.inactive_offer_listing_completed.items.add = self.global_item1
        self.inactive_offer_listing_completed.save
        self.inactive_offer_listing_completed_id = self.inactive_offer_listing_completed.id

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

        for offer in range(number_of_offers):
            new_offer = Offer.objects.create(offerListing=self.inactive_offer_listing_offers,
                owner=self.global_user2, amount=7.00)
            new_offer.items.add(self.global_item2)
            new_offer.save
            self.inactive_offer_listing_offers_offer_ids[offer] = new_offer.id

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

    #Test to ensure user cannot delete an active offer listing with offers
    def test_unsuccessful_deletion_active_listing_offers(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.active_offer_listing_offers
        post_response = self.client.post(reverse('delete-offer-listing', args=[str(listing.id)]))
        self.assertEqual(post_response.status_code, 404)

    #Test to ensure that user can delete an inactive offer listing the was not
    #completed with no offers
    def test_successful_deletion_inactive_listing_no_offers(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.inactive_offer_listing_no_offers
        post_response = self.client.post(reverse('delete-offer-listing', args=[str(listing.id)]))
        self.assertRedirects(post_response, reverse('offer-listings'))
        self.assertFalse(OfferListing.objects.filter(id=self.inactive_offer_listing_no_offers_id).exists())

    #Test to ensure that user can delete an inactive offer listing the was not
    #completed with offers and offers are deleted
    def test_successful_deletion_inactive_listing_offers(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.inactive_offer_listing_offers
        post_response = self.client.post(reverse('delete-offer-listing', args=[str(listing.id)]))
        self.assertRedirects(post_response, reverse('offer-listings'))
        self.assertFalse(OfferListing.objects.filter(id=self.inactive_offer_listing_offers_id).exists())
        for offer_id in self.inactive_offer_listing_offers_offer_ids:
            self.assertFalse(Offer.objects.filter(id=offer_id).exists())

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
        self.assertTrue(len(response.context['bids']) == 1)

    #Test to ensure that the user only sees offers they have made for the second user
    def test_list_only_current_users_bids_user2(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('my-bids'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['bids']) == 1)

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

    #Test to ensure a user is able to create an auction listing and have it
    #relate to them.  Also test to ensure receipt for listing was created
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
        self.assertTrue(new_auction_listing.receipt.exists())
        receipt = Receipt.objects.get(listing=new_auction_listing)
        self.assertEqual(receipt.owner, post_response.wsgi_request.user)

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

    #Test to ensure that a bid is created succesfully and relates to the
    #current user
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

    #Test to ensure that listing receipt is updated when bid is placed
    def test_successful_bid_receipt_is_updated(self):
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
        receipt = Receipt.objects.get(listing=listing)
        self.assertEqual(receipt.exchangee, created_bid.bidder)

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
            owner=self.global_user2, amount=7.00, offerAccepted=False)

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

    #Test to ensure object can be deleted by listing owner
    def test_successful_deletion_by_listing_owner(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        offer = self.regular_offer
        offer_id = self.regular_offer.id
        post_response = self.client.post(reverse('delete-offer', args=[str(offer.id)]))
        self.assertRedirects(post_response, reverse('offer-listing-detail', args=[str(self.global_offer_listing1.id)]))
        self.assertFalse(Offer.objects.filter(id=offer_id).exists())

    #Test to ensure object can be deleted by offer owner
    def test_successful_deletion_by_offer_owner(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        offer = self.regular_offer
        offer_id = self.regular_offer.id
        post_response = self.client.post(reverse('delete-offer', args=[str(offer.id)]))
        self.assertRedirects(post_response, '/listings/offer-listings/my-offers')
        self.assertFalse(Offer.objects.filter(id=offer_id).exists())

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
        self.inactive_auction_listing_id = self.inactive_auction_listing.id

        self.inactive_auction_listing_no_bids = AuctionListing.objects.create(owner=self.global_user1,
            name='Test Auction Listing', description="Just a test listing", startingBid=5.00,
            minimumIncrement=1.00, autobuy=25.00, endTime=date_inactive)
        self.inactive_auction_listing_no_bids.items.add = self.global_item1
        self.inactive_auction_listing_no_bids.save
        self.inactive_auction_listing_no_bids_id = self.inactive_auction_listing_no_bids.id

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

    #Test to ensure that user can delete an expired auction listing
    #with no bids
    def test_successful_deletion_expired_listing_no_bids(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.inactive_auction_listing_no_bids
        post_response = self.client.post(reverse('delete-auction-listing', args=[str(listing.id)]))
        self.assertRedirects(post_response, reverse('auction-listings'))
        self.assertFalse(AuctionListing.objects.filter(id=self.inactive_auction_listing_no_bids_id).exists())

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

    #Test to ensure that the host can remove a participant from the event
    def test_user_is_removed_by_host(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        event = self.global_event
        post_response = self.client.post(reverse('remove-participant', args=[str(event.id), str(self.user1.id)]))
        self.assertEqual(post_response.status_code, 302)
        updated_event = Event.objects.get(id=event.id)
        self.assertFalse(event.participants.filter(pk=self.user1.pk).exists())

    #Test to ensure that a participant can remove themselves from the event
    def test_user_can_remove_themselves(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        event = self.global_event
        post_response = self.client.post(reverse('remove-participant', args=[str(event.id), str(self.global_user2.id)]))
        self.assertEqual(post_response.status_code, 302)
        updated_event = Event.objects.get(id=event.id)
        self.assertFalse(event.participants.filter(pk=self.global_user2.pk).exists())

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

    #Test to ensure that a user is able to create invitations for all users
    def test_invitations_are_created(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        event = self.global_event
        response = self.client.get(reverse('create-invitations', args=[str(event.id)]))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse('create-invitations', args=[str(event.id)]),
            data={'users': [str(self.user1.id), str(self.user2.id), str(self.user3.id)]})
        self.assertEqual(post_response.status_code, 302)
        self.assertTrue(Invitation.objects.filter(event=event, recipient=self.user1).exists())
        self.assertTrue(Invitation.objects.filter(event=event, recipient=self.user2).exists())
        self.assertTrue(Invitation.objects.filter(event=event, recipient=self.user3).exists())

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

    #Test to ensure that the event's participants are updated with the user that accepted
    def test_user_is_added_to_event(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        invitation = self.invitation
        event = invitation.event
        post_response = self.client.post(reverse('accept-invitation', args=[str(invitation.id)]))
        self.assertEqual(post_response.status_code, 302)
        updated_event = Event.objects.get(id=event.id)
        self.assertTrue(event.participants.filter(pk=self.user1.pk).exists())

    #Test to ensure that the invitation is destroyed after user accepts it
    def test_invitation_destroyed_after_acceptance(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        invitation = self.invitation
        invitation_id = invitation.id
        post_response = self.client.post(reverse('accept-invitation', args=[str(invitation.id)]))
        self.assertEqual(post_response.status_code, 302)
        self.assertFalse(Invitation.objects.filter(id=invitation_id).exists())

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

    #Test to ensure that the user is not added to event after declining
    def test_user_is_not_added_to_event(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        invitation = self.invitation
        event = invitation.event
        post_response = self.client.post(reverse('decline-invitation', args=[str(invitation.id)]))
        self.assertEqual(post_response.status_code, 302)
        refreshed_event = Event.objects.get(id=event.id)
        self.assertFalse(event.participants.filter(pk=self.user1.pk).exists())

    #Test to ensure that the invitation is destroyed after user declines it
    def test_invitation_destroyed_after_declining(self):
        login = self.client.login(username='mikey', password='example')
        self.assertTrue(login)
        invitation = self.invitation
        invitation_id = invitation.id
        post_response = self.client.post(reverse('decline-invitation', args=[str(invitation.id)]))
        self.assertEqual(post_response.status_code, 302)
        self.assertFalse(Invitation.objects.filter(id=invitation_id).exists())

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

class WishlistListingDetailViewTest(MyTestCase):
    def setUp(self):
        super(WishlistListingDetailViewTest, self).setUp()

        #Get the current date and time for testing and create active endTimes
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        #Wishlist listing to test with
        self.listing = WishlistListing.objects.create(owner=self.global_user1,
            name='My Wishlist Listing', endTime=date_active,
            moneyOffer=5.00, notes="Just a test")
        self.listing.items.add(self.global_item1)
        self.listing.save

    #Test to ensure that a user must be logged in to view wishlist listings
    def test_redirect_if_not_logged_in(self):
        listing = self.listing
        response = self.client.get(reverse('wishlist-listing-detail', args=[str(listing.id)]))
        self.assertRedirects(response,
            '/accounts/login/?next=/listings/wishlists/wishlist-listings/{0}'.format(listing.id))

    #Test to ensure owner is not redirected if logged in
    def test_no_redirect_if_logged_in_owner(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.listing
        response = self.client.get(reverse('wishlist-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure non owner is not redirected if logged in
    def test_no_redirect_if_logged_in_not_owner(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        listing = self.listing
        response = self.client.get(reverse('wishlist-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)

    #Test to ensure right template is used/exists
    def test_correct_template_used(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        listing = self.listing
        response = self.client.get(reverse('wishlist-listing-detail', args=[str(listing.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlists/wishlist_listing_detail.html')

class AllWishlistListingsViewTest(MyTestCase):
    def setUp(self):
        super(AllWishlistListingsViewTest, self).setUp()

        #Create a variety of listings to test with
        #Number of active listings should be 9
        number_of_active_listings_user1 = 3
        number_of_active_listings_user2 = 6
        number_of_inactive_listings_user1 = 7

        date_ended = timezone.localtime(timezone.now()) - timedelta(hours=1)
        date_active = timezone.localtime(timezone.now()) + timedelta(days=1)

        for num in range(number_of_active_listings_user1):
            listing = WishlistListing.objects.create(owner=self.global_user1,
                name='My Wishlist Listing #{0}'.format(num), endTime=date_active,
                moneyOffer=5.00, notes="Just a test")
            listing.items.add(self.global_item1)
            listing.itemsOffer.add(self.global_non_wishlist_item)
            listing.save

        for num in range(number_of_active_listings_user2):
            listing = WishlistListing.objects.create(owner=self.global_user2,
                name='My Wishlist Listing #{0}'.format(num), endTime=date_active,
                moneyOffer=5.00, notes="Just a test")
            listing.items.add(self.global_item2)
            listing.save

        for num in range(number_of_inactive_listings_user1):
            listing = WishlistListing.objects.create(owner=self.global_user1,
                name='My Wishlist Listing #{0}'.format(num), endTime=date_ended,
                moneyOffer=5.00, notes="Just a test")
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
        self.assertEqual(len(response.context['wishlistlistings']), 9)

    #Test to ensure that different user sees the correct amount of active listings
    def test_list_only_active_listings_new_user_page_1(self):
        login = self.client.login(username='mike3', password='example')
        self.assertTrue(login)
        response = self.client.get(reverse('all-wishlist-listings'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['wishlistlistings']), 9)

class CreateWishlistListingViewTest(MyTestCase):
    def setUp(self):
        super(CreateWishlistListingViewTest, self).setUp()

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

class ProfileDetailViewTest(MyTestCase):
    def setUp(self):
        super(ProfileDetailViewTest, self).setUp()

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

    #Test that a user can see the user that owns the profile's listings
    def test_user_can_see_listings(self):
        login = self.client.login(username='mike2', password='example')
        self.assertTrue(login)
        profile = self.global_user1.profile
        response = self.client.get(reverse('profile-detail', args=[str(profile.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['offer_listings']) == 3)
        self.assertTrue(len(response.context['auction_listings']) == 4)
        self.assertTrue(len(response.context['wishlist_listings']) == 5)

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
                receipt.save
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
                receipt.save

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
                receipt.save
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
                receipt.save

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
        receipt.save

        listing = AuctionListing.objects.create(owner=self.global_user1,
            name='Test Auction Listing', description="Just a test listing",
            startingBid=5.00, minimumIncrement=1.00, autobuy=25.00,
            endTime=date_active)
        Bid.objects.create(auctionListing=listing, bidder=self.user1,
            amount=5.00, winningBid=True)
        receipt = Receipt.objects.get(listing=listing)
        receipt.owner = self.global_user1
        receipt.exchangee = self.user1
        receipt.save

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
