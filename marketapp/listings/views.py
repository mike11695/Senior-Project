from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from listings.models import Image, Item, Listing, OfferListing, AuctionListing
from listings.forms import (SignUpForm, AddImageForm, AddItemForm, CreateOfferListingForm,
    CreateAuctionListingForm)

from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import make_aware
from django.conf import settings

# Create your views here.
def index(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')

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

class ImageListView(LoginRequiredMixin, generic.ListView):
    model = Image
    context_object_name = 'images'
    template_name = "images/images.html"

class ImageDetailView(LoginRequiredMixin, generic.DetailView):
    model = Image
    template_name = "images/image_detail.html"

@login_required(login_url='/accounts/login/')
def add_image(request):
    if request.method == 'POST':
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            created_image = form.save()
            created_image.owner = request.user
            created_image.save()
            return redirect('images')
    else:
        form = AddImageForm()
    return render(request, 'images/add_image.html', {'form': form})

class ItemListView(LoginRequiredMixin, generic.ListView):
    model = Item
    context_object_name = 'items'
    template_name = "items/items.html"

class ItemDetailView(LoginRequiredMixin, generic.DetailView):
    model = Item
    template_name = "items/item_detail.html"

@login_required(login_url='/accounts/login/')
def add_item(request):
    if request.method == 'POST':
        form = AddItemForm(data=request.POST, user=request.user)
        if form.is_valid():
            created_item = form.save()
            created_item.owner = request.user
            created_item.save()
            return redirect('items')
    else:
        form = AddItemForm(user=request.user)
    return render(request, 'items/add_item.html', {'form': form})

@login_required(login_url='/accounts/login/')
def faq(request):
    # Render the HTML template faq/documents.html with the data in the context variable
    return render(request, 'faq/documents.html')

@login_required(login_url='/accounts/login/')
def faq_images(request):
    # Render the HTML template faq/images.html with the data in the context variable
    return render(request, 'faq/images.html')

@login_required(login_url='/accounts/login/')
def faq_items(request):
    # Render the HTML template faq/items.html with the data in the context variable
    return render(request, 'faq/items.html')

class OfferListingListView(LoginRequiredMixin, generic.ListView):
    model = OfferListing
    context_object_name = 'offerlistings'
    template_name = "listings/offer_listings.html"

class OfferListingDetailView(LoginRequiredMixin, generic.DetailView):
    model = OfferListing
    context_object_name = 'offer-listing-detail'
    template_name = "listings/offer_listing_detail.html"

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
            created_listing.save()
            return redirect('offer-listings')
    else:
        form = CreateOfferListingForm(user=request.user)
    return render(request, 'listings/create_offer_listing.html', {'form': form})

class AuctionListingListView(LoginRequiredMixin, generic.ListView):
    model = AuctionListing
    context_object_name = 'auctionlistings'
    template_name = "listings/auction_listings.html"

class AuctionListingDetailView(LoginRequiredMixin, generic.DetailView):
    model = AuctionListing
    context_object_name = 'auction-listing-detail'
    template_name = "listings/auction_listing_detail.html"

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
