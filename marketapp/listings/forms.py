from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from listings.models import (User, Image, Tag, Item, Listing, OfferListing,
    AuctionListing, Offer, Bid, Event, Invitation)
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError

from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import make_aware
from django.conf import settings
from django.shortcuts import get_object_or_404

#Form for a user to sign up to the site
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=100, help_text='Enter a valid e-mail address')
    paypalEmail = forms.EmailField(max_length=100, label="Paypal Email",
        help_text='Enter a valid Paypal e-mail address')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'paypalEmail', 'password1', 'password2', )

#Form for a user to upload an image to the site
class AddImageForm(ModelForm):
    def clean_image(self):
        clean_image = self.cleaned_data.get('image', False)

        #check image size to ensure it meets the limit
        if clean_image:
            width, height = get_image_dimensions(clean_image)
            if width > 1250 or height > 1250:
                raise ValidationError("Height or Width is larger than limit allowed.")
            return clean_image
        else:
            raise ValidationError("No image found")

    name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = Image
        fields = ['image', 'name', 'tags']
        exclude = ['owner', 'width', 'height']
        help_texts = {'image': "Image must not be larger than 1250x1250."}

#Form for a user to add and edit an item
class ItemForm(ModelForm):
    images = forms.ModelMultipleChoiceField(queryset=None, help_text="An image is required.")
    name = forms.CharField(max_length=50, required=True, help_text="Name for item is required.")

    class Meta:
        model = Item
        fields = ['images', 'name', 'description']
        exclude = ['owner']

    #Initializes the items dropdown with items that only relate to the current user
    def __init__(self, *args, **kwargs):
       self.user = kwargs.pop('user')
       super(ItemForm, self).__init__(*args, **kwargs)
       self.fields['images'].queryset = Image.objects.filter(owner=self.user)

#Form for creating and editing an offer listing
class OfferListingForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        clean_openToMoneyOffers = cleaned_data.get('openToMoneyOffers')
        clean_minRange = cleaned_data.get('minRange')
        clean_maxRange = cleaned_data.get('maxRange')

        #check image size to ensure it meets the limit
        if clean_openToMoneyOffers == True:
            #Check to see that minRange exists
            if clean_minRange:
                if clean_maxRange:
                    print("Max Range: ", clean_maxRange)
                    #Check to see that minRange is less than maxRange if not 0
                    if clean_minRange > clean_maxRange and clean_maxRange != 0.00:
                        raise ValidationError("Minimum range cannot be less that maximum range.")
                    #Check to see that minRange is not equal to maxRange
                    elif clean_minRange == clean_maxRange:
                        raise ValidationError("Minimum and maximum ranges must be different.")
                    #Check to see that ranges are not negative
                    elif clean_minRange < 0.00 or clean_maxRange < 0.00:
                        raise ValidationError("Minimum and maximum ranges must be a positive value.")
                    else:
                        return
                elif clean_minRange < 0.00:
                    raise ValidationError("Minimum range must be a positive value.")
                else:
                    return
            else:
                raise ValidationError("You must have at least a minimum range if open to money offers.")

    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), help_text="An item is required.")
    name = forms.CharField(max_length=50, required=True, help_text="Name for listing is required.")
    minRange = forms.DecimalField(max_digits=9, decimal_places=2, required=False,
        help_text="Minimum money offers you'll consider.")
    maxRange = forms.DecimalField(max_digits=9, decimal_places=2, required=False,
        help_text="Maximum money offers you'll consider (leave blank if you don't have a maximum).")

    class Meta:
        model = OfferListing
        fields = ['name', 'description', 'items', 'endTimeChoices', 'openToMoneyOffers',
            'minRange', 'maxRange', 'notes']
        exclude = ['owner', 'endTime', 'listingEnded', 'listingCompleted']

    #Initializes the items dropdown with items that only relate to the current user
    def __init__(self, *args, **kwargs):
       self.user = kwargs.pop('user')
       super(OfferListingForm, self).__init__(*args, **kwargs)
       self.fields['items'].queryset = Item.objects.filter(owner=self.user)

#This class is pretty much the same as CreateOfferListingForm, except it removes endTimeChoices
#from the form so the user can't just edit their listing to always be active
class UpdateOfferListingForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        clean_openToMoneyOffers = cleaned_data.get('openToMoneyOffers')
        clean_minRange = cleaned_data.get('minRange')
        clean_maxRange = cleaned_data.get('maxRange')

        #check image size to ensure it meets the limit
        if clean_openToMoneyOffers == True:
            #Check to see that minRange exists
            if clean_minRange:
                if clean_maxRange:
                    print("Max Range: ", clean_maxRange)
                    #Check to see that minRange is less than maxRange if not 0
                    if clean_minRange > clean_maxRange and clean_maxRange != 0.00:
                        raise ValidationError("Minimum range cannot be less that maximum range.")
                    #Check to see that minRange is not equal to maxRange
                    elif clean_minRange == clean_maxRange:
                        raise ValidationError("Minimum and maximum ranges must be different.")
                    #Check to see that ranges are not negative
                    elif clean_minRange < 0.00 or clean_maxRange < 0.00:
                        raise ValidationError("Minimum and maximum ranges must be a positive value.")
                    else:
                        return
                elif clean_minRange < 0.00:
                    raise ValidationError("Minimum range must be a positive value.")
                else:
                    return
            else:
                raise ValidationError("You must have at least a minimum range if open to money offers.")

    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), help_text="An item is required.")
    name = forms.CharField(max_length=50, required=True, help_text="Name for listing is required.")
    minRange = forms.DecimalField(max_digits=9, decimal_places=2, required=False,
        help_text="Minimum money offers you'll consider.")
    maxRange = forms.DecimalField(max_digits=9, decimal_places=2, required=False,
        help_text="Maximum money offers you'll consider (leave blank if you don't have a maximum).")

    class Meta:
        model = OfferListing
        fields = ['name', 'description', 'items', 'openToMoneyOffers', 'minRange', 'maxRange', 'notes']
        exclude = ['owner', 'endTime', 'endTimeChoices', 'listingEnded', 'listingCompleted']

    #Initializes the items dropdown with items that only relate to the current user
    def __init__(self, *args, **kwargs):
       self.user = kwargs.pop('user')
       super(UpdateOfferListingForm, self).__init__(*args, **kwargs)
       self.fields['items'].queryset = Item.objects.filter(owner=self.user)

#Form for a user to create an auction listing
class AuctionListingForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        clean_starting_bid = cleaned_data.get('startingBid')
        clean_minimum_increment = cleaned_data.get('minimumIncrement')
        clean_autobuy = cleaned_data.get('autobuy')

        #Checks to ensure that starting bid must be at least 0.01
        if clean_starting_bid:
            if clean_starting_bid < 0.01:
                raise ValidationError("Starting bid must be at least $0.01.")

        if clean_minimum_increment:
            #Checks to ensure that minimum increment must be at least 0.01
            if clean_minimum_increment < 0.01:
                raise ValidationError("Minimum increment must be at least $0.01.")
            #Checks to ensure that minimum increment is not greater than the starting bid
            if clean_starting_bid:
                if clean_minimum_increment > clean_starting_bid:
                    raise ValidationError("Minimum increment must not be greater than starting bid.")

        if clean_autobuy:
            #Checks to ensure that autobuy must be at least 0.01
            if clean_autobuy < 0.01:
                raise ValidationError("Autobuy must be at least $0.01.")
            if clean_starting_bid:
                #Checks to ensure that autobuy is not less than or equal to the starting bid
                if clean_autobuy <= clean_starting_bid:
                    raise ValidationError("Autobuy must be greater than the starting bid.")

        return

    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), help_text="An item is required.")
    name = forms.CharField(max_length=50, required=True, help_text="Name for listing is required.")
    startingBid = forms.DecimalField(max_digits=9, decimal_places=2, required=True,
        help_text="Money amount bidding should start at for auction.")
    minimumIncrement = forms.DecimalField(max_digits=9, decimal_places=2, required=True,
        help_text="Minimum increment bid that can be placed on the auction, that cannot be greater than the starting bid (maximum increment bid will be x3 this value).")
    autobuy = forms.DecimalField(max_digits=9, decimal_places=2, required=False,
        help_text="A bid greater than the starting bid that will automatically win the auction if placed. (Leave blank if not interested in having an autobuy price)")

    class Meta:
        model = AuctionListing
        fields = ['name', 'description', 'items', 'endTimeChoices', 'startingBid',
            'minimumIncrement', 'autobuy']
        exclude = ['owner', 'endTime', 'listingEnded']

    #Initializes the items dropdown with items that only relate to the current user
    def __init__(self, *args, **kwargs):
       self.user = kwargs.pop('user')
       super(AuctionListingForm, self).__init__(*args, **kwargs)
       self.fields['items'].queryset = Item.objects.filter(owner=self.user)

#Form for a user to create an offer for an offer listing
class OfferForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        clean_amount = cleaned_data.get('amount')
        clean_listing = cleaned_data.get('offerListing')

        if timezone.localtime(timezone.now()) > clean_listing.endTime:
            raise ValidationError("Listing has ended, no offers can be made.")
        else:
            if clean_amount:
                if clean_listing.openToMoneyOffers:
                    if (clean_amount < clean_listing.minRange) and clean_amount != 0.00:
                        #Check to see that the amount offered is not less than the listing's minimum range
                        raise ValidationError("Amount offered is less than the minimum range of ${0}".format(clean_listing.minRange))
                    elif clean_amount > clean_listing.maxRange:
                        #Check to see that the amount offered is not more than the listing's maximum range
                        raise ValidationError("Amount offered is more than the maximum range of ${0}".format(clean_listing.maxRange))
                else:
                    raise ValidationError("Listing is not accepting money offers.")
            else:
                clean_items = cleaned_data.get('items')
                if clean_items:
                    pass
                else:
                    raise ValidationError("An item must be offered.")

        return

    offerListing = forms.ModelChoiceField(queryset=OfferListing.objects.all(), required=False,
        disabled=True, label="Offer Listing")
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(),
        help_text="Items are not required for an offer if user is open to money offers.",
        required=False)
    amount = forms.DecimalField(max_digits=9, decimal_places=2, required=False,
        help_text="Amount of cash you'd like to offer on listing (Leave blank or enter 0.00 if you do not want to offer cash).")

    class Meta:
        model = Offer
        exclude = ['owner', 'offerAccepted']

    #Initializes the items dropdown with items that only relate to the current user
    #Also gets the listing person is offering on
    def __init__(self, *args, **kwargs):
       self.user = kwargs.pop('user')
       listing = kwargs.pop('instance')
       self.listing = OfferListing.objects.get(id=listing.id)
       super(OfferForm, self).__init__(*args, **kwargs)
       self.fields['items'].queryset = Item.objects.filter(owner=self.user)
       if self.listing.openToMoneyOffers:
           self.fields['amount'].initial = 0.00
       else:
           self.fields['amount'].initial = 0.00
           self.fields['amount'].widget.attrs['readonly'] = True

#Form for a user to create an offer for an offer listing
class EditOfferForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        clean_amount = cleaned_data.get('amount')
        clean_listing = cleaned_data.get('offerListing')

        if timezone.localtime(timezone.now()) > clean_listing.endTime:
            raise ValidationError("Listing has ended, no offers can be made.")
        else:
            if clean_amount:
                if clean_listing.openToMoneyOffers:
                    if (clean_amount < clean_listing.minRange) and clean_amount != 0.00:
                        #Check to see that the amount offered is not less than the listing's minimum range
                        raise ValidationError("Amount offered is less than the minimum range of ${0}".format(clean_listing.minRange))
                    elif clean_amount > clean_listing.maxRange:
                        #Check to see that the amount offered is not more than the listing's maximum range
                        raise ValidationError("Amount offered is more than the maximum range of ${0}".format(clean_listing.maxRange))
                else:
                    raise ValidationError("Listing is not accepting money offers.")
            else:
                clean_items = cleaned_data.get('items')
                if clean_items:
                    pass
                else:
                    raise ValidationError("An item must be offered.")

        return

    offerListing = forms.ModelChoiceField(queryset=OfferListing.objects.all(), required=False,
        disabled=True, label="Offer Listing")
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(),
        help_text="Items are not required for an offer if user is open to money offers.",
        required=False)
    amount = forms.DecimalField(max_digits=9, decimal_places=2, required=False,
        help_text="Amount of cash you'd like to offer on listing (Leave blank or enter 0.00 if you do not want to offer cash).")

    class Meta:
        model = Offer
        exclude = ['owner', 'offerAccepted']

    #Initializes the items dropdown with items that only relate to the current user
    #Also gets the listing person is offering on
    def __init__(self, *args, **kwargs):
       self.user = kwargs.pop('user')
       listing = kwargs.pop('listing')
       super(EditOfferForm, self).__init__(*args, **kwargs)
       self.listing = OfferListing.objects.get(id=listing.id)
       self.fields['items'].queryset = Item.objects.filter(owner=self.user)
       if self.listing.openToMoneyOffers == False:
           self.fields['amount'].initial = 0.00
           self.fields['amount'].widget.attrs['readonly'] = True

#Form for a user to create a bid for an auction listing
class CreateBidForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        clean_amount = cleaned_data.get('amount')
        clean_listing = cleaned_data.get('auctionListing')
        clean_bidder = cleaned_data.get('bidder')

        if timezone.localtime(timezone.now()) > clean_listing.endTime:
            raise ValidationError("Auction has ended, no bids can be placed.")
        else:
            if clean_amount:
                bids = Bid.objects.filter(auctionListing=clean_listing)
                if bids:
                    #Auction has at least one bid
                    if bids.count() == 1:
                        current_bid = bids.first()
                    else:
                        current_bid = bids.last()

                    if clean_listing.autobuy:
                        if clean_amount != clean_listing.autobuy:
                            if clean_amount == current_bid.amount and current_bid.amount == clean_listing.startingBid:
                                #Amount bid is same as starting and current bid
                                raise ValidationError("Starting bid has already been placed.")
                            elif clean_amount <= current_bid.amount:
                                #Amount bid is less than or equal to the current bid
                                lowest_bid = clean_listing.startingBid + clean_listing.minimumIncrement
                                raise ValidationError("Lowest bid that can be placed is ${0}".format(lowest_bid))
                            elif current_bid.bidder == clean_bidder:
                                #User already has the current bid
                                raise ValidationError("You already have the current bid.")
                            elif clean_amount > (current_bid.amount + (clean_listing.minimumIncrement * 3)):
                                #Amount bid is greater than the maximum that can be bid
                                highest_bid = clean_listing.amount + (clean_listing.minimumIncrement * 3)
                                raise ValidationError("Maximum bid that can be placed is ${0}".format(highest_bid))
                            elif clean_amount < (current_bid.amount + clean_listing.minimumIncrement):
                                #Amount bid is less than the minimum bid that can currently be bid
                                minimal_bid = current_bid.amount + clean_listing.minimumIncrement
                                raise ValidationError("Minimum bid that can be placed is ${0}".format(minimal_bid))
                    else:
                        if clean_amount == current_bid.amount and current_bid.amount == clean_listing.startingBid:
                            #Amount bid is same as starting and current bid
                            raise ValidationError("Starting bid has already been placed.")
                        elif clean_amount <= current_bid.amount:
                            #Amount bid is less than or equal to the current bid
                            lowest_bid = clean_listing.startingBid + clean_listing.minimumIncrement
                            raise ValidationError("Lowest bid that can be placed is ${0}".format(lowest_bid))
                        elif current_bid.bidder == clean_bidder:
                            #User already has the current bid
                            raise ValidationError("You already have the current bid.")
                        elif clean_amount > (current_bid.amount + (clean_listing.minimumIncrement * 3)):
                            #Amount bid is greater than the maximum that can be bid
                            highest_bid = clean_listing.amount + (clean_listing.minimumIncrement * 3)
                            raise ValidationError("Maximum bid that can be placed is ${0}".format(highest_bid))
                        elif clean_amount < (current_bid.amount + clean_listing.minimumIncrement):
                            #Amount bid is less than the minimum bid that can currently be bid
                            minimal_bid = current_bid.amount + clean_listing.minimumIncrement
                            raise ValidationError("Minimum bid that can be placed is ${0}".format(minimal_bid))
                else:
                    #There are no bids currently
                    if clean_listing.autobuy:
                        if clean_amount != clean_listing.autobuy:
                            if clean_amount < clean_listing.startingBid:
                                #Amount bid is less than the starting bid
                                raise ValidationError("Bid must be equal to or greater than the starting bid.")
                            elif clean_amount > (clean_listing.startingBid + (clean_listing.minimumIncrement * 3)):
                                #Amount bid is greater than the maximum that can be bid
                                highest_bid = clean_listing.startingBid + (clean_listing.minimumIncrement * 3)
                                raise ValidationError("Maximum bid that can be placed is ${0}".format(highest_bid))
                            elif clean_amount < (clean_listing.startingBid + clean_listing.minimumIncrement) and clean_amount != clean_listing.startingBid:
                                #Amount bid is less than the minimum bid that can currently be bid
                                minimal_bid = clean_listing.startingBid + clean_listing.minimumIncrement
                                raise ValidationError("Minimum bid that can be placed is ${0}".format(minimal_bid))
                    else:
                        if clean_amount < clean_listing.startingBid:
                            #Amount bid is less than the starting bid
                            raise ValidationError("Bid must be equal to or greater than the starting bid.")
                        elif clean_amount > (clean_listing.startingBid + (clean_listing.minimumIncrement * 3)):
                            #Amount bid is greater than the maximum that can be bid
                            highest_bid = clean_listing.startingBid + (clean_listing.minimumIncrement * 3)
                            raise ValidationError("Maximum bid that can be placed is ${0}".format(highest_bid))
                        elif clean_amount < (clean_listing.startingBid + clean_listing.minimumIncrement) and clean_amount != clean_listing.startingBid:
                            #Amount bid is less than the minimum bid that can currently be bid
                            minimal_bid = clean_listing.startingBid + clean_listing.minimumIncrement
                            raise ValidationError("Minimum bid that can be placed is ${0}".format(minimal_bid))
            else:
                #No bid was included
                raise ValidationError("An amount must be included in bid.")

        return

    auctionListing = forms.ModelChoiceField(queryset=AuctionListing.objects.all(), required=False,
        disabled=True, label="Auction Listing")
    bidder = forms.ModelChoiceField(queryset=User.objects.all(), required=False,
        disabled=True, label="Bidder")

    class Meta:
        model = Bid
        fields = ['amount']
        exclude = ['winningBid']

    #Initializes the bid field with the current minimal increment bid
    def __init__(self, *args, **kwargs):
        listing = kwargs.pop('instance')
        self.listing = AuctionListing.objects.get(id=listing.id)
        self.bids = Bid.objects.filter(auctionListing=self.listing)
        super(CreateBidForm, self).__init__(*args, **kwargs)

        if self.bids:
            if self.bids.count() > 1:
                current_bid = self.bids.last()
                self.fields['amount'].initial = current_bid.amount + self.listing.minimumIncrement
            elif self.bids.count() == 1:
                current_bid = self.bids.first()
                self.fields['amount'].initial = current_bid.amount + self.listing.minimumIncrement
        else:
            self.fields['amount'].initial = self.listing.startingBid

#Form for a user to create an event
class EventForm(ModelForm):
    #Host will be set in form creation view, participants will be added when they accept an invitation
    title = forms.CharField(max_length=50, required=True, help_text="Title For the Event Required.")
    date = forms.DateTimeField(required=True,
        help_text="Date/Time for Event ('YY-MM-DD' format or 'YY-MM-DD H:M' format).")
    location = forms.CharField(max_length=100, required=True, help_text="Address Where Event is Held.")

    class Meta:
        model = Event
        fields = ['title', 'context', 'date', 'location']
        exclude = ['host', 'participants']

#Form for a user to select users to invite to an event
class InvitationForm(forms.Form):
    def clean(self):
        cleaned_data = super().clean()
        clean_users = cleaned_data.get('users')
        clean_event = cleaned_data.get('event')

        if clean_users:
            #Check for each user invited if they already received an invitation,
            #and see if they are accepting invitations
            for user in clean_users:
                if user.invitesOpen == False:
                    raise ValidationError("User {0} is not accepting invitations to events.".format(user))
                elif Invitation.objects.filter(event=clean_event, recipient=user).exists():
                    raise ValidationError("User {0} already has an invitation to this event.".format(user))
            return
        else:
            raise ValidationError("At least one user must be selected to invite.")

    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), label="Users to Invite",
        help_text="Users You Would Like to Invite to Event.")
    event = forms.ModelChoiceField(queryset=Event.objects.all(), required=False,
        disabled=True)

    #Set the queryset for users to only be ones that have not accepted an invite to event
    def __init__(self, *args, **kwargs):
       event = kwargs.pop('instance')
       super(InvitationForm, self).__init__(*args, **kwargs)
       existing_participants_ids = [user.id for user in event.participants.all()]
       self.fields['users'].queryset = User.objects.exclude(id__in=existing_participants_ids)
