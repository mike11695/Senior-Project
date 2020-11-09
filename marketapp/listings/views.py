from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.files.base import ContentFile
from django.contrib.gis.geoip2 import GeoIP2
from django.db.models import Count, Max, OuterRef, Subquery
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt

from listings.models import (User, Image, Item, Listing, OfferListing, AuctionListing,
    Offer, Bid, Event, Invitation, Wishlist, WishlistListing, Profile,
    Conversation, Message, Receipt, PaymentReceipt, ListingNotification,
    OfferNotification, BidNotification, PaymentNotification,
    InvitationNotification, EventNotification, Notification,
    RatingNotification, WarningNotification)
from listings.forms import (SignUpForm, AddImageForm, ItemForm, OfferListingForm,
    AuctionListingForm, UpdateOfferListingForm, OfferForm, EditOfferForm, CreateBidForm,
    EventForm, InvitationForm, WishlistForm, WishlistListingForm, QuickWishlistListingForm,
    EditWishlistListingForm, ProfileForm, EditAccountForm, ConversationForm,
    MessageForm, EditImageForm)

from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import make_aware
from django.conf import settings
from django.shortcuts import get_object_or_404

# Create your views here.
def index(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')

#Form view for users to sign up to the site
def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)

                #Get the person that is registering's IP address to get location
                #information
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')

                #Gets the user's location information when not in the test
                #enviornment
                if ip != '127.0.0.1':
                    geo = GeoIP2()
                    user_location = geo.city(ip)
                    user.profile.country = user_location["country_name"]
                    user.profile.city = user_location["city"]
                    user.profile.state = user_location["region"] #State the user is in
                    user.profile.zipCode = user_location["postal_code"]

                    user.profile.save()

                return redirect('index')
        else:
            form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

#View for a user to see a list of their images
class ImageListView(LoginRequiredMixin, generic.ListView):
    model = Image
    context_object_name = 'images'
    template_name = "images/images.html"

    #Filters the list of images to only show those that belong to the current logged in user
    def get_queryset(self):
        return Image.objects.filter(owner=self.request.user)

#Detail view of a image only the owner can see
class ImageDetailView(LoginRequiredMixin, generic.DetailView):
    model = Image
    template_name = "images/image_detail.html"

    #Checks to ensure that only the user that created the image can view the detail view
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != self.request.user:
            return redirect('index')
        return super(ImageDetailView, self).dispatch(request, *args, **kwargs)

#Form view to upload an image to the site
@login_required(login_url='/accounts/login/')
def add_image(request):
    if request.method == 'POST':
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            created_image = form.save()

            clean_tags = form.cleaned_data.get('tags')
            for tag in clean_tags:
                created_image.tags.add(tag)

            created_image.owner = request.user
            created_image.save()
            return redirect('images')
    else:
        form = AddImageForm()
    return render(request, 'images/add_image.html', {'form': form})

#View for a user to edit an image, but only the name and the tags
class ImageEditView(LoginRequiredMixin, generic.UpdateView):
    model = Image
    form_class = EditImageForm
    template_name = "images/edit_image.html"

    #Checks to make sure owner of image is editing, redirects otherwise
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != self.request.user:
            return redirect('index')
        return super(ImageEditView, self).dispatch(request, *args, **kwargs)

#View for a user to delete an image that they own
class ImageDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Image
    success_url = reverse_lazy('images')
    template_name = "images/image_delete.html"
    context_object_name = 'image'

    #Checks to make sure owner of image clicked to delete, redirects otherwise
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != self.request.user:
            return redirect('index')
        return super(ImageDeleteView, self).dispatch(request, *args, **kwargs)

    #Check to see if any items contain the image before deleting
    def delete(self, request, *args, **kwargs):
       self.object = self.get_object()
       items = Item.objects.filter(images__pk=self.object.pk)
       if self.object.owner == self.request.user:
           if items:
               #Image is related to items
               #Check to see if image is related to unowned items only
               if items.filter(owner=self.request.user).exists() != True:
                   #Soft delete the image
                   self.object.owner = None
                   self.object.save()

                   return HttpResponseRedirect(self.get_success_url())
               elif items.filter(owner=self.request.user).exists():
                   #Image is referenced in item user owns, do not allow deletion
                   raise Http404("This item is referenced in items you own. " +
                    "Deleted the related items first to delete this image.")

               return HttpResponseRedirect(self.get_success_url())
           else:
              #Image is not related to items, delete it
              self.object.delete()
              return HttpResponseRedirect(self.get_success_url())
       else:
           return redirect('index')

#View for a user to see a list of items they created
class ItemListView(LoginRequiredMixin, generic.ListView):
    model = Item
    context_object_name = 'items'
    template_name = "items/items.html"
    paginate_by = 20

    #Filters the list of items to only show those that belong to the current logged in user
    def get_queryset(self):
        return Item.objects.filter(owner=self.request.user).order_by('id')

#Detail view for an item only the owner can see
class ItemDetailView(LoginRequiredMixin, generic.DetailView):
    model = Item
    template_name = "items/item_detail.html"

#Form view to create an item for listings, offers and wish lists
@login_required(login_url='/accounts/login/')
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(data=request.POST, user=request.user)
        if form.is_valid():
            created_item = form.save()

            clean_images = form.cleaned_data.get('images')
            for image in clean_images:
                created_item.images.add(image)

            created_item.owner = request.user
            created_item.save()
            return redirect('items')
    else:
        form = ItemForm(user=request.user)
    return render(request, 'items/add_item.html', {'form': form})

#Form view to edit an item
@login_required(login_url='/accounts/login/')
def edit_item(request, pk):
    #Get the listing offer to be relisted
    current_item = get_object_or_404(Item, pk=pk)

    #Check if the owner of item is editing the item
    if current_item.owner == request.user:
        if request.method == 'POST':
            form = ItemForm(data=request.POST, user=request.user, instance=current_item)
            if form.is_valid():
                edited_item = form.save(commit=False)

                #Clear the existing images
                edited_item.images.clear()

                #Add the new items from the form
                clean_images = form.cleaned_data.get('images')
                for image in clean_images:
                    edited_item.images.add(image)

                edited_item.save()
                return redirect('item-detail', pk=current_item.pk)
        else:
            form = ItemForm(user=request.user, instance=current_item)
        return render(request, 'items/edit_item.html', {'form': form})
    else:
        return redirect('index')

#View for a user to delete an item that they own
class ItemDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Item
    success_url = reverse_lazy('items')
    template_name = "items/item_delete.html"
    context_object_name = 'item'

    #Checks to make sure owner of listing clicked to delete, redirects otherwise
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != self.request.user:
            return redirect('index')
        return super(ItemDeleteView, self).dispatch(request, *args, **kwargs)

    #Get listings that contain item to be deleted and delete them if they
    #contain the item, unless offer listing or auction listing is completed
    #if so soft delete those listings.  If an offer is accepted, also
    #soft delete
    def delete(self, request, *args, **kwargs):
       self.object = self.get_object()
       offer_listings = OfferListing.objects.filter(owner=self.object.owner,
            items__pk=self.object.pk)
       auction_listings = AuctionListing.objects.filter(owner=self.object.owner,
            items__pk=self.object.pk)
       wishlist_listings = WishlistListing.objects.filter(owner=self.object.owner,
            items__pk=self.object.pk)
       offers = Offer.objects.filter(owner=self.object.owner,
            items__pk=self.object.pk)
       if self.object.owner == self.request.user:
           if (offer_listings or auction_listings or wishlist_listings
                or offers):
                #Go through all listings and offers
                #Delete any inactive listings that contain the item
                #Delete any active listings that contain the item if no offers
                #or bids.
                #Delete all wishlist listings that contain the item
                #Delete all offers that have not been accepted that contain the
                #item
                #If there are and completed listings or offers, soft delete
                #the item
                soft_delete = False

                #If item is in user's wishlist, simply remove it
                if Wishlist.objects.filter(owner=self.object.owner).exists():
                    wishlist = Wishlist.objects.get(owner=self.object.owner)
                    if self.object in wishlist.items.all():
                        wishlist.items.remove(self.object)

                #Check to see if any active offer listings have offers.
                #If so, don't allow deletion
                if offer_listings:
                    if Offer.objects.filter(
                            offerListing__in=[listing.id for listing in
                                offer_listings if listing.listingEnded == False]
                        ).exists():
                            raise Http404("This item is offered in a listing" +
                            " that currently has offers.  Reject the current" +
                            " offers to delete this item.")

                #Check to see if there are any active auction listings.
                #If so, don't allow deletion
                if auction_listings:
                    if AuctionListing.objects.filter(
                            id__in=[listing.id for listing in
                                auction_listings if listing.listingEnded == False]
                        ).exists():
                            raise Http404("This item is offered in at least " +
                                " one active auction.  This item cannot be" +
                                " deleted.")

                #There are no active listings with offers or bids
                #For offer listings, check if any of the listings have been completed
                if offer_listings:
                    if offer_listings.filter(listingCompleted=True).exists():
                        #There are completed listings, item should be soft deleted
                        soft_delete = True

                        #Delete all the active and inactive listings that have not
                        #been completed
                        non_completed_offer_listings = offer_listings.filter(
                            listingCompleted=False)
                        if non_completed_offer_listings:
                            for listing in non_completed_offer_listings:
                                listing.delete()

                    else:
                        #There are no completed listings, delete the listings
                        for listing in offer_listings:
                            listing.delete()

                #For auction listings, check if any of the listings have been completed
                #All listings should be expired
                if auction_listings:
                    if Bid.objects.filter(
                        auctionListing__in=[listing.id for listing in
                            auction_listings]).exists():
                        #There are completed listings, item should be soft deleted
                        soft_delete = True

                        #Delete all inactive listings that were not bid on
                        for listing in auction_listings:
                            if listing.bids.count() == 0:
                                listing.delete()

                    else:
                        #There are no completed listings, delete the listings
                        for listing in auction_listings:
                            listing.delete()

                #Delete all wishlist listings
                if wishlist_listings:
                    for listing in wishlist_listings:
                        listing.delete()

                #Check if any offers have been accepted
                if offers:
                    if offers.filter(offerAccepted=True).exists():
                        #There are accepted offers, item should be soft deleted
                        soft_delete = True

                    #Delete all offers that were not accepted
                    for offer in offers:
                        if offer.offerAccepted != True:
                            offer.delete()

                if soft_delete:
                    self.object.owner = None
                    self.object.save()
                else:
                    #Delete the item and any related images if they are not
                    #related to any other items
                    for image in self.object.images.all():
                        if (image.owner == None
                            and Item.objects.filter(images__pk=image.pk).exclude(
                                id=self.object.id).exists() != True):
                            image.delete()

                    self.object.delete()

                return HttpResponseRedirect(self.get_success_url())
           else:
                #Item has no relationships, delete it
                #Delete any images that have no owner and are not related to
                #any other item
                for image in self.object.images.all():
                    if (image.owner == None
                        and Item.objects.filter(images__pk=image.pk).exclude(
                            id=self.object.id).exists() != True):
                        image.delete()

                self.object.delete()
                return HttpResponseRedirect(self.get_success_url())
       else:
           return redirect('index')

#Index page for FAQs
@login_required(login_url='/accounts/login/')
def faq(request):
    # Render the HTML template faq/documents.html with the data in the context variable
    return render(request, 'faq/documents.html')

#FAQ page for images
@login_required(login_url='/accounts/login/')
def faq_images(request):
    # Render the HTML template faq/images.html with the data in the context variable
    return render(request, 'faq/images.html')

#FAQ page for items
@login_required(login_url='/accounts/login/')
def faq_items(request):
    # Render the HTML template faq/items.html with the data in the context variable
    return render(request, 'faq/items.html')

#FAQ page for listings
@login_required(login_url='/accounts/login/')
def faq_listings(request):
    # Render the HTML template faq/listings.html with the data in the context variable
    return render(request, 'faq/listings.html')

#FAQ page for events
@login_required(login_url='/accounts/login/')
def faq_events(request):
    # Render the HTML template faq/events.html with the data in the context variable
    return render(request, 'faq/events.html')

#FAQ page for wishlists
@login_required(login_url='/accounts/login/')
def faq_wishlists(request):
    # Render the HTML template faq/wishlists.html with the data in the context variable
    return render(request, 'faq/wishlists.html')

#FAQ page for profiles
@login_required(login_url='/accounts/login/')
def faq_profiles(request):
    # Render the HTML template faq/profiles.html with the data in the context variable
    return render(request, 'faq/profiles.html')

#FAQ page for accounts
@login_required(login_url='/accounts/login/')
def faq_accounts(request):
    # Render the HTML template faq/accounts.html with the data in the context variable
    return render(request, 'faq/accounts.html')

#FAQ page for conversations
@login_required(login_url='/accounts/login/')
def faq_conversations(request):
    # Render the HTML template faq/conversations.html with the data in the context variable
    return render(request, 'faq/conversations.html')

#FAQ page for receipts
@login_required(login_url='/accounts/login/')
def faq_receipts(request):
    # Render the HTML template faq/receipts.html with the data in the context variable
    return render(request, 'faq/receipts.html')

#List view for a user to see all of the offer listings they have
class OfferListingListView(LoginRequiredMixin, generic.ListView):
    model = OfferListing
    context_object_name = 'offerlistings'
    template_name = "listings/offer_listings.html"
    paginate_by = 10

    #Filters the list of offer listings to only show those that belong to the current logged in user
    def get_queryset(self):
        return OfferListing.objects.filter(owner=self.request.user).order_by('endTime').reverse().annotate(offer_count=Count('offerlisting'))

#Detailed view for all users to see a offer listing (need to add offers for the owner to see later)
class OfferListingDetailView(LoginRequiredMixin, generic.DetailView):
    model = OfferListing
    context_object_name = 'offerlisting'
    template_name = "listings/offer_listing_detail.html"

    #Receive the offers made on the listing for the owner to view
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()

        context['offers'] = Offer.objects.filter(offerListing=obj)

        return context

    #Checks to ensure that only the user that created the listing and user that made offer
    # can view the listing when it has been completed
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        #listing = OfferListing.objects.get(id=obj.offerListing.id)
        if obj.listingCompleted:
            accepted_offer = Offer.objects.get(offerListing = obj) #There will only be one offer associted with listing
            if obj.owner == self.request.user:
                return super(OfferListingDetailView, self).dispatch(request, *args, **kwargs)
            elif accepted_offer.owner == self.request.user:
                return super(OfferListingDetailView, self).dispatch(request, *args, **kwargs)
            else:
                return redirect('index')
        else:
            return super(OfferListingDetailView, self).dispatch(request, *args, **kwargs)

#List view for a user to see all of the offer listings that are active on site
class AllOfferListingsListView(LoginRequiredMixin, generic.ListView):
    model = OfferListing
    context_object_name = 'offerlistings'
    template_name = "listings/all_offer_listings.html"
    paginate_by = 10

    #Filters the list of offer listings to only show those that have not
    #ended yet
    def get_queryset(self):
        listings_ids = [listing.id for listing in OfferListing.objects.all() if listing.listingEnded == False
            and listing.listingCompleted == False]
        queryset = OfferListing.objects.filter(id__in=listings_ids).order_by('id').reverse()

        current_date = timezone.localtime(timezone.now())

        for obj in queryset:
            time_left = obj.endTime - current_date
            if time_left.total_seconds() <= 1800:
                obj.endingSoon = True
            else:
                obj.endingSoon = False

        return queryset

#View for a user to see a list of offers they have made
class MyOffersListView(LoginRequiredMixin, generic.ListView):
    model = Offer
    context_object_name = 'offers'
    template_name = "listings/offers.html"
    paginate_by = 10

    #Filters the list of offers to only show those that belong to the current logged in user
    def get_queryset(self):
        offer_ids = [offer.id for offer in Offer.objects.all() if offer.offerListing.listingEnded == False or
            offer.offerListing.listingCompleted and offer.offerAccepted]
        return Offer.objects.filter(id__in=offer_ids, owner=self.request.user).order_by('id')

#Form view to create an offer listing
@login_required(login_url='/accounts/login/')
def create_offer_listing(request):
    if request.method == 'POST':
        form = OfferListingForm(data=request.POST, user=request.user)
        if form.is_valid():
            created_listing = form.save()

            #Get the end time choice from form and set end time accordingly
            clean_choice = form.cleaned_data.get('endTimeChoices')
            if clean_choice == '1h':
                #Set end time to 1 hour from current time if choice was 1h
                date = timezone.localtime(timezone.now()) + timedelta(hours=1)
            elif clean_choice == '2h':
                #Set end time to 2 hours from current time if choice was 2h
                date = timezone.localtime(timezone.now()) + timedelta(hours=2)
            elif clean_choice == '4h':
                #Set end time to 4 hours from current time if choice was 4h
                date = timezone.localtime(timezone.now()) + timedelta(hours=4)
            elif clean_choice == '8h':
                #Set end time to 8 hours from current time if choice was 8h
                date = timezone.localtime(timezone.now()) + timedelta(hours=8)
            elif clean_choice == '12h':
                #Set end time to 12 hours from current time if choice was 12h
                date = timezone.localtime(timezone.now()) + timedelta(hours=12)
            elif clean_choice == '1d':
                #Set end time to 1 day from current time if choice was 1d
                date = timezone.localtime(timezone.now()) + timedelta(days=1)
            elif clean_choice == '3d':
                #Set end time to 3 days from current time if choice was 3ds
                date = timezone.localtime(timezone.now()) + timedelta(days=3)
            elif clean_choice == '7d':
                #Set end time to 7 days from current time
                date = timezone.localtime(timezone.now()) + timedelta(days=7)

            #Get openToMoneyOffers value from form
            clean_openToMoneyOffers = form.cleaned_data.get('openToMoneyOffers')

            #Check to see if option was checked or not
            if clean_openToMoneyOffers == True:
                #If true, check if the user added a maxRange to form
                clean_maxRange = form.cleaned_data.get('maxRange')
                if clean_maxRange:
                    #If so, keep the value the same
                    created_listing.maxRange = clean_maxRange
                else:
                    #If not, set it to 0.00
                    created_listing.maxRange = 0.00
            else:
                #If not checked, set ranges to 0.00
                created_listing.minRange = 0.00
                created_listing.maxRange = 0.00

            created_listing.endTime = date
            created_listing.owner = request.user

            clean_items = form.cleaned_data.get('items')
            for item in clean_items:
                created_listing.items.add(item)

            created_listing.save()

            #Set owner for receipt if it was created sucessfully
            if created_listing.receipt:
                receipt = Receipt.objects.get(listing=created_listing)
                receipt.owner = request.user
                receipt.save()

            #Create an ending notification for listing that will be active
            #when the listing ends
            content = ('Your listing "' + created_listing.name
                + '" has expired.')
            ListingNotification.objects.create(user=request.user,
                listing=created_listing, content=content,
                creationDate=created_listing.endTime,
                type="Listing Ended")

            return redirect('offer-listings')
    else:
        form = OfferListingForm(user=request.user)
    return render(request, 'listings/create_offer_listing.html', {'form': form})

#Form view for editing an offer listing without changing the end time
@login_required(login_url='/accounts/login/')
def update_offer_listing(request, pk):
    #Get the listing offer to be updated
    current_listing = get_object_or_404(OfferListing, pk=pk)
    existing_objects = Offer.objects.filter(offerListing=current_listing).exists()

    if request.user == current_listing.owner:
        if current_listing.listingCompleted != True and current_listing.listingEnded != True and existing_objects != True:
            if request.method == 'POST':
                form = UpdateOfferListingForm(data=request.POST, user=request.user, instance=current_listing)
                if form.is_valid():
                    current_listing = form.save(commit=False)

                    #Get openToMoneyOffers value from form
                    clean_openToMoneyOffers = form.cleaned_data.get('openToMoneyOffers')

                    #Check to see if option was checked or not
                    if clean_openToMoneyOffers == True:
                        #If true, check if the user added a maxRange to form
                        clean_maxRange = form.cleaned_data.get('maxRange')
                        if clean_maxRange:
                            #If so, keep the value the same
                            current_listing.maxRange = clean_maxRange
                        else:
                            #If not, set it to 0.00
                            current_listing.maxRange = 0.00
                    else:
                        #If not checked, set ranges to 0.00
                        current_listing.minRange = 0.00
                        current_listing.maxRange = 0.00

                    #Clear the current items from the listing
                    current_listing.items.clear()

                    #Add the newly added items to the listing
                    clean_items = form.cleaned_data.get('items')
                    for item in clean_items:
                        current_listing.items.add(item)

                    current_listing.save()
                    return redirect('offer-listing-detail', pk=current_listing.pk)
            else:
                form = UpdateOfferListingForm(user=request.user, instance=current_listing)
            return render(request, 'listings/update_offer_listing.html', {'form': form})
        else:
            return redirect('offer-listings')
    else:
        return redirect('index')

#Form view for relisting an offer listing
@login_required(login_url='/accounts/login/')
def relist_offer_listing(request, pk):
    #Get the listing offer to be relisted
    current_listing = get_object_or_404(OfferListing, pk=pk)
    existing_offers = Offer.objects.filter(offerListing=current_listing)

    if request.user == current_listing.owner:
        if current_listing.listingEnded and current_listing.listingCompleted != True:
            if request.method == 'POST':
                form = OfferListingForm(data=request.POST, user=request.user, instance=current_listing)
                if form.is_valid():
                    #Retrieve the old notification for the listing ending
                    #so it can be updated
                    notifications = ListingNotification.objects.filter(listing=current_listing)
                    old_notification = notifications.first()

                    current_listing = form.save(commit=False)

                    #Delete the previous existing offers
                    for offer in existing_offers:
                        notifications = OfferNotification.objects.filter(offer=offer)
                        if notifications:
                            content_to_search_for = (offer.owner.username +
                                ' has placed an offer on your listing "' +
                                offer.offerListing.name + '".')
                            for notification in notifications:
                                #Will ensure that rejection and listing expired
                                #notifications remain for the offer after it's
                                #deleted
                                if notification.content == content_to_search_for:
                                    notification.delete()

                        offer.delete()
                    #existing_offers.delete()

                    #Get openToMoneyOffers value from form
                    clean_openToMoneyOffers = form.cleaned_data.get('openToMoneyOffers')

                    #Check to see if option was checked or not
                    if clean_openToMoneyOffers == True:
                        #If true, check if the user added a maxRange to form
                        clean_maxRange = form.cleaned_data.get('maxRange')
                        if clean_maxRange:
                            #If so, keep the value the same
                            current_listing.maxRange = clean_maxRange
                        else:
                            #If not, set it to 0.00
                            current_listing.maxRange = 0.00
                    else:
                        #If not checked, set ranges to 0.00
                        current_listing.minRange = 0.00
                        current_listing.maxRange = 0.00

                    #Clear the current items from the listing
                    current_listing.items.clear()

                    #Add the newly added items to the listing
                    clean_items = form.cleaned_data.get('items')
                    for item in clean_items:
                        current_listing.items.add(item)

                    #Get the end time choice from form and set end time accordingly
                    clean_choice = form.cleaned_data.get('endTimeChoices')
                    if clean_choice == '1h':
                        #Set end time to 1 hour from current time if choice was 1h
                        date = timezone.localtime(timezone.now()) + timedelta(hours=1)
                    elif clean_choice == '2h':
                        #Set end time to 2 hours from current time if choice was 2h
                        date = timezone.localtime(timezone.now()) + timedelta(hours=2)
                    elif clean_choice == '4h':
                        #Set end time to 4 hours from current time if choice was 4h
                        date = timezone.localtime(timezone.now()) + timedelta(hours=4)
                    elif clean_choice == '8h':
                        #Set end time to 8 hours from current time if choice was 8h
                        date = timezone.localtime(timezone.now()) + timedelta(hours=8)
                    elif clean_choice == '12h':
                        #Set end time to 12 hours from current time if choice was 12h
                        date = timezone.localtime(timezone.now()) + timedelta(hours=12)
                    elif clean_choice == '1d':
                        #Set end time to 1 day from current time if choice was 1d
                        date = timezone.localtime(timezone.now()) + timedelta(days=1)
                    elif clean_choice == '3d':
                        #Set end time to 3 days from current time if choice was 3ds
                        date = timezone.localtime(timezone.now()) + timedelta(days=3)
                    else:
                        #Set end time to 7 days from current time
                        date = timezone.localtime(timezone.now()) + timedelta(days=7)

                    #Set the end date for the listing
                    current_listing.endTime = date

                    current_listing.save()

                    #Update the ending notification
                    old_notification.creationDate = current_listing.endTime
                    old_notification.save()

                    return redirect('offer-listing-detail', pk=current_listing.pk)
            else:
                form = OfferListingForm(user=request.user, instance=current_listing)
            return render(request, 'listings/relist_offer_listing.html', {'form': form})
        else:
            return redirect('offer-listings')
    else:
        return redirect('index')

#View for a user to delete an offer listing that they own
class OfferListingDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = OfferListing
    success_url = reverse_lazy('offer-listings')
    template_name = "listings/offer_listing_delete.html"
    context_object_name = 'offerlisting'

    #Checks to make sure owner of listing clicked to delete, redirects otherwise
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != self.request.user:
            return redirect('index')
        return super(OfferListingDeleteView, self).dispatch(request, *args, **kwargs)

    #Checks to make sure listing is not active before deleting
    def delete(self, request, *args, **kwargs):
       self.object = self.get_object()

       if self.object.owner == self.request.user:
            if self.object.listingEnded != True:
                #Listing is still active, only allow user to delete if there
                #are no offers
                if Offer.objects.filter(offerListing=self.object).exists():
                    raise Http404(("This listing cannot be deleted, reject " +
                        "all current offers to delete it."))
                else:
                    #Allow the user to delete the listing if there are no offers

                    #Go through items and delete any that don't have an owner
                    #and are not related to any other listing/offer
                    for item in self.object.items.all():
                        if (item.owner == None
                            and Listing.objects.filter(items__pk=item.pk).exclude(
                                id=self.object.id).exists() != True
                            and Offer.objects.filter(items__pk=item.pk).exists()
                                != True
                            and Wishlist.objects.filter(items__pk=item.pk).exists()
                                != True):
                                #Go through images and delete any that don't have an owner
                                for image in item.images.all():
                                    if (image.owner == None
                                        and Item.objects.filter(images__pk=image.pk).exclude(
                                            id=item.id).exists() != True):
                                        image.delete()

                                item.delete()

                    self.object.delete()
                    return HttpResponseRedirect(self.get_success_url())
            else:
                #Listing has ended, soft deleted if listing was completed
                #Delete if listing was not completed
                if self.object.listingCompleted:
                    self.object.owner = None
                    self.object.save()

                    #Delete any notifications that were relevant to listing
                    notifications = ListingNotification.objects.filter(listing=self.object)
                    old_notification = notifications.first()
                    old_notification.delete()
                else:
                    #Go through items and delete any that don't have an owner
                    #and have no other relationships
                    for item in self.object.items.all():
                        if (item.owner == None
                            and Listing.objects.filter(items__pk=item.pk).exclude(
                                id=self.object.id).exists() != True
                            and Offer.objects.filter(items__pk=item.pk).exists()
                                != True
                            and Wishlist.objects.filter(items__pk=item.pk).exists()
                                != True):
                                #Go through images and delete any that don't have an owner
                                for image in item.images.all():
                                    if (image.owner == None
                                        and Item.objects.filter(images__pk=image.pk).exclude(
                                            id=item.id).exists() != True):
                                        image.delete()

                                item.delete()

                    #Delete offer notifications associated with listing and owner
                    offer_notifications = OfferNotification.objects.filter(
                        listing=self.object, user=self.request.user)
                    for notification in offer_notifications:
                        notification.delete()

                    self.object.delete()

                return HttpResponseRedirect(self.get_success_url())
       else:
           return redirect('index')

#Form for a user to view all of their active auctions (need to come back to this
#once listings are able to end)
class AuctionListingListView(LoginRequiredMixin, generic.ListView):
    model = AuctionListing
    context_object_name = 'auctionlistings'
    template_name = "listings/auction_listings.html"
    paginate_by = 10

    #Filters the list of auction listings to only show those that belong to the
    #current logged in user along with bids
    def get_queryset(self):
        return AuctionListing.objects.filter(owner=self.request.user).order_by('endTime').reverse().annotate(bid_count=Count('bids'))

#Detailed view for all users to see an auction
class AuctionListingDetailView(LoginRequiredMixin, generic.DetailView):
    model = AuctionListing
    context_object_name = 'auctionlisting'
    template_name = "listings/auction_listing_detail.html"

    def get_last_bid(self):
        try:
            return self.bids.all().reverse()[0]
        except IndexError:
            pass

#List view for a user to see all of the auction listings that are active on site
class AllAuctionListingsListView(LoginRequiredMixin, generic.ListView):
    model = AuctionListing
    context_object_name = 'auctionlistings'
    template_name = "listings/all_auction_listings.html"
    paginate_by = 10

    #Filters the list of auction listings to only show those that have not
    #ended yet
    def get_queryset(self):
        listings_ids = [listing.id for listing in AuctionListing.objects.all() if listing.listingEnded == False]
        queryset = AuctionListing.objects.filter(id__in=listings_ids).order_by('id').reverse()

        current_date = timezone.localtime(timezone.now())

        for obj in queryset:
            time_left = obj.endTime - current_date
            if time_left.total_seconds() <= 1800:
                obj.endingSoon = True
            else:
                obj.endingSoon = False

        return queryset

#View for a user to see a list of bids they have made
class MyBidsListView(LoginRequiredMixin, generic.ListView):
    model = Bid
    context_object_name = 'bids'
    template_name = "listings/bids.html"
    paginate_by = 10

    #Filters the list of bids to only show those that belong to the current logged in user
    #Only gets the last bid user made for each listing
    def get_queryset(self):
        #Get all the auctions on site that have a bid related to current user
        auction_ids = [auction.id for auction in AuctionListing.objects.all() if
            auction.bids.filter(bidder=self.request.user).exists()]

        #Initiate an empty list of bids
        bid_ids = []

        #For each auction, get the last bid the user made on it and append to
        #list of bid ids
        for auction_id in auction_ids:
            auction = AuctionListing.objects.get(id=auction_id)
            latest_bid = Bid.objects.filter(auctionListing=auction, bidder=self.request.user).last()
            bid_ids.append(latest_bid.id)

        #bid_ids = [bid.id for bid in Bid.objects.all() if bid.auctionListing.listingEnded == False or
            #bid.auctionListing.listingEnded and bid.winningBid]
        return Bid.objects.filter(id__in=bid_ids).order_by('id')

#Form view for creating an auction listing
@login_required(login_url='/accounts/login/')
def create_auction_listing(request):
    if request.method == 'POST':
        form = AuctionListingForm(data=request.POST, user=request.user)
        if form.is_valid():
            created_listing = form.save()

            #Get the end time choice from form and set end time accordingly
            clean_choice = form.cleaned_data.get('endTimeChoices')
            if clean_choice == '1h':
                #Set end time to 1 hour from current time if choice was 1h
                date = timezone.localtime(timezone.now()) + timedelta(hours=1)
            elif clean_choice == '2h':
                #Set end time to 2 hours from current time if choice was 2h
                date = timezone.localtime(timezone.now()) + timedelta(hours=2)
            elif clean_choice == '4h':
                #Set end time to 4 hours from current time if choice was 4h
                date = timezone.localtime(timezone.now()) + timedelta(hours=4)
            elif clean_choice == '8h':
                #Set end time to 8 hours from current time if choice was 8h
                date = timezone.localtime(timezone.now()) + timedelta(hours=8)
            elif clean_choice == '12h':
                #Set end time to 12 hours from current time if choice was 12h
                date = timezone.localtime(timezone.now()) + timedelta(hours=12)
            elif clean_choice == '1d':
                #Set end time to 1 day from current time if choice was 1d
                date = timezone.localtime(timezone.now()) + timedelta(days=1)
            elif clean_choice == '3d':
                #Set end time to 3 days from current time if choice was 3ds
                date = timezone.localtime(timezone.now()) + timedelta(days=3)
            else:
                #Set end time to 7 days from current time
                date = timezone.localtime(timezone.now()) + timedelta(days=7)

            #Get autobuy value from the form
            clean_autobuy = form.cleaned_data.get('autobuy')

            #Check to see if user filled in autobuy field
            if clean_autobuy:
                #If filled in, keep the original value
                created_listing.autobuy = clean_autobuy
            else:
                #If not filled in, set it to 0.00
                created_listing.autobuy = 0.00

            created_listing.endTime = date
            created_listing.owner = request.user
            created_listing.save()

            #Set owner for receipt if it was created sucessfully
            if created_listing.receipt:
                receipt = Receipt.objects.get(listing=created_listing)
                receipt.owner = request.user
                receipt.save()

            #Create an ending notification for listing that will be active
            #when the listing ends
            content = ('Your listing "' + created_listing.name
                + '" has expired.')
            ListingNotification.objects.create(user=request.user,
                listing=created_listing, content=content,
                creationDate=created_listing.endTime,
                type="Listing Ended")

            return redirect('auction-listings')
    else:
        form = AuctionListingForm(user=request.user)
    return render(request, 'listings/create_auction_listing.html', {'form': form})

#Form view for relisting an auction listing
@login_required(login_url='/accounts/login/')
def relist_auction_listing(request, pk):
    #Get the listing to be relisted
    current_listing = get_object_or_404(AuctionListing, pk=pk)

    if current_listing.owner == request.user:
        if current_listing.listingEnded and current_listing.bids.count() == 0:
            if request.method == 'POST':
                form = AuctionListingForm(data=request.POST, user=request.user, instance=current_listing)
                if form.is_valid():
                    #Retrieve the old notification for the listing ending
                    #so it can be updated
                    notifications = ListingNotification.objects.filter(listing=current_listing)
                    old_notification = notifications.first()

                    current_listing = form.save(commit=False)

                    #Clear the current items from the listing
                    current_listing.items.clear()

                    #Add the newly added items to the listing
                    clean_items = form.cleaned_data.get('items')
                    for item in clean_items:
                        current_listing.items.add(item)

                    #Get the end time choice from form and set end time accordingly
                    clean_choice = form.cleaned_data.get('endTimeChoices')
                    if clean_choice == '1h':
                        #Set end time to 1 hour from current time if choice was 1h
                        date = timezone.localtime(timezone.now()) + timedelta(hours=1)
                    elif clean_choice == '2h':
                        #Set end time to 2 hours from current time if choice was 2h
                        date = timezone.localtime(timezone.now()) + timedelta(hours=2)
                    elif clean_choice == '4h':
                        #Set end time to 4 hours from current time if choice was 4h
                        date = timezone.localtime(timezone.now()) + timedelta(hours=4)
                    elif clean_choice == '8h':
                        #Set end time to 8 hours from current time if choice was 8h
                        date = timezone.localtime(timezone.now()) + timedelta(hours=8)
                    elif clean_choice == '12h':
                        #Set end time to 12 hours from current time if choice was 12h
                        date = timezone.localtime(timezone.now()) + timedelta(hours=12)
                    elif clean_choice == '1d':
                        #Set end time to 1 day from current time if choice was 1d
                        date = timezone.localtime(timezone.now()) + timedelta(days=1)
                    elif clean_choice == '3d':
                        #Set end time to 3 days from current time if choice was 3ds
                        date = timezone.localtime(timezone.now()) + timedelta(days=3)
                    else:
                        #Set end time to 7 days from current time
                        date = timezone.localtime(timezone.now()) + timedelta(days=7)

                    #Set the end date for the listing
                    current_listing.endTime = date

                    #Get autobuy value from the form
                    clean_autobuy = form.cleaned_data.get('autobuy')

                    #Check to see if user filled in autobuy field
                    if clean_autobuy:
                        #If filled in, keep the original value
                        current_listing.autobuy = clean_autobuy
                    else:
                        #If not filled in, set it to 0.00
                        current_listing.autobuy = 0.00

                    current_listing.save()

                    #Update the ending notification
                    old_notification.creationDate = current_listing.endTime
                    old_notification.save()

                    return redirect('auction-listing-detail', pk=current_listing.pk)
            else:
                form = AuctionListingForm(user=request.user, instance=current_listing)
            return render(request, 'listings/relist_auction_listing.html', {'form': form})
        else:
            return redirect('auction-listings')
    else:
        return redirect('index')

#Detailed view for listing owner and offerer to see a offer
class OfferDetailView(LoginRequiredMixin, generic.DetailView):
    model = Offer
    context_object_name = 'offer'
    template_name = "listings/offer_detail.html"

    #Checks to ensure that only the user that created the listing and user that made offer
    # can view the detail view
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        listing = OfferListing.objects.get(id=obj.offerListing.id)
        if obj.owner == self.request.user:
            return super(OfferDetailView, self).dispatch(request, *args, **kwargs)
        elif listing.owner == self.request.user:
            return super(OfferDetailView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('index')

#Form view for creating an offer for an offer listing
@login_required(login_url='/accounts/login/')
def create_offer(request, pk):
    #Get the listing object the offer is being created for
    current_listing = get_object_or_404(OfferListing, pk=pk)

    #Check to ensure listing is still active
    if current_listing.listingEnded or current_listing.listingCompleted:
        return redirect('index')
    else:
        #Check to ensure the listing owner cant create an offer for their own listing
        if request.user != current_listing.owner:
            if request.method == 'POST':
                form = OfferForm(data=request.POST, user=request.user, instance=current_listing, initial={'offerListing': current_listing})
                if form.is_valid():
                    created_offer = form.save()

                    #Add the items submitted to the offer
                    clean_items = form.cleaned_data.get('items')
                    for item in clean_items:
                        created_offer.items.add(item)

                    created_offer.owner = request.user
                    created_offer.save()

                    #Create an end notification for the offer if listing owner
                    #does not select an offer before listing ends
                    content = ('Your offer on the listing "' + created_offer.offerListing.name
                        + '" has expired.')
                    OfferNotification.objects.create(
                        listing=created_offer.offerListing, offer=created_offer,
                        user=created_offer.owner, content=content,
                        creationDate=created_offer.offerListing.endTime,
                        type="Listing Expired")

                    #Create a notification for the listing owner that an offer
                    #has been made
                    content = (created_offer.owner.username + ' has placed an offer ' +
                    'on your listing "' + created_offer.offerListing.name + '".')
                    OfferNotification.objects.create(
                        listing=created_offer.offerListing, offer=created_offer,
                        user=created_offer.offerListing.owner,
                        content=content,
                        creationDate=timezone.localtime(timezone.now()),
                        type="Offer Made")

                    return redirect('offer-detail', pk=created_offer.pk)
            else:
                form = OfferForm(user=request.user, instance=current_listing, initial={'offerListing': current_listing})
            return render(request, 'listings/create_offer.html', {'form': form})
        else:
            return redirect('index')

#Form view for editing an offer a user owns
@login_required(login_url='/accounts/login/')
def edit_offer(request, pk):
    #Get the offer object to be edited
    current_offer = get_object_or_404(Offer, pk=pk)

    #Check to ensure listing is still active before editing
    if current_offer.offerListing.listingEnded or current_offer.offerListing.listingCompleted:
        return redirect('offer-detail', pk=current_offer.pk)
    else:
        #Check to ensure that the owner of the offer is editing it
        if request.user == current_offer.owner:
            if request.method == 'POST':
                form = EditOfferForm(data=request.POST, user=request.user, instance=current_offer,
                    listing=current_offer.offerListing)
                if form.is_valid():
                    edited_offer = form.save(commit=False)

                    #Clear the offer's current items
                    edited_offer.items.clear()

                    #Add the items submitted to the offer
                    clean_items = form.cleaned_data.get('items')
                    for item in clean_items:
                        edited_offer.items.add(item)

                    edited_offer.save()

                    #Create notification to notify the offer listing owner that
                    #an offer was updated
                    content = (edited_offer.owner.username + 'has updated an ' +
                         'offer on the listing "' + edited_offer.offerListing.name
                        + '".')
                    OfferNotification.objects.create(
                        listing=edited_offer.offerListing,
                        user=edited_offer.offerListing.owner, content=content,
                        creationDate=timezone.localtime(timezone.now()),
                        type="Offer Updated")

                    return redirect('offer-detail', pk=edited_offer.pk)
            else:
                form = EditOfferForm(user=request.user, instance=current_offer, listing=current_offer.offerListing)
            return render(request, 'listings/offer_edit.html', {'form': form})
        else:
            return redirect('index')

#Method for accepting an offer on a listing, done by listing owner
def accept_offer(request, pk):
    current_offer = get_object_or_404(Offer, pk=pk)

    if request.user:
        if request.user != current_offer.offerListing.owner:
            return redirect('index')
        elif current_offer.offerListing.listingEnded or current_offer.offerListing.listingCompleted:
            return redirect('offer-listing-detail', pk=current_offer.offerListing.pk)
        else:
            #Update the offer's offerAccepted field to True and save the object
            current_offer.offerAccepted = True
            current_offer.save()

            #Retrieve the listing the offer is associated with, change listingCompleted to True
            current_listing = OfferListing.objects.get(id=current_offer.offerListing.id)
            current_listing.listingCompleted = True

            #Retrieve the old notification for the listing ending do it can
            #be deleted
            notifications = ListingNotification.objects.filter(listing=current_listing)
            old_notification = notifications.first()
            old_notification.delete()

            #Delete current offer notifications for the listing
            offer_notifications = OfferNotification.objects.filter(listing=current_listing)
            for notification in offer_notifications:
                notification.delete()

            #Create a notification for the accepted offer
            content = (current_listing.owner.username + 'has accepted your' +
                ' offer on the listing "' + current_listing.name + '".')
            OfferNotification.objects.create(listing=current_listing,
                offer=current_offer, user=current_offer.owner,
                content=content, creationDate=timezone.localtime(timezone.now()),
                type="Offer Accepted")

            #Set endTime for listing to current date and time so that it ends after accepting offer
            date = timezone.localtime(timezone.now())
            current_listing.endTime = date
            current_listing.save()

            #Retrieve the other offers for the listing and destroy them if not accepted
            other_offers = Offer.objects.filter(offerListing=current_listing)
            users = []
            for offer in other_offers:
                if offer.offerAccepted != True:
                    #Create a notification for the user that a dfferent offer was
                    #accepted
                    if offer.owner not in users and offer.owner != current_offer.owner:
                        content = (current_listing.owner.username + 'has accepted a' +
                            ' different offer on the listing "' + current_listing.name + '".')
                        OfferNotification.objects.create(listing=current_listing,
                            user=offer.owner, content=content,
                            creationDate=timezone.localtime(timezone.now()),
                            type="Offer Rejected")
                        users.append(offer.owner)
                    #Destroy the object
                    offer.delete()

            #Update the listing's receipt
            receipt = Receipt.objects.get(listing=current_listing)
            receipt.exchangee = current_offer.owner
            receipt.save()

            #Redirect to the listing afterwards
            return redirect('offer-listing-detail', pk=current_offer.offerListing.pk)
    else:
        return redirect('index')

#View for a user to delete an offer that they own or is
class OfferDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Offer
    template_name = "listings/offer_delete.html"
    context_object_name = 'offer'

    #Checks to make sure owner of listing or owner of offer clicked to delete, redirects otherwise
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner == self.request.user:
            return super(OfferDeleteView, self).dispatch(request, *args, **kwargs)
        elif obj.offerListing.owner == self.request.user:
            if obj.offerAccepted:
                return redirect('offer-detail', pk=obj.pk)
            else:
                return super(OfferDeleteView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('index')

    #Checks to see if offer was accepted or not before deleting
    def delete(self, request, *args, **kwargs):
       self.object = self.get_object()
       listing = self.object.offerListing

       if self.object.owner == self.request.user:
           if self.object.offerAccepted:
               #Soft delete the offer
               self.object.owner = None
               self.object.save()
           elif self.object.offerAccepted != True:
               #Delete the offer

               #Go through items and delete any that don't have an owner
               for item in self.object.items.all():
                   if (item.owner == None
                       and Listing.objects.filter(items__pk=item.pk).exists()
                        != True
                       and Offer.objects.filter(items__pk=item.pk).exclude(
                           id=self.object.id).exists() != True
                       and Wishlist.objects.filter(items__pk=item.pk).exists()
                           != True):
                           #Go through images and delete any that don't have an owner
                           for image in item.images.all():
                               if (image.owner == None
                                   and Item.objects.filter(images__pk=image.pk).exclude(
                                       id=item.id).exists() != True):
                                   image.delete()

                           item.delete()

               #Delete ending notification related to the offer
               content = ('Your offer on the listing "' + self.object.offerListing.name
                   + '" has expired.')
               notification = OfferNotification.objects.filter(offer=self.object,
                    user=self.object.owner, content=content)
               notification.delete()

               #Create notification to notify the offer listing owner that
               #an offer was retracted
               content = (self.object.owner.username + 'has retracted an ' +
                    'offer on the listing "' + self.object.offerListing.name
                   + '".')
               OfferNotification.objects.create(
                   listing=self.object.offerListing,
                   user=self.object.offerListing.owner, content=content,
                   creationDate=timezone.localtime(timezone.now()),
                   type="Offer Retracted")

               self.object.delete()
           return HttpResponseRedirect(self.get_success_url(listing))
       elif self.object.offerListing.owner == self.request.user:
           if self.object.offerAccepted != True:
               #Delete the offer if it wasn't accepted

               #Go through items and delete any that don't have an owner
               for item in self.object.items.all():
                   if (item.owner == None
                       and Listing.objects.filter(items__pk=item.pk).exists()
                        != True
                       and Offer.objects.filter(items__pk=item.pk).exclude(
                           id=self.object.id).exists() != True
                       and Wishlist.objects.filter(items__pk=item.pk).exists()
                           != True):
                           #Go through images and delete any that don't have an owner
                           for image in item.images.all():
                               if (image.owner == None
                                   and Item.objects.filter(images__pk=image.pk).exclude(
                                       id=item.id).exists() != True):
                                   image.delete()

                           item.delete()

               #Delete ending notification related to the offer
               content = ('Your offer on the listing "' + self.object.offerListing.name
                   + '" has expired.')
               notification = OfferNotification.objects.filter(offer=self.object,
                    user=self.object.owner, content=content)
               notification.delete()

               #Create notification to notify the offer owner that their
               #offer was rejected
               content = (self.object.offerListing.owner.username + 'has ' +
                    'rejected your offer on the listing "' +
                    self.object.offerListing.name + '".')
               OfferNotification.objects.create(
                   listing=self.object.offerListing,
                   user=self.object.owner, content=content,
                   creationDate=timezone.localtime(timezone.now()),
                   type="Offer Rejected")

               self.object.delete()
               return HttpResponseRedirect(self.get_success_url(listing))
           else:
               raise Http404(("Only the owner that made this offer can delete it."))
       else:
           return redirect('index')

    #Returns offer listing owner to the offer listing, will return offer owner to their list of offers
    def get_success_url(self, listing):
        if listing.owner == self.request.user:
            return reverse_lazy('offer-listing-detail', kwargs={'pk': listing.pk})
        else:
            return reverse_lazy('my-offers')

#Form view for creating an bid for an auction listing
@login_required(login_url='/accounts/login/')
def create_bid(request, pk):
    #Get the listing object the bid is being created for
    current_listing = get_object_or_404(AuctionListing, pk=pk)

    previous_winning_bid = None

    #Get the previous winning bid
    if current_listing.bids.count() > 0:
        for bid in current_listing.bids.all():
            if bid.winningBid == True:
                previous_winning_bid = bid

    #Check to make sure listing is still active
    if current_listing.listingEnded:
        return redirect('index')
    else:
        #Check to ensure that the auction owner cannot bid on their own auction
        if request.user != current_listing.owner:
            if previous_winning_bid:
                if request.user != previous_winning_bid.bidder:
                    if request.method == 'POST':
                        form = CreateBidForm(data=request.POST, instance=current_listing, initial={'auctionListing': current_listing, 'bidder': request.user})
                        if form.is_valid():
                            created_bid = form.save()

                            #Set the bidder and auctionListing fields (not sure why they aren't saving with the form...)
                            created_bid.bidder = request.user
                            created_bid.auctionListing = current_listing

                            #End the auction if the bid amount matches autobuy price
                            bid_amount = form.cleaned_data.get('amount')
                            if current_listing.autobuy == bid_amount:
                                current_listing.endTime = timezone.localtime(timezone.now())
                                current_listing.save()

                            #Get the previous winning bid and change it to no longer be winning bid
                            previous_winning_bid.winningBid = False
                            previous_winning_bid.save()

                            #Set winning bid to be the current winning bid
                            created_bid.winningBid = True

                            created_bid.save()

                            #Create winning notifications for the current bid that will
                            #become visible when listing ends
                            bid = Bid.objects.get(id=created_bid.id)
                            content = ('Your bid of $' + str(bid.amount) +
                                ' won the listing "' + current_listing.name
                                + '".')
                            BidNotification.objects.create(
                                listing=current_listing, user=request.user,
                                bid=created_bid,
                                creationDate=current_listing.endTime,
                                content=content, type="Winning Bid")

                            content = ('Your listing "' + current_listing.name
                                + '" has ended with a winning bid of $' + str(bid.amount) + '.')
                            notifications = ListingNotification.objects.filter(listing=current_listing)
                            old_notification = notifications.first()
                            if current_listing.autobuy == bid_amount:
                                old_notification.creationDate = current_listing.endTime
                            old_notification.content = content
                            old_notification.type = "Listing Completed"
                            old_notification.save()

                            #Create a notification for the previous bidder
                            #to notify them they've been outbid
                            content = ('Your bid of $' + str(previous_winning_bid.amount) +
                                ' has been outbidded by a bid of $' + str(bid.amount)
                                + '.')
                            previous_bid_notification = BidNotification.objects.get(bid=previous_winning_bid)
                            previous_bid_notification.content = content
                            previous_bid_notification.creationDate = timezone.localtime(timezone.now())
                            previous_bid_notification.type = "Outbidded"
                            previous_bid_notification.save()

                            #Update the receipt for the listing
                            receipt = Receipt.objects.get(listing=current_listing)
                            receipt.exchangee = request.user
                            receipt.save()

                            print(receipt)

                            return redirect('auction-listing-detail', pk=current_listing.pk)
                    else:
                        form = CreateBidForm(instance=current_listing, initial={'auctionListing': current_listing, 'bidder': request.user})
                    return render(request, 'listings/create_bid.html', {'form': form})
                else:
                    return redirect('auction-listing-detail', pk=current_listing.pk)
            else:
                if request.method == 'POST':
                    form = CreateBidForm(data=request.POST, instance=current_listing, initial={'auctionListing': current_listing, 'bidder': request.user})
                    if form.is_valid():
                        created_bid = form.save()

                        #Set the bidder and auctionListing fields (not sure why they aren't saving with the form...)
                        created_bid.bidder = request.user
                        created_bid.auctionListing = current_listing

                        #End the auction if the bid amount matches autobuy price
                        bid_amount = form.cleaned_data.get('amount')
                        if current_listing.autobuy == bid_amount:
                            current_listing.endTime = timezone.localtime(timezone.now())
                            current_listing.save()

                        #Set winning bid to be the current winning bid
                        created_bid.winningBid = True

                        created_bid.save()

                        #Create winning notifications for the current bid that will
                        #become visible when listing ends
                        bid = Bid.objects.get(id=created_bid.id)
                        content = ('Your bid of $' + str(bid.amount) +
                            ' won the listing "' + current_listing.name
                            + '".')
                        BidNotification.objects.create(
                            listing=current_listing, user=request.user,
                            bid=created_bid,
                            creationDate=current_listing.endTime,
                            content=content, type="Winning Bid")

                        content = ('Your listing "' + current_listing.name
                            + '" has ended with a winning bid of $' + str(bid.amount) + '.')
                        print(created_bid.amount)
                        notifications = ListingNotification.objects.filter(listing=current_listing)
                        old_notification = notifications.first()
                        if current_listing.autobuy == bid_amount:
                            old_notification.creationDate = current_listing.endTime
                        old_notification.content = content
                        old_notification.type = "Listing Completed"
                        old_notification.save()

                        #Update the receipt for the listing
                        receipt = Receipt.objects.get(listing=current_listing)
                        receipt.exchangee = request.user
                        receipt.save()

                        return redirect('auction-listing-detail', pk=current_listing.pk)
                else:
                    form = CreateBidForm(instance=current_listing, initial={'auctionListing': current_listing, 'bidder': request.user})
                return render(request, 'listings/create_bid.html', {'form': form})
        else:
            return redirect('index')

#View for a user to delete an auction listing that they own
class AuctionListingDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = AuctionListing
    success_url = reverse_lazy('auction-listings')
    template_name = "listings/auction_listing_delete.html"
    context_object_name = 'auctionlisting'

    #Checks to make sure owner of listing clicked to delete, redirects otherwise
    #if auction is still active, redirect to auction listings
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner == self.request.user:
            if obj.listingEnded:
                return super(AuctionListingDeleteView, self).dispatch(request, *args, **kwargs)
            else:
                return redirect('auction-listings')
        else:
            return redirect('index')

    #Checks to see if expired listing has bids or not
    def delete(self, request, *args, **kwargs):
       self.object = self.get_object()

       if self.object.owner == self.request.user:
           #Check if listing has bids, if so soft delete
           #If not delete
           if Bid.objects.filter(auctionListing=self.object).exists():
               self.object.owner = None
               self.object.save()

               #Delete any notifications that were related to listing
               notifications = ListingNotification.objects.filter(listing=self.object)
               old_notification = notifications.first()
               old_notification.delete()
           else:
               #Go through items and delete any that don't have an owner
               for item in self.object.items.all():
                   if (item.owner == None
                       and Listing.objects.filter(items__pk=item.pk).exclude(
                           id=self.object.id).exists() != True
                       and Offer.objects.filter(items__pk=item.pk).exists()
                           != True
                       and Wishlist.objects.filter(items__pk=item.pk).exists()
                           != True):
                           #Go through images and delete any that don't have an owner
                           for image in item.images.all():
                               if (image.owner == None
                                   and Item.objects.filter(images__pk=image.pk).exclude(
                                       id=item.id).exists() != True):
                                   image.delete()

                           item.delete()

               self.object.delete()

           return HttpResponseRedirect(self.get_success_url())
       else:
           return redirect('index')

#View for a user to see a list of events they created
class EventListView(LoginRequiredMixin, generic.ListView):
    model = Event
    context_object_name = 'events'
    template_name = "events/events.html"
    paginate_by = 10

    #Filters the list of items to only show those that belong to the current logged in user
    def get_queryset(self):
        host_events = Event.objects.filter(host=self.request.user)
        participant_events = Event.objects.filter(participants__id=self.request.user.id)
        return host_events.union(participant_events).order_by('id')

#Detail view of an event only the host and participants can see
class EventDetailView(LoginRequiredMixin, generic.DetailView):
    model = Event
    template_name = "events/event_detail.html"

    #Checks to ensure that only the user that created the event or accepted
    #invite can see detail view
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.host == self.request.user:
            return super(EventDetailView, self).dispatch(request, *args, **kwargs)
        elif self.request.user in obj.participants.all():
            return super(EventDetailView, self).dispatch(request, *args, **kwargs)
        return redirect('index')

#Form view for creating an event
@login_required(login_url='/accounts/login/')
def create_event(request):
    if request.method == 'POST':
        form = EventForm(data=request.POST)
        if form.is_valid():
            created_event = form.save()

            #Set the user that created event as the host for the event
            created_event.host = request.user

            #Save the object and redirect to events list view
            created_event.save()
            return redirect('events')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})

#Form view for editing an event
@login_required(login_url='/accounts/login/')
def edit_event(request, pk):
    current_event = get_object_or_404(Event, pk=pk)

    #Check to ensure that the host is editing the event, redirect otherwise
    if current_event.host == request.user:
        if request.method == 'POST':
            form = EventForm(data=request.POST, instance=current_event)
            if form.is_valid():
                updated_event = form.save(commit=False)

                updated_event.save()
                return redirect('event-detail', pk=updated_event.pk)
        else:
            form = EventForm(instance=current_event)
        return render(request, 'events/edit_event.html', {'form': form})
    else:
        return redirect('index')

#Method for removing a user from an event
@login_required(login_url='/accounts/login/')
def remove_participant(request, event_pk, user_pk):
    current_event = get_object_or_404(Event, pk=event_pk)
    user = get_object_or_404(User, pk=user_pk)

    #Redirect if current user is not the host or a participant
    if request.user == current_event.host:
        #Host may remove any participant
        current_event.participants.remove(user)
        current_event.save()

        #Create notification for the user that the host has removed them
        #from the event
        content = (current_event.host.username + ' has removed you from ' +
            'the event "' + current_event.title + '".')
        EventNotification.objects.create(event=current_event,
            user=user, content=content, type="Participant Removed",
            creationDate=timezone.localtime(timezone.now()))

        #Redirect to the event detail page
        return redirect('event-detail', pk=current_event.pk)
    elif current_event.participants.filter(pk=request.user.pk).exists():
        #Check to ensure participant is removing themself from the event
        if request.user == user:
            #Remove user from event
            current_event.participants.remove(user)
            current_event.save()

            #Create notification for the host that the user has left
            #the event
            content = (user.username + ' has left the event "' +
                current_event.title + '".')
            EventNotification.objects.create(event=current_event,
                user=current_event.host, content=content, type="Participant Left",
                creationDate=timezone.localtime(timezone.now()))

            #Redirect to events list view page
            return redirect('events')
        else:
            #Redirect to index page if current user does not match user to be removed
            return redirect('index')
    else:
        return redirect('index')

#View for a user to delete an event that they are hosting
class EventDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Event
    success_url = reverse_lazy('events')
    template_name = "events/event_delete.html"
    context_object_name = 'event'

    #Checks to make sure owner of listing clicked to delete, redirects otherwise
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.host != self.request.user:
            return redirect('index')
        return super(EventDeleteView, self).dispatch(request, *args, **kwargs)

#View for a user to see a list of invitations they have received
class InvitationListView(LoginRequiredMixin, generic.ListView):
    model = Invitation
    context_object_name = 'invitations'
    template_name = "events/invitations.html"
    paginate_by = 20

    #Filters the list of invitations to only show those that belong to the
    #current logged in user
    def get_queryset(self):
        return Invitation.objects.filter(recipient=self.request.user)

#Form view for creating invitations for an event
@login_required(login_url='/accounts/login/')
def create_invitations(request, pk):
    #Get the event object the invitations are being created for
    current_event = get_object_or_404(Event, pk=pk)

    #Check to ensure the host is the one creating the invitations
    if request.user == current_event.host:
        if request.method == 'POST':
            form = InvitationForm(data=request.POST, instance=current_event, initial={'event': current_event})
            if form.is_valid():
                #Get the list of users from the form
                users = form.cleaned_data.get('users')

                #For each user, create an invitation for them
                for user in users:
                    if user.invitesOpen:
                        invitation = Invitation.objects.create(event=current_event, recipient=user)

                        #Create notification for the user that they were
                        #invited to event
                        content = (current_event.host.username + ' has invited you to ' +
                            'participate in their event "' + current_event.title +
                            '"!')
                        InvitationNotification.objects.create(event=current_event,
                            invitation=invitation, user=user,
                            content=content, type="Invitation Sent",
                            creationDate=timezone.localtime(timezone.now()))

                #Return to the event detail page
                return redirect('event-detail', pk=current_event.pk)
        else:
            form = InvitationForm(instance=current_event, initial={'event': current_event})
        return render(request, 'events/create_invitations.html', {'form': form})
    else:
        return redirect('index')

#Method for accepting an invitation for an event
@login_required(login_url='/accounts/login/')
def accept_invitation(request, pk):
    current_invitation = get_object_or_404(Invitation, pk=pk)

    #Redirect if current user is not the recipient
    if request.user != current_invitation.recipient:
            return redirect('index')
    else:
        #Add the user as a participant to the event
        event = Event.objects.get(id=current_invitation.event.id)
        event.participants.add(request.user)
        event.save()

        #Create notification for the host that the user has joined
        #the event
        content = (request.user.username + ' has accepted the invitiation ' +
            'to your event "' + event.title + '".')
        EventNotification.objects.create(event=event,
            user=current_invitation.event.host,
            content=content, type="Participant Joined",
            creationDate=timezone.localtime(timezone.now()))

        #Delete the invitation after accepting the invite
        current_invitation.delete()

        #Redirect to the event afterwards
        return redirect('event-detail', pk=event.pk)

#Method for declining an invitation for an event
@login_required(login_url='/accounts/login/')
def decline_invitation(request, pk):
    current_invitation = get_object_or_404(Invitation, pk=pk)

    #Redirect if current user is not the recipient
    if request.user != current_invitation.recipient:
            return redirect('index')
    else:
        #Create notification for the host that the user has declined to join
        #the event
        content = (request.user.username + ' has declined the invitiation ' +
            'to your event "' + current_invitation.event.title + '".')
        EventNotification.objects.create(event=current_invitation.event,
            user=current_invitation.event.host,
            content=content, type="Participant Declined",
            creationDate=timezone.localtime(timezone.now()))

        #Delete the invitation as user declined invite
        current_invitation.delete()

        #Redirect to invitation list view after
        return redirect('invitations')

#Detail view for a user's wishlist
class WishlistDetailView(LoginRequiredMixin, generic.DetailView):
    model = Wishlist
    template_name = "wishlists/wishlist_detail.html"

#Form view to create a wishlist for a user
@login_required(login_url='/accounts/login/')
def create_wishlist(request):
    #check to see if user already has made a wishlist, if so redirect to index
    try:
        wishlist = request.user.wishlist
    except Wishlist.DoesNotExist:
        wishlist = None

    if wishlist != None:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = WishlistForm(data=request.POST, user=request.user)
            if form.is_valid():
                created_wishlist = form.save()

                #Add items from the form to the new wishlist, if any
                clean_items = form.cleaned_data.get('items')
                if clean_items:
                    for item in clean_items:
                        created_wishlist.items.add(item)

                #Set wishlist owner as current user
                created_wishlist.owner = request.user
                created_wishlist.save()

                #redirect to the new wishlist's detail view
                return redirect('wishlist-detail', pk=created_wishlist.pk)
        else:
            form = WishlistForm(user=request.user)
        return render(request, 'wishlists/create_wishlist.html', {'form': form})

#Form view to edit a wishlist
@login_required(login_url='/accounts/login/')
def edit_wishlist(request, pk):
    #get wishlist object being edited
    current_wishlist = get_object_or_404(Wishlist, pk=pk)

    #check to see if user already has made a wishlist, if so redirect to index
    """try:
        wishlist = request.user.wishlist
    except Wishlist.DoesNotExist:
        wishlist = None"""

    #Check to make sure the wishlist's owner is the one editing, if not redirect
    if current_wishlist.owner != request.user:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = WishlistForm(data=request.POST, user=request.user, instance=current_wishlist)
            if form.is_valid():
                updated_wishlist = form.save(commit=False)

                #Clear the existing items from the wishlist
                updated_wishlist.items.clear()

                #Add items from the form to the new wishlist, if any
                clean_items = form.cleaned_data.get('items')
                if clean_items:
                    for item in clean_items:
                        updated_wishlist.items.add(item)

                #Save the updated wishlist
                updated_wishlist.save()

                #redirect to the wishlist's detail view
                return redirect('wishlist-detail', pk=updated_wishlist.pk)
        else:
            form = WishlistForm(user=request.user, instance=current_wishlist)
        return render(request, 'wishlists/edit_wishlist.html', {'form': form})

#Method for removing an item quickly from a wishlist
@login_required(login_url='/accounts/login/')
def remove_wishlist_item(request, wishlist_pk, item_pk):
    #Get the wishlist and item to remove
    current_wishlist = get_object_or_404(Wishlist, pk=wishlist_pk)
    item_to_remove = get_object_or_404(Item, pk=item_pk)

    #Redirect if current user is not the owner
    if request.user == current_wishlist.owner:
        #Check to make sure item is in wishlist
        if current_wishlist.items.filter(id=item_to_remove.id).exists():
            current_wishlist.items.remove(item_to_remove)
            current_wishlist.save()

            #Redirect to the event detail page
            return redirect('wishlist-detail', pk=current_wishlist.pk)
        else:
            return redirect('index')
    else:
        return redirect('index')

#List view for a user to see all of the wishlist listings they have
class WishlistListingListView(LoginRequiredMixin, generic.ListView):
    model = WishlistListing
    context_object_name = 'wishlistlistings'
    template_name = "wishlists/wishlist_listings.html"
    paginate_by = 10

    #Filters the list of wishlist listings to only show those that belong to the current logged in user
    def get_queryset(self):
        return WishlistListing.objects.filter(owner=self.request.user).order_by('endTime').reverse()

#Detail view for a wishlist listing
class WishlistListingDetailView(LoginRequiredMixin, generic.DetailView):
    model = WishlistListing
    context_object_name = 'wishlistlisting'
    template_name = "wishlists/wishlist_listing_detail.html"

#List view for a user to see all of the wishlists listings that are active on site
class AllWishlistListingsListView(LoginRequiredMixin, generic.ListView):
    model = WishlistListing
    context_object_name = 'wishlistlistings'
    template_name = "wishlists/all_wishlist_listings.html"
    paginate_by = 10

    #Filters the list of wishlist listings to only show those that
    #Have not ended yet
    def get_queryset(self):
        listings_ids = [listing.id for listing in WishlistListing.objects.all()
            if listing.listingEnded == False]
        return WishlistListing.objects.filter(id__in=listings_ids).order_by('id').reverse()

#Form view to create a wishlist listing for a user
@login_required(login_url='/accounts/login/')
def create_wishlist_listing(request):
    #check to see if user has made a wishlist before making a listing,
    #if not redirect to index
    try:
        wishlist = request.user.wishlist
    except Wishlist.DoesNotExist:
        wishlist = None

    if wishlist == None:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = WishlistListingForm(data=request.POST, user=request.user)
            if form.is_valid():
                created_wishlist_listing = form.save()

                #Get the end time choice from form and set end time accordingly
                clean_choice = form.cleaned_data.get('endTimeChoices')
                if clean_choice == '1h':
                    #Set end time to 1 hour from current time if choice was 1h
                    date = timezone.localtime(timezone.now()) + timedelta(hours=1)
                elif clean_choice == '2h':
                    #Set end time to 2 hours from current time if choice was 2h
                    date = timezone.localtime(timezone.now()) + timedelta(hours=2)
                elif clean_choice == '4h':
                    #Set end time to 4 hours from current time if choice was 4h
                    date = timezone.localtime(timezone.now()) + timedelta(hours=4)
                elif clean_choice == '8h':
                    #Set end time to 8 hours from current time if choice was 8h
                    date = timezone.localtime(timezone.now()) + timedelta(hours=8)
                elif clean_choice == '12h':
                    #Set end time to 12 hours from current time if choice was 12h
                    date = timezone.localtime(timezone.now()) + timedelta(hours=12)
                elif clean_choice == '1d':
                    #Set end time to 1 day from current time if choice was 1d
                    date = timezone.localtime(timezone.now()) + timedelta(days=1)
                elif clean_choice == '3d':
                    #Set end time to 3 days from current time if choice was 3ds
                    date = timezone.localtime(timezone.now()) + timedelta(days=3)
                else:
                    #Set end time to 7 days from current time
                    date = timezone.localtime(timezone.now()) + timedelta(days=7)

                #Set the endTime for the listing with the calculated date
                created_wishlist_listing.endTime = date

                #Check to see if moneyOffer was left blank in form
                clean_money_offer = form.cleaned_data.get('moneyOffer')
                if clean_money_offer:
                    pass
                else:
                    #set moneyOffer to $0.00 if no money was offered
                    created_wishlist_listing.moneyOffer = 0.00

                #Set the listing owner to be the current user
                created_wishlist_listing.owner = request.user

                #Add items from the form to the listing for wishlist items
                clean_wishlist_items = form.cleaned_data.get('items')
                for item in clean_wishlist_items:
                    created_wishlist_listing.items.add(item)

                #Add items from the form to the listing for offered items
                clean_offered_items = form.cleaned_data.get('itemsOffer')
                for item in clean_offered_items:
                    created_wishlist_listing.itemsOffer.add(item)

                #Save the wishlist listing
                created_wishlist_listing.save()

                #redirect to the list view for a user's wishlist listings
                return redirect('wishlist-listings')
        else:
            form = WishlistListingForm(user=request.user)
        return render(request, 'wishlists/create_wishlist_listing.html', {'form': form})

#Form view to edit a wishlist listing for a user
@login_required(login_url='/accounts/login/')
def edit_wishlist_listing(request, pk):
    #Get the listing to be editing
    current_listing = get_object_or_404(WishlistListing, pk=pk)

    #check to see if user has made a wishlist before editing a listing,
    #if not redirect to index
    try:
        wishlist = request.user.wishlist
    except Wishlist.DoesNotExist:
        wishlist = None

    if wishlist == None:
        return redirect('index')
    else:
        #Check to make sure that the owner of listing is editing
        #Redirect if not
        if current_listing.owner == request.user:
            #Check to make sure the listing is still active, if not redirect
            if current_listing.listingEnded != True:
                if request.method == 'POST':
                    form = EditWishlistListingForm(data=request.POST, user=request.user,
                        instance=current_listing)
                    if form.is_valid():
                        updated_listing = form.save(commit=False)

                        #Check to see if moneyOffer was left blank in form
                        clean_money_offer = form.cleaned_data.get('moneyOffer')
                        if clean_money_offer:
                            pass
                        else:
                            #set moneyOffer to $0.00 if no money was offered
                            updated_listing.moneyOffer = 0.00

                        #Clear current wishlist items from listing and add items from the
                        #form to the listing for wishlist items
                        updated_listing.items.clear()
                        clean_wishlist_items = form.cleaned_data.get('items')
                        for item in clean_wishlist_items:
                            updated_listing.items.add(item)

                        #Clear current offer items from listing and add items from the
                        #form to the listing for wishlist items
                        updated_listing.itemsOffer.clear()
                        clean_offered_items = form.cleaned_data.get('itemsOffer')
                        for item in clean_offered_items:
                            updated_listing.itemsOffer.add(item)

                        #Save the wishlist listing
                        updated_listing.save()

                        #redirect to the list view for a user's wishlist listings
                        return redirect('wishlist-listing-detail', pk=updated_listing.pk)
                else:
                    form = EditWishlistListingForm(user=request.user, instance=current_listing)
                return render(request, 'wishlists/edit_wishlist_listing.html', {'form': form})
            else:
                return redirect('wishlist-detail', pk=request.user.wishlist.id)
        else:
            return redirect('index')

#Form view to relist an expired wishlist listing for a user
@login_required(login_url='/accounts/login/')
def relist_wishlist_listing(request, pk):
    #Get the listing to be relisted
    current_listing = get_object_or_404(WishlistListing, pk=pk)

    #check to see if user has made a wishlist before relistng a listing,
    #if not redirect to index
    try:
        wishlist = request.user.wishlist
    except Wishlist.DoesNotExist:
        wishlist = None

    if wishlist == None:
        return redirect('index')
    else:
        #Check to make sure that the owner of listing is relisting
        #Redirect if not
        if current_listing.owner == request.user:
            #Check to make sure the listing has ended, if not redirect
            if current_listing.listingEnded:
                if request.method == 'POST':
                    form = WishlistListingForm(data=request.POST, user=request.user,
                        instance=current_listing)
                    if form.is_valid():
                        relisted_listing = form.save(commit=False)

                        #Get the end time choice from form and set end time accordingly
                        clean_choice = form.cleaned_data.get('endTimeChoices')
                        if clean_choice == '1h':
                            #Set end time to 1 hour from current time if choice was 1h
                            date = timezone.localtime(timezone.now()) + timedelta(hours=1)
                        elif clean_choice == '2h':
                            #Set end time to 2 hours from current time if choice was 2h
                            date = timezone.localtime(timezone.now()) + timedelta(hours=2)
                        elif clean_choice == '4h':
                            #Set end time to 4 hours from current time if choice was 4h
                            date = timezone.localtime(timezone.now()) + timedelta(hours=4)
                        elif clean_choice == '8h':
                            #Set end time to 8 hours from current time if choice was 8h
                            date = timezone.localtime(timezone.now()) + timedelta(hours=8)
                        elif clean_choice == '12h':
                            #Set end time to 12 hours from current time if choice was 12h
                            date = timezone.localtime(timezone.now()) + timedelta(hours=12)
                        elif clean_choice == '1d':
                            #Set end time to 1 day from current time if choice was 1d
                            date = timezone.localtime(timezone.now()) + timedelta(days=1)
                        elif clean_choice == '3d':
                            #Set end time to 3 days from current time if choice was 3ds
                            date = timezone.localtime(timezone.now()) + timedelta(days=3)
                        else:
                            #Set end time to 7 days from current time
                            date = timezone.localtime(timezone.now()) + timedelta(days=7)

                        #Set the endTime for the listing with the calculated date
                        relisted_listing.endTime = date

                        #Check to see if moneyOffer was left blank in form
                        clean_money_offer = form.cleaned_data.get('moneyOffer')
                        if clean_money_offer:
                            pass
                        else:
                            #set moneyOffer to $0.00 if no money was offered
                            relisted_listing.moneyOffer = 0.00

                        #Clear current wishlist items from listing and add items from the
                        #form to the listing for wishlist items
                        relisted_listing.items.clear()
                        clean_wishlist_items = form.cleaned_data.get('items')
                        for item in clean_wishlist_items:
                            relisted_listing.items.add(item)

                        #Clear current offer items from listing and add items from the
                        #form to the listing for wishlist items
                        relisted_listing.itemsOffer.clear()
                        clean_offered_items = form.cleaned_data.get('itemsOffer')
                        for item in clean_offered_items:
                            relisted_listing.itemsOffer.add(item)

                        #Save the wishlist listing
                        relisted_listing.save()

                        #redirect to the list view for a user's wishlist listings
                        return redirect('wishlist-listing-detail', pk=relisted_listing.pk)
                else:
                    form = WishlistListingForm(user=request.user, instance=current_listing)
                return render(request, 'wishlists/relist_wishlist_listing.html', {'form': form})
            else:
                return redirect('wishlist-detail', pk=request.user.wishlist.id)
        else:
            return redirect('index')

#Form view to quickly create a wishlist listing with the item selected for a user
@login_required(login_url='/accounts/login/')
def quick_wishlist_listing(request, pk):
    #Get the item that was selected by user
    current_item = get_object_or_404(Item, pk=pk)

    #check to see if user has made a wishlist before making a listing,
    #if not redirect to index
    try:
        wishlist = request.user.wishlist
    except Wishlist.DoesNotExist:
        wishlist = None

    if wishlist == None:
        print("No wishlist found")
        return redirect('index')
    else:
        #Check to ensure that the user owns the item they want to make listing with
        #If not redirect to index
        if current_item.owner != request.user:
            return redirect('index')
        else:
            if request.method == 'POST':
                #Initialize form with item selected
                form = QuickWishlistListingForm(data=request.POST, user=request.user,
                    initial={'items': Item.objects.filter(pk=current_item.pk)})
                if form.is_valid():
                    created_wishlist_listing = form.save()

                    #Get the end time choice from form and set end time accordingly
                    clean_choice = form.cleaned_data.get('endTimeChoices')
                    if clean_choice == '1h':
                        #Set end time to 1 hour from current time if choice was 1h
                        date = timezone.localtime(timezone.now()) + timedelta(hours=1)
                    elif clean_choice == '2h':
                        #Set end time to 2 hours from current time if choice was 2h
                        date = timezone.localtime(timezone.now()) + timedelta(hours=2)
                    elif clean_choice == '4h':
                        #Set end time to 4 hours from current time if choice was 4h
                        date = timezone.localtime(timezone.now()) + timedelta(hours=4)
                    elif clean_choice == '8h':
                        #Set end time to 8 hours from current time if choice was 8h
                        date = timezone.localtime(timezone.now()) + timedelta(hours=8)
                    elif clean_choice == '12h':
                        #Set end time to 12 hours from current time if choice was 12h
                        date = timezone.localtime(timezone.now()) + timedelta(hours=12)
                    elif clean_choice == '1d':
                        #Set end time to 1 day from current time if choice was 1d
                        date = timezone.localtime(timezone.now()) + timedelta(days=1)
                    elif clean_choice == '3d':
                        #Set end time to 3 days from current time if choice was 3ds
                        date = timezone.localtime(timezone.now()) + timedelta(days=3)
                    else:
                        #Set end time to 7 days from current time
                        date = timezone.localtime(timezone.now()) + timedelta(days=7)

                    #Set the endTime for the listing with the calculated date
                    created_wishlist_listing.endTime = date

                    #Check to see if moneyOffer was left blank in form
                    clean_money_offer = form.cleaned_data.get('moneyOffer')
                    if clean_money_offer:
                        pass
                    else:
                        #set moneyOffer to $0.00 if no money was offered
                        created_wishlist_listing.moneyOffer = 0.00

                    #Set the listing owner to be the current user
                    created_wishlist_listing.owner = request.user

                    #Add items from the form to the listing for wishlist items
                    clean_wishlist_items = form.cleaned_data.get('items')
                    for item in clean_wishlist_items:
                        created_wishlist_listing.items.add(item)

                    #Add items from the form to the listing for offered items
                    clean_offered_items = form.cleaned_data.get('itemsOffer')
                    for item in clean_offered_items:
                        created_wishlist_listing.itemsOffer.add(item)

                    #Save the wishlist listing
                    created_wishlist_listing.save()

                    #redirect to the list view for a user's wishlist listings
                    return redirect('wishlist-listings')
            else:
                form = QuickWishlistListingForm(user=request.user,
                    initial={'items': [str(current_item.id)]})
            return render(request, 'wishlists/quick_wishlist_listing.html', {'form': form})

#View for a user to delete an wishlist listing that they own
class WishlistListingDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = WishlistListing
    success_url = reverse_lazy('wishlist-listings')
    template_name = "wishlists/wishlist_listing_delete.html"
    context_object_name = 'wishlistlisting'

    #Checks to make sure owner of listing clicked to delete, redirects otherwise
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != self.request.user:
            return redirect('index')
        return super(WishlistListingDeleteView, self).dispatch(request, *args, **kwargs)

#Method to quickly add an item, owned or unowned, to a user's wishlist
@login_required(login_url='/accounts/login/')
def quick_add_item_to_wishlist(request, pk):
    #Get the item to be added to the wishlist
    item_to_add = get_object_or_404(Item, pk=pk)

    #check to see if user has made a wishlist before adding an item,
    #if not redirect to index
    try:
        wishlist = request.user.wishlist
    except Wishlist.DoesNotExist:
        wishlist = None

    if wishlist == None:
        return redirect('index')
    else:
        #check to make sure item is not on wishlist already
        users_wishlist = request.user.wishlist
        if users_wishlist.items.filter(id=item_to_add.id).exists():
            #Don't add to wishlist
            return redirect('item-detail', pk=item_to_add.pk)
        else:
            #Check to see if the item is owner or unowned by current user
            users_items = request.user.items
            if users_items.filter(id=item_to_add.id).exists():
                #Simply add the item to the user's wishlist
                users_wishlist.items.add(item_to_add)
                users_wishlist.save()

                #Redirect to the user's wishlist
                return redirect('wishlist-detail', pk=users_wishlist.pk)
            else:
                #Make a copy of the item for the current user to own
                item_copy = Item.objects.create(owner=request.user,
                    name=item_to_add.name, description=item_to_add.description)
                for image in item_to_add.images.all():
                    image_copy = Image.objects.create(owner=request.user,
                        image=image.image, name=image.name)
                    for tag in image.tags.all():
                        image_copy.tags.add(tag)
                    image_copy.save()

                    item_copy.images.add(image_copy)
                item_copy.save()

                #Add the item to the user's wishlist
                users_wishlist.items.add(item_copy)
                users_wishlist.save()

                #Redirect to the user's wishlist
                return redirect('wishlist-detail', pk=users_wishlist.pk)

#Detail view for an user's profile
class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = "profiles/profile_detail.html"

    #Receive the most recent active listings (offer/auction/wishlist) of the
    #user that owns the profile
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()

        #Get the most recent offer listings
        listings_ids = [listing.id for listing in OfferListing.objects.filter(owner=obj.user)
            if listing.listingEnded == False]
        context['offer_listings'] = OfferListing.objects.filter(id__in=listings_ids).order_by('-id')[:5]

        #Get the most recent auction listings
        listings_ids = [listing.id for listing in AuctionListing.objects.filter(owner=obj.user)
            if listing.listingEnded == False]
        context['auction_listings'] = AuctionListing.objects.filter(id__in=listings_ids).order_by('-id')[:5]

        #Get the most recent wishlist listings
        listings_ids = [listing.id for listing in WishlistListing.objects.filter(owner=obj.user)
            if listing.listingEnded == False]
        context['wishlist_listings'] = WishlistListing.objects.filter(id__in=listings_ids).order_by('-id')[:5]

        return context

#Form view to edit a user's profile
@login_required(login_url='/accounts/login/')
def edit_profile(request, pk):
    #Get the profile to be edited
    current_profile = get_object_or_404(Profile, pk=pk)

    #Check if the owner of item is editing the profile, if not redirect
    if current_profile.user == request.user:
        if request.method == 'POST':
            form = ProfileForm(data=request.POST, instance=current_profile)
            if form.is_valid():
                edited_profile = form.save(commit=False)

                #Update the user's location
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')

                #Gets the user's location information when not in the test
                #enviornment
                if ip != '127.0.0.1':
                    geo = GeoIP2()
                    user_location = geo.city(ip)
                    edited_profile.country = user_location["country_name"]
                    edited_profile.city = user_location["city"]
                    edited_profile.state = user_location["region"] #State the user is in
                    edited_profile.zipCode = user_location["postal_code"]

                #Save profile
                edited_profile.save()

                #Redirect to the profile's detail view
                return redirect('profile-detail', pk=edited_profile.pk)
        else:
            form = ProfileForm(instance=current_profile)
        return render(request, 'profiles/edit_profile.html', {'form': form})
    else:
        return redirect('index')

#List view for all users currently on the site
class UserListView(LoginRequiredMixin, generic.ListView):
    model = User
    context_object_name = 'users'
    template_name = "users/users.html"
    paginate_by = 25

    #Return the list of users in order of when they signed up
    def get_queryset(self):
        return User.objects.all().order_by('id')

#Form view to edit a user's account
@login_required(login_url='/accounts/login/')
def edit_account(request, pk):
    #Get the user to be edited
    current_user = get_object_or_404(User, pk=pk)

    #Check if the matching user is editing the account, redirect otherwise
    if current_user == request.user:
        if request.method == 'POST':
            form = EditAccountForm(data=request.POST, instance=current_user)
            if form.is_valid():
                edited_account = form.save(commit=False)
                edited_account.save()

                #Redirect to the user's profile
                return redirect('profile-detail', pk=current_user.profile.pk)
        else:
            form = EditAccountForm(instance=current_user)
        return render(request, 'users/edit_account.html', {'form': form})
    else:
        return redirect('index')

#List view for a user to see conversations related to them
class ConversationListView(LoginRequiredMixin, generic.ListView):
    model = Conversation
    context_object_name = 'conversations'
    template_name = "conversations/conversations.html"
    paginate_by = 15

    #Filters the list of conversations to only show those that the current
    #user is a sender or a recipient of
    def get_queryset(self):
        conversation_ids = [
            conversation.id for conversation
            in Conversation.objects.all()
            if conversation.sender == self.request.user
            or conversation.recipient == self.request.user
        ]

        latest_message = Subquery(Message.objects.filter(
            conversation_id=OuterRef("id"),
        ).values('dateSent').order_by("-dateSent")[:1])

        conversations = Conversation.objects.filter(id__in=conversation_ids).annotate(
            latest_message=latest_message).order_by(latest_message).reverse()

        return conversations

#Form view for a user to start a conversation with another user
@login_required(login_url='/accounts/login/')
def start_conversation(request, pk):
    #Get the user to be the recipient
    recipient = get_object_or_404(User, pk=pk)

    #Check if the sending user is not the recipient, redirect otherwise
    if recipient != request.user:
        #Check to ensure recipient is open to messages, else redirect
        if recipient.inquiriesOpen:
            if request.method == 'POST':
                form = ConversationForm(data=request.POST)
                if form.is_valid():
                    new_conversation = form.save()

                    #Set sender of conversation
                    new_conversation.sender = request.user

                    #Set recipient of conversation
                    new_conversation.recipient = recipient

                    #Save the conversation
                    new_conversation.save()

                    #Create the first message of the conversation
                    message_content = form.cleaned_data.get('message')
                    Message.objects.create(conversation=new_conversation,
                        author=request.user, content=message_content,
                        dateSent=timezone.localtime(timezone.now()),
                        unread=True)

                    #Redirect to conversations
                    return redirect('conversations')
            else:
                form = ConversationForm()
            return render(request, 'conversations/start_conversation.html',
                {'form': form})
        else:
            return redirect('index')
    else:
        return redirect('index')

#Detail view for a conversation with message form
class ConversationDetailView(LoginRequiredMixin, FormMixin, generic.DetailView):
    model = Conversation
    template_name = "conversations/conversation_detail.html"
    form_class = MessageForm

    #Checks to ensure that only sender and recipient can view the conversation
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.sender == self.request.user:
            return super(ConversationDetailView, self).dispatch(request, *args, **kwargs)
        elif obj.recipient == self.request.user:
            return super(ConversationDetailView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('index')

    #Get the current conversation being accessed
    def get_object(self):
        try:
            current_conversation = Conversation.objects.get(id=self.kwargs.get('pk'))

            #Have unread messages be read
            self.read_messages(current_conversation)

            return current_conversation
        except self.model.DoesNotExist:
            raise Http404("Conversation could not be found.")

    #Method to set messages to read in conversation
    def read_messages(self, conversation):
        #Get the messages from the conversation
        messages = Message.objects.filter(conversation=conversation)

        for message in messages:
            #set message to be read if current user is not author of it
            if message.unread:
                if (conversation.recipient == self.request.user
                    or conversation.sender == self.request.user):
                    if message.author != self.request.user:
                        message.unread = False
                        message.save()

    #Set the context for the detail view of the conversation
    def get_context_data(self, *args, **kwargs):
        context = super(ConversationDetailView, self).get_context_data(*args, **kwargs)
        conversation = self.get_object()
        if conversation.sender != None and conversation.recipient != None:
            context['message_form'] = self.get_form()
        context['conversation'] = conversation

        #Get the messages and add context to them
        messages = Message.objects.filter(conversation=conversation)
        new_messages = []
        for index, message in enumerate(messages):
            if index == 0:
                message.new_date = True
                previous = message
            else:
                #compare current message dateSent with previous message dateSent
                if (message.author == previous.author
                    and message.dateSent.year == previous.dateSent.year
                    and message.dateSent.month == previous.dateSent.month
                    and message.dateSent.day == previous.dateSent.day
                    and message.dateSent.hour == previous.dateSent.hour
                    and message.dateSent.minute == previous.dateSent.minute):
                        message.new_date = False
                        previous = message
                else:
                    message.new_date = True
                    previous = message

        context['messages'] = messages

        return context

    #Post method for the message form
    def post(self, request, *args, **kwargs):
        self.object = self.get_object() #conversation object
        if self.object.sender != None and self.object.recipient != None:
            form = self.get_form()
            if form.is_valid():
                content = form.cleaned_data.get('content')

                #Create the new message
                Message.objects.create(conversation=self.object,
                    author=request.user, content=content,
                    dateSent=timezone.localtime(timezone.now()),
                    unread=True)

                #Return to the conversation detail view
                return redirect('conversation-detail', pk=self.object.pk)
            else:
                return super(ConversationDetailView, self).form_invalid(form)
        else:
            raise Http404("The other user is no longer part of the conversation.")

#View for a user to delete an conversation they are a part of
#Conversation will only truly be deleted after both users have removed themselves
class ConversationDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Conversation
    success_url = reverse_lazy('conversations')
    template_name = "conversations/conversation_delete.html"
    context_object_name = 'conversation'

    #Checks to make sure sender or recipient of conversation clicked to delete
    #redirects otherwise
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.sender == self.request.user:
            return super(ConversationDeleteView, self).dispatch(request, *args, **kwargs)
        elif obj.recipient == self.request.user:
            return super(ConversationDeleteView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('index')

    #Handles deletion of the conversation so that it will only be deleted once
    #both users are removed
    def delete(self, request, *args, **kwargs):
       self.object = self.get_object()

       if (self.object.sender == self.request.user or self.object.recipient == self.request.user):
           if (self.object.sender != None and self.object.recipient != None):
               #Just remove the current user from conversation, do not delete
               if self.object.sender == self.request.user:
                   self.object.sender = None
                   self.object.save()
               else:
                   self.object.recipient = None
                   self.object.save()
           elif (self.object.sender == None or self.object.recipient == None):
               #Delete the conversation
               self.object.delete()
           return HttpResponseRedirect(self.get_success_url())
       else:
           return redirect('index')

#View for a user to see a list of receipts related to them
class ReceiptListView(LoginRequiredMixin, generic.ListView):
    model = Receipt
    context_object_name = 'receipts'
    template_name = "receipts/receipts.html"
    paginate_by = 10

    #Filters the list of receipts to only show those that belong to the current logged in user
    def get_queryset(self):
        all_receipt_ids = []

        #Get user's completed offer listings, and the receipts for listings
        offer_listings = OfferListing.objects.filter(owner=self.request.user, listingCompleted=True)
        if offer_listings:
            for listing in offer_listings:
                receipt = Receipt.objects.get(listing=listing)
                if receipt and (receipt.owner == self.request.user
                    or receipt.exchangee == self.request.user):
                        all_receipt_ids.append(receipt.id)

        #Get user's completed auction listings, and the receipts for listings
        auction_listing_ids = [listing.id for listing
            in AuctionListing.objects.filter(owner=self.request.user)
            if (listing.bids.count() > 0 and listing.listingEnded)]
        auction_listings = AuctionListing.objects.filter(id__in=auction_listing_ids)
        if auction_listings:
            for listing in auction_listings:
                receipt = Receipt.objects.get(listing=listing)
                if receipt and (receipt.owner == self.request.user
                    or receipt.exchangee == self.request.user):
                        all_receipt_ids.append(receipt.id)

        #Get users accepted offers, and the receipts for offers
        offers = Offer.objects.filter(owner=self.request.user, offerAccepted=True)
        if offers:
            listing_ids = [offer.offerListing.id for offer in offers]
            listings = OfferListing.objects.filter(id__in=listing_ids)
            if listings:
                for listing in listings:
                    receipt = Receipt.objects.get(listing=listing)
                    if receipt and (receipt.owner == self.request.user
                        or receipt.exchangee == self.request.user):
                            all_receipt_ids.append(receipt.id)

        #Get user's winning bids, and the receipts for bids
        bid_ids = [bid.id for bid
            in Bid.objects.filter(bidder=self.request.user, winningBid=True)
            if bid.auctionListing.listingEnded]
        bids = Bid.objects.filter(id__in=bid_ids)
        if bids:
            listing_ids = [bid.auctionListing.id for bid in bids]
            listings = AuctionListing.objects.filter(id__in=listing_ids)
            if listings:
                for listing in listings:
                    receipt = Receipt.objects.get(listing=listing)
                    if receipt and (receipt.owner == self.request.user
                        or receipt.exchangee == self.request.user):
                            all_receipt_ids.append(receipt.id)

        receipts = Receipt.objects.filter(id__in=all_receipt_ids).order_by('id')
        for receipt in receipts:
            #Add the actual listing subclass object to the receipt
            if OfferListing.objects.filter(receipt=receipt).exists():
                listing_obj = OfferListing.objects.get(receipt=receipt)
            else:
                listing_obj = AuctionListing.objects.get(receipt=receipt)

            receipt.listing_obj = listing_obj

            if PaymentReceipt.objects.filter(receipt=receipt).exists():
                receipt.payment_made = True
            else:
                receipt.payment_made = False

        return receipts

#Form view for user to make a payment
@login_required(login_url='/accounts/login/')
def make_paypal_payment(request, pk):
    #Get the receipt object to work with
    receipt = get_object_or_404(Receipt, pk=pk)

    #Check to see that the receipt exchangee is making payment, and that a
    #payment receipt does not already exist
    #Redirect if otherwise
    if (receipt.exchangee == request.user
        and PaymentReceipt.objects.filter(receipt=receipt).exists() != True) :
            #Get the listing that is related to the receipt
            if OfferListing.objects.filter(receipt=receipt).exists():
                listing = OfferListing.objects.get(receipt=receipt)
                listing_type = "Offer Listing"
            elif AuctionListing.objects.filter(receipt=receipt).exists():
                listing = AuctionListing.objects.get(receipt=receipt)
                listing_type = "Auction Listing"
            else:
                return redirect('index')

            #Check to ensure that listing has ended
            #If not, redirect
            if (listing_type == "Offer Listing"
                and (listing.listingEnded and listing.listingCompleted)):
                    #Get the related offer
                    related_offer = listing.offerlisting.last()

                    #Check to ensure that the offer is indeed the users.
                    #If so, check if an amount was included in offer
                    #If not, redirect
                    if (related_offer.owner == request.user
                        and related_offer.amount > 0.00
                        and related_offer.offerAccepted):
                            payment_amount = related_offer.amount
                    else:
                        return redirect('index')
            elif (listing_type == "Auction Listing"
                and (listing.listingEnded and listing.bids.count() > 0)):
                    #Get the related bid
                    related_bid = listing.bids.last()

                    #Check to ensure that the bid is indeed the users
                    #If so, get the amount offered in bid
                    #If not redirect
                    if (related_bid.bidder == request.user
                        and related_bid.winningBid):
                            payment_amount = related_bid.amount
                    else:
                        return redirect('index')
            else:
                return redirect('index')

            #User indeed owns the winning bid or accepted offer and an amount
            #was included.
            context = {
                'payment_amount': payment_amount,
                'user_paying': receipt.exchangee,
                'user_receiving': receipt.owner,
                'receipt': receipt,
            }
            return render(request, 'receipts/make_payment.html', context=context)
    else:
        return redirect('index')

#Form view for user to see paypal payment details after making payment
@login_required(login_url='/accounts/login/')
def paypal_payment_made(request, pk):
    #Get the receipt object to work with
    receipt = get_object_or_404(Receipt, pk=pk)

    if ((receipt.exchangee == request.user or receipt.owner == request.user)
        and PaymentReceipt.objects.filter(receipt=receipt).exists()):
            context = {
                'receipt': receipt,
            }
            return render(request, 'receipts/payment_made.html', context=context)
    else:
        return redirect('index')

#View that will update receipt when a payment is made
@csrf_exempt
def create_payment_receipt(request):
    if request.method == 'POST':
        if 'receipt_id' in request.POST:
            receipt_id = request.POST['receipt_id']
            receipt = get_object_or_404(Receipt, pk=receipt_id)
            if ('order_id' in request.POST
                and 'status' in request.POST
                and 'amount' in request.POST):
                    #Make the payment receipt
                    order_id = request.POST['order_id']
                    status = request.POST['status']
                    amount = request.POST['amount']

                    payment_receipt = PaymentReceipt.objects.create(
                        receipt=receipt, orderID=order_id, status=status,
                        amountPaid=amount,
                        paymentDate=str(timezone.localtime(timezone.now())))

                    #Create notification for owner that payment was made
                    content = (receipt.exchangee.username + ' has made a ' +
                        'payment of $' + "{:.2f}".format(float(payment_receipt.amountPaid))
                        + ' on the listing "' + receipt.listing.name + '".')
                    PaymentNotification.objects.create(receipt=receipt,
                        user=receipt.owner, content=content,
                        type="Payment Made",
                        creationDate=timezone.localtime(timezone.now()))
            return HttpResponse('success', status=200)
        else:
            #Something went wrong
            return HttpResponse('failed', status=404)
    else:
        #Nothing happens
        return HttpResponse('nothing happened', status=200)

#View for a user to delete an receipt they are the owner or exchangee on it
#Receipt will only truly be deleted after both users have removed themselves
class ReceiptDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Receipt
    success_url = reverse_lazy('receipts')
    template_name = "receipts/receipt_delete.html"
    context_object_name = 'receipt'

    #Checks to make sure owner or exchangee of reciept clicked to delete
    #Redirects otherwise
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if OfferListing.objects.filter(receipt=obj).exists():
            related_listing = OfferListing.objects.get(receipt=obj)
            offer_listing = True
        else:
            related_listing = AuctionListing.objects.get(receipt=obj)
            offer_listing = False

        if offer_listing:
            if (related_listing.listingEnded == True and related_listing.listingCompleted
                and (obj.owner == self.request.user or obj.exchangee == self.request.user)):
                    return super(ReceiptDeleteView, self).dispatch(request, *args, **kwargs)
            else:
                return redirect('index')
        else:
            if (related_listing.listingEnded == True and related_listing.bids.count() > 0
                and (obj.owner == self.request.user or obj.exchangee == self.request.user)):
                    return super(ReceiptDeleteView, self).dispatch(request, *args, **kwargs)
            else:
                return redirect('index')

    #Handles deletion of the receipt so that it will only be deleted once
    #both users are removed
    def delete(self, request, *args, **kwargs):
       self.object = self.get_object()
       offer_listing = False
       remove_owner = False
       remove_exchangee = False
       delete_receipt = False

       #Get the listing related to the receipt
       if OfferListing.objects.filter(receipt=self.object).exists():
           listing = OfferListing.objects.get(receipt=self.object)
           offer_listing = True
       else:
           listing = AuctionListing.objects.get(receipt=self.object)
           offer_listing = False

       #Redirect if listing has not ended yet
       if offer_listing:
           if(self.object.owner == self.request.user
                or self.object.exchangee == self.request.user):
                    if (self.object.owner != None and self.object.exchangee != None):
                        #Just remove the current user from receipt, do not delete
                        #But only if a payment has been made if money was offered
                        accepted_offer = listing.offerlisting.last()

                        if (accepted_offer.amount > 0.00
                            and PaymentReceipt.objects.filter(
                            receipt=self.object).exists() != True):
                                raise Http404(("You cannot delete this " +
                                    "receipt as a payment has not been " +
                                    "made yet."))
                        elif self.object.owner == self.request.user:
                            remove_owner = True
                        else:
                            remove_exchangee = True
                    else:
                        #Delete the receipt
                        delete_receipt = True
           else:
               return redirect('index')
       else:
           if(self.object.owner == self.request.user
                or self.object.exchangee == self.request.user):
                    if (self.object.owner != None and self.object.exchangee != None):
                        #Just remove the current user from receipt, do not delete
                        #But only if a payment has been made
                        if PaymentReceipt.objects.filter(
                            receipt=self.object).exists() != True:
                                raise Http404(("You cannot delete this " +
                                    "receipt as a payment has not been " +
                                    "made yet."))
                        elif self.object.owner == self.request.user:
                            remove_owner = True
                        else:
                            remove_exchangee = True
                    else:
                        #Delete the receipt
                        delete_receipt = True
           else:
               return redirect('index')

       if remove_owner:
           self.object.owner = None
           self.object.save()
       elif remove_exchangee:
           self.object.exchangee = None
           self.object.save()
       elif delete_receipt:
           #Delete the receipt, the related payment receipt and related listing
           #For the related listing, go through items and delete if owner is
           #none and has no relations to other objects, delete notifications
           #For each image for the item, delete if owner is none and has no
           #relations to other items, delete notifications
           #For offer listings, delete the items in the accepted offer that have
           #an owner of none and are not related to any other objects,
           #delete notifications. Do the same as above for the item's images

           #Delete the items for the accepted offer if offer listing
           if offer_listing:
               accepted_offer = listing.offerlisting.last()
               if accepted_offer.items.count() > 0:
                   for item in accepted_offer.items.all():
                       if (item.owner == None
                           and Listing.objects.filter(
                               items__pk=item.pk).exists() != True
                           and Offer.objects.filter(items__pk=item.pk).exclude(
                               id=accepted_offer.id).exists() != True
                           and Wishlist.objects.filter(items__pk=item.pk).exists()
                               != True):
                               #Go through images and delete any that don't have an owner
                               for image in item.images.all():
                                   if (image.owner == None
                                       and Item.objects.filter(images__pk=image.pk).exclude(
                                           id=item.id).exists() != True):
                                       image.delete()

                               item.delete()

               #Delete offer notifications related to listing
               listing_notifications = OfferNotification.objects.filter(listing=listing)
               if listing_notifications:
                   listing_notifications.delete()
           else:
               #Delete bid notifications related to listing
               bid_notifications = BidNotification.objects.filter(listing=listing)
               if bid_notifications:
                   bid_notifications.delete()

           #Delete the items in the related listing
           for item in listing.items.all():
               if (item.owner == None
                   and Listing.objects.filter(items__pk=item.pk).exclude(
                       id=listing.id).exists() != True
                   and Offer.objects.filter(items__pk=item.pk).exists() != True
                   and Wishlist.objects.filter(items__pk=item.pk).exists() != True):
                       #Go through images and delete any that don't have an owner
                       for image in item.images.all():
                           if (image.owner == None
                               and Item.objects.filter(images__pk=image.pk).exclude(
                                   id=item.id).exists() != True):
                               image.delete()

                       item.delete()

           #Delete notifications related to listing
           listing_notifications = ListingNotification.objects.filter(listing=listing)
           if listing_notifications:
               listing_notifications.delete()

           #Delete the related listing
           listing.delete()

           #Delete payment notifications
           payment_notifications = PaymentNotification.objects.filter(receipt=self.object)
           if payment_notifications:
               payment_notifications.delete()

           #Delete the receipt, which will delete the related payment receipt
           self.object.delete()

       return HttpResponseRedirect(self.get_success_url())

#View for a user to see a list of notifications related to them
class NotificationListView(LoginRequiredMixin, generic.ListView):
    model = Notification
    context_object_name = 'notifications'
    template_name = "notifications/notifications.html"
    paginate_by = 20

    #Filters the list of notifications to only show those that belong to
    #the current logged in user
    def get_queryset(self):
        notifications_ids = [notification.id for notification
            in Notification.objects.all()
            if (notification.active == True
            and notification.user == self.request.user)]
        notifications = Notification.objects.filter(id__in=notifications_ids).order_by('id')
        #notifications = Notification.objects.filter(user=self.request.user).order_by('id')

        #Get the subclass objects related to the notification
        if notifications:
            #Have unread notifications be read
            print(notifications)
            notifications = self.read_notifications(notifications)

            for notification in notifications:
                if (notification.type == "Listing Ended"
                    or notification.type == "Listing Expired"
                    or notification.type == "Auction Completed"):
                        #Get listing notification object
                        notification.obj = ListingNotification.objects.get(
                            id=notification.id)
                elif (notification.type == "Offer Accepted"
                    or notification.type == "Offer Rejected"
                    or notification.type == "Offer Retracted"
                    or notification.type == "Offer Made"
                    or notification.type == "Offer Updated"):
                        #Get offer notification object
                        notification.obj = OfferNotification.objects.get(
                            id=notification.id)
                elif (notification.type == "Outbid"
                    or notification.type == "Winning Bid"):
                        #Get bid notification object
                        notification.obj = BidNotification.objects.get(
                            id=notification.id)
                elif (notification.type == "Invitation Sent"):
                    #Get invitation notification object
                    notification.obj = InvitationNotification.objects.get(
                        id=notification.id)
                elif (notification.type == "Participant Joined"
                    or notification.type == "Participant Declined"
                    or notification.type == "Participant Removed"
                    or notification.type == "Participant Left"):
                        #Get bid notification object
                        notification.obj = EventNotification.objects.get(
                            id=notification.id)
                elif (notification.type == "Payment Made"):
                    #Get payment notification object
                    notification.obj = PaymentNotification.objects.get(
                        id=notification.id)
                elif (notification.type == "Feedback Left"):
                    #Get rating notification object
                    notification.obj = RatingNotification.objects.get(
                        id=notification.id)
                elif (notification.type == "Warning Received"):
                    #Get warning notification object
                    notification.obj = WarningNotification.objects.get(
                        id=notification.id)

        return notifications

    #Method to set notifications to read
    def read_notifications(self, notifications):
        for notification in notifications:
            print(notification)
            print(notification.unread)
            #set notification to be read
            if notification.unread:
                notification.unread = False
                notification.save()

        return notifications

#View method to delete a list of notifications selected by a user
@csrf_exempt #Add this too.
def delete_notifications(request, id=None):
    if request.method == 'POST':
        notification_id_list = request.POST.getlist('data')

        for notification_id in notification_id_list:
            #Get the notification
            notification = Notification.objects.get(id=notification_id)

            #Only delete the notification if the user that owns the notification
            #is deleting it
            if notification.user == request.user:
                notification.delete()

        #redirect to notifications list view
        return redirect('notifications')
    else:
        return HttpResponse('not post', status=404)
