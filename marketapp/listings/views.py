from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect

from listings.models import (User, Image, Item, Listing, OfferListing, AuctionListing,
    Offer, Bid, Event, Invitation, Wishlist)
from listings.forms import (SignUpForm, AddImageForm, ItemForm, OfferListingForm,
    AuctionListingForm, UpdateOfferListingForm, OfferForm, EditOfferForm, CreateBidForm,
    EventForm, InvitationForm, WishlistForm)

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
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
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
    fields = ['name', 'tags']
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

    #Get items that contain image to be deleted and delete them if they contain no other images afterwards
    def delete(self, request, *args, **kwargs):
       self.object = self.get_object()
       items = Item.objects.filter(owner=self.object.owner)
       if self.object.owner == self.request.user:
           self.object.delete()
           if items:
               for item in items:
                   if item.images.count() == 0:
                       #get the owner's listings to search which ones contain the item
                       offer_listings = OfferListing.objects.filter(owner=self.object.owner)
                       auction_listings = AuctionListing.objects.filter(owner=self.object.owner)

                       if offer_listings:
                           for listing in offer_listings:
                               if item in listing.items.all():
                                   #Deletes offer listing if it contained the item
                                   listing.delete()

                       if auction_listings:
                           for listing in auction_listings:
                               if item in listing.items.all():
                                   #Deletes auction listing if it contained the item
                                   listing.delete()

                       #Deletes item if no other images are contained as to not have items with broken images
                       item.delete()
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

    #Get listings that contain item to be deleted and delete them if they contain the item
    #Add wishlists and search listings to this once implemented
    def delete(self, request, *args, **kwargs):
       self.object = self.get_object()
       offer_listings = OfferListing.objects.filter(owner=self.object.owner)
       auction_listings = AuctionListing.objects.filter(owner=self.object.owner)
       if self.object.owner == self.request.user:
           if offer_listings:
               for listing in offer_listings:
                   if self.object in listing.items.all():
                       #Deletes offer listing if it contained the item
                       listing.delete()

           if auction_listings:
               for listing in auction_listings:
                   if self.object in listing.items.all():
                       #Deletes auction listing if it contained the item
                       listing.delete()

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
        if obj.owner == self.request.user:
            context['offers'] = Offer.objects.filter(offerListing=obj)
        else:
            context['offers'] = None
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

    #Filters the list of offer listings to only show those that belong to the current logged in user
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
            else:
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
                    current_listing = form.save(commit=False)

                    #Delete the previous existing offers
                    existing_offers.delete()

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

    #Filters the list of offer listings to only show those that belong to the current logged in user
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
    def get_queryset(self):
        bid_ids = [bid.id for bid in Bid.objects.all() if bid.auctionListing.listingEnded == False or
            bid.auctionListing.listingEnded and bid.winningBid]
        return Bid.objects.filter(id__in=bid_ids, bidder=self.request.user).order_by('id')

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

            #Set endTime for listing to current date and time so that it ends after accepting offer
            date = timezone.localtime(timezone.now())
            current_listing.endTime = date
            current_listing.save()

            #Retrieve the other offers for the listing and destroy them if not accepted
            other_offers = Offer.objects.filter(offerListing=current_listing)
            for offer in other_offers:
                if offer.offerAccepted != True:
                    #Destroy the object
                    offer.delete()

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
            if obj.offerAccepted:
                return redirect('offer-detail', pk=obj.pk)
            else:
                return super(OfferDeleteView, self).dispatch(request, *args, **kwargs)
        elif obj.offerListing.owner == self.request.user:
            if obj.offerAccepted:
                return redirect('offer-detail', pk=obj.pk)
            else:
                return super(OfferDeleteView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('index')

    #Returns offer listing owner to the offer listing, will return offer owner to their list of offers
    def get_success_url(self):
        obj = self.get_object()
        listing = OfferListing.objects.get(id=obj.offerListing.id)
        if obj.owner == self.request.user:
            #Change this to offer list later for user that owns offer
            return reverse_lazy('offer-listing-detail', kwargs={'pk': listing.pk})
        else:
            return reverse_lazy('offer-listing-detail', kwargs={'pk': listing.pk})

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

    #Redirect if current user is the host or a participant
    if request.user == current_event.host:
        #Host may remove any participant
        current_event.participants.remove(user)
        current_event.save()

        #Redirect to the event detail page
        return redirect('event-detail', pk=current_event.pk)
    elif current_event.participants.filter(pk=request.user.pk).exists():
        print("Participant removing themselves")
        #Check to ensure participant is removing themself from the event
        if request.user == user:
            #Remove user from event
            current_event.participants.remove(user)
            current_event.save()

            #Redirect to events list view page
            return redirect('events')
        else:
            #Redirect to index page if current user does not match user to be removed
            return redirect('index')
    else:
        print("User not part of event")
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
                    Invitation.objects.create(event=current_event, recipient=user)

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
            print("Post")
            form = WishlistForm(data=request.POST, user=request.user)
            if form.is_valid():
                print("Form is valid")
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
