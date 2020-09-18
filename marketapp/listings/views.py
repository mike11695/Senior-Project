from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count

from listings.models import Image, Item, Listing, OfferListing, AuctionListing, Offer, Bid
from listings.forms import (SignUpForm, AddImageForm, AddItemForm, CreateOfferListingForm,
    CreateAuctionListingForm, UpdateOfferListingForm, CreateOfferForm, CreateBidForm)

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

#View for a user to see a list of items they created
class ItemListView(LoginRequiredMixin, generic.ListView):
    model = Item
    context_object_name = 'items'
    template_name = "items/items.html"

    #Filters the list of items to only show those that belong to the current logged in user
    def get_queryset(self):
        return Item.objects.filter(owner=self.request.user)

#Detail view for an item only the owner can see
class ItemDetailView(LoginRequiredMixin, generic.DetailView):
    model = Item
    template_name = "items/item_detail.html"

#Form view to create an item for listings, offers and wish lists
@login_required(login_url='/accounts/login/')
def add_item(request):
    if request.method == 'POST':
        form = AddItemForm(data=request.POST, user=request.user)
        if form.is_valid():
            created_item = form.save()

            clean_images = form.cleaned_data.get('images')
            for image in clean_images:
                created_item.images.add(image)

            created_item.owner = request.user
            created_item.save()
            return redirect('items')
    else:
        form = AddItemForm(user=request.user)
    return render(request, 'items/add_item.html', {'form': form})

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

#List view for a user to see all of the offer listings they have active (Need to change this
#once listings are able to end)
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

#Form view to create an offer listing
@login_required(login_url='/accounts/login/')
def create_offer_listing(request):
    if request.method == 'POST':
        form = CreateOfferListingForm(data=request.POST, user=request.user)
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
        form = CreateOfferListingForm(user=request.user)
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

#View for a user to relist an offer listing that they own that has ended
class OfferListingRelistView(LoginRequiredMixin, generic.UpdateView):
    model = OfferListing
    fields = ['name', 'description', 'items', 'endTimeChoices', 'openToMoneyOffers',
        'minRange', 'maxRange', 'notes']
    template_name = "listings/relist_offer_listing.html"

    #Checks to make sure owner of listing is relisting, redirects otherwise
    #Also checks to ensure that listing actually had ended and had not been completed
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != self.request.user:
            return redirect('index')
        else:
            if obj.listingEnded and obj.listingCompleted != True:
                return super(OfferListingRelistView, self).dispatch(request, *args, **kwargs)
            else:
                return redirect('offer-listings')

    #Form valdation to ensure that previous offers are deleted, and end time is set
    def form_valid(self, form):
        relisted_listing = form.save(commit=False)

        #Retrieves the offers associated with current listing and deletes them
        Offer.objects.filter(offerListing=relisted_listing).delete()

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
                relisted_listing.maxRange = clean_maxRange
            else:
                #If not, set it to 0.00
                relisted_listing.maxRange = 0.00
        else:
            #If not checked, set ranges to 0.00
            relisted_listing.minRange = 0.00
            relisted_listing.maxRange = 0.00

        #Set the end date for the listing
        relisted_listing.endTime = date

        #Clear the current items from the listing
        relisted_listing.items.clear()

        #Add the newly added items to the listing
        clean_items = form.cleaned_data.get('items')
        for item in clean_items:
            relisted_listing.items.add(item)

        #Save the object
        relisted_listing.save()

        return super(OfferListingRelistView, self).form_valid(form)

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

    #Filters the list of offer listings to only show those that belong to the current logged in user
    def get_queryset(self):
        return AuctionListing.objects.filter(owner=self.request.user)

#Detailed view for all users to see an auction
class AuctionListingDetailView(LoginRequiredMixin, generic.DetailView):
    model = AuctionListing
    context_object_name = 'auction-listing-detail'
    template_name = "listings/auction_listing_detail.html"

#Form view for creating an auction listing
@login_required(login_url='/accounts/login/')
def create_auction_listing(request):
    if request.method == 'POST':
        form = CreateAuctionListingForm(data=request.POST, user=request.user)
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
        form = CreateAuctionListingForm(user=request.user)
    return render(request, 'listings/create_auction_listing.html', {'form': form})

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
                form = CreateOfferForm(data=request.POST, user=request.user, instance=current_listing, initial={'offerListing': current_listing})
                if form.is_valid():
                    created_offer = form.save()

                    #Add the items submitted to the offer
                    clean_items = form.cleaned_data.get('items')
                    for item in clean_items:
                        created_offer.items.add(item)

                    created_offer.owner = request.user
                    created_offer.save()
                    return redirect('offer-listing-detail', pk=current_listing.pk)
            else:
                form = CreateOfferForm(user=request.user, instance=current_listing, initial={'offerListing': current_listing})
            return render(request, 'listings/create_offer.html', {'form': form})
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

            #Retrieve the listing the offer is associated with, change listingCompleted to True and save object
            current_listing = OfferListing.objects.get(id=current_offer.offerListing.id)
            current_listing.listingCompleted = True
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

#Form view for creating an bid for an auction listing
@login_required(login_url='/accounts/login/')
def create_bid(request, pk):
    #Get the listing object the bid is being created for
    current_listing = get_object_or_404(AuctionListing, pk=pk)

    #Check to make sure listing is still active
    if current_listing.listingEnded:
        return redirect('index')
    else:
        #Check to ensure that the auction owner cannot bid on their own auction
        if request.user != current_listing.owner:
            if request.method == 'POST':
                form = CreateBidForm(data=request.POST, instance=current_listing, initial={'auctionListing': current_listing, 'bidder': request.user})
                if form.is_valid():
                    created_bid = form.save()

                    #Set the bidder and auctionListing fields (not sure why they aren't saving with the form...)
                    created_bid.bidder = request.user
                    created_bid.auctionListing = current_listing

                    created_bid.save()
                    return redirect('auction-listing-detail', pk=current_listing.pk)
            else:
                form = CreateBidForm(instance=current_listing, initial={'auctionListing': current_listing, 'bidder': request.user})
            return render(request, 'listings/create_bid.html', {'form': form})
        else:
            return redirect('index')
