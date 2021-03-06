from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from listings.models import (User, Image, Tag, Item, Listing, OfferListing,
    AuctionListing, Offer, Bid, Event, Invitation, Wishlist, WishlistListing,
    Profile, Conversation, Message, Report, ListingReport, EventReport,
    UserReport, RatingReport, WishlistReport, ImageReport, Rating,
    RatingTicket)
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError
from decimal import Decimal

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
        fields = ('username', 'first_name', 'last_name', 'email', 'paypalEmail',
            'password1', 'password2')

#Form for user to edit their account
class EditAccountForm(ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    paypalEmail = forms.EmailField(max_length=100, label="Paypal Email",
        help_text='Enter a valid Paypal e-mail address', required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'paypalEmail',
            'invitesOpen', 'inquiriesOpen')
        exclude = ['username', 'email', 'password1', 'password2']
        labels = {'invitesOpen': "Open to Invitations?",
            'inquiriesOpen': "Open to Inquiries?"}
        help_texts = {'invitesOpen': "Check if you want to be invited to events",
            'inquiriesOpen': "Check if you want users to message you"}

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
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple, required=False, label="Tags")

    class Meta:
        model = Image
        fields = ['image', 'name', 'tags']
        exclude = ['owner', 'width', 'height']
        help_texts = {'image': "Image must not be larger than 1250x1250."}

#Form for a user to edit an image
class EditImageForm(ModelForm):
    name = forms.CharField(max_length=50, required=True)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple, required=False, label="Tags")

    class Meta:
        model = Image
        fields = ['name', 'tags']
        exclude = ['image', 'owner', 'width', 'height']

#Form for a user to add and edit an item
class ItemForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        clean_images = cleaned_data.get('images')

        #Check to make sure user selected an image
        if clean_images:
            pass
        else:
            raise ValidationError("An image must be selected.")

    images = forms.ModelMultipleChoiceField(queryset=None,
        help_text="An image is required.", widget=forms.CheckboxSelectMultiple,
        required=True)
    name = forms.CharField(max_length=50, required=True,
        help_text="Name for item is required.")
    description = forms.CharField(max_length=250, required=True,
        widget=forms.Textarea(attrs={'rows':5, 'cols':23}),
        help_text="A brief description of the item in the image(s).")

    class Meta:
        model = Item
        fields = ['name', 'description', 'images']
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
        clean_items = cleaned_data.get('items')

        #Check to make sure user selected items
        if clean_items:
            pass
        else:
            raise ValidationError("You must select at least one item.")

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

    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(),
        help_text="An item is required.", widget=forms.CheckboxSelectMultiple)
    name = forms.CharField(max_length=50, required=True, help_text="Name for listing is required.")
    minRange = forms.DecimalField(max_digits=9, decimal_places=2, required=False,
        help_text="Minimum money offers you'll consider.", label="Minimum Offer Range")
    maxRange = forms.DecimalField(max_digits=9, decimal_places=2, required=False,
        help_text="Maximum money offers you'll consider (leave blank if you don't have a maximum).",
        label="Maximum Offer Range")
    description = forms.CharField(max_length=500, required=True,
        widget=forms.Textarea(attrs={'rows':5, 'cols':49}),
        help_text="A short description of what the listing obtains.")
    notes = forms.CharField(max_length=500, required=True,
        widget=forms.Textarea(attrs={'rows':5, 'cols':49}),
        help_text="Include here what offers you're seeking.")

    class Meta:
        model = OfferListing
        fields = ['name', 'items', 'description', 'endTimeChoices', 'openToMoneyOffers',
            'minRange', 'maxRange', 'notes']
        exclude = ['owner', 'endTime', 'listingEnded', 'listingCompleted']
        labels = {'endTimeChoices': "Ending Time From Now"}

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
        clean_items = cleaned_data.get('items')

        #Check to make sure user selected items
        if clean_items:
            pass
        else:
            raise ValidationError("You must select at least one item.")

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

    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(),
        help_text="An item is required.", widget=forms.CheckboxSelectMultiple)
    name = forms.CharField(max_length=50, required=True, help_text="Name for listing is required.")
    minRange = forms.DecimalField(max_digits=9, decimal_places=2, required=False,
        help_text="Minimum money offers you'll consider.")
    maxRange = forms.DecimalField(max_digits=9, decimal_places=2, required=False,
        help_text="Maximum money offers you'll consider (leave blank if you don't have a maximum).")
    description = forms.CharField(max_length=500, required=True,
        widget=forms.Textarea(attrs={'rows':5, 'cols':49}),
        help_text="A short description of what the listing obtains.")
    notes = forms.CharField(max_length=500, required=True,
        widget=forms.Textarea(attrs={'rows':5, 'cols':49}),
        help_text="Include here what offers you're seeking.")

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
        clean_items = cleaned_data.get('items')

        #Check to make sure user selected items
        if clean_items:
            pass
        else:
            raise ValidationError("You must select at least one item.")

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

    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(),
        help_text="An item is required.", widget=forms.CheckboxSelectMultiple)
    name = forms.CharField(max_length=50, required=True, help_text="Name for listing is required.")
    startingBid = forms.DecimalField(max_digits=9, decimal_places=2, required=True,
        help_text="Money amount bidding should start at for auction.",
        label="Starting Bid")
    minimumIncrement = forms.DecimalField(max_digits=9, decimal_places=2, required=True,
        help_text="Minimum increment bid that can be placed on the auction, that cannot be greater than the starting bid (maximum increment bid will be x3 this value).",
        label="Minimum Increment")
    autobuy = forms.DecimalField(max_digits=9, decimal_places=2, required=False,
        help_text="A bid greater than the starting bid that will automatically win the auction if placed. (Leave blank if not interested in having an autobuy price)")
    description = forms.CharField(max_length=500, required=True,
        widget=forms.Textarea(attrs={'rows':5, 'cols':49}),
        help_text="A short description of what the listing obtains.")

    class Meta:
        model = AuctionListing
        fields = ['name', 'description', 'items', 'endTimeChoices', 'startingBid',
            'minimumIncrement', 'autobuy']
        exclude = ['owner', 'endTime', 'listingEnded']
        labels = {'endTimeChoices': "Ending Time From Now"}

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
            raise forms.ValidationError("Listing has ended, no offers can be made.")
        else:
            if clean_amount:
                if clean_listing.openToMoneyOffers:
                    if (clean_amount < clean_listing.minRange) and clean_amount != 0.00:
                        #Check to see that the amount offered is not less than the listing's minimum range
                        raise forms.ValidationError("Amount offered is less than the minimum range of ${0}".format(clean_listing.minRange))
                    elif clean_listing.maxRange:
                        if clean_amount > clean_listing.maxRange:
                            #Check to see that the amount offered is not more than the listing's maximum range
                            raise forms.ValidationError("Amount offered is more than the maximum range of ${0}".format(clean_listing.maxRange))
                else:
                    raise forms.ValidationError("Listing is not accepting money offers.")
            else:
                clean_items = cleaned_data.get('items')
                if clean_items:
                    pass
                else:
                    raise forms.ValidationError("An item or money amount must be offered.")

        return

    offerListing = forms.ModelChoiceField(queryset=OfferListing.objects.all(), required=False,
        disabled=True, label="Offer Listing")
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(),
        help_text="Items are not required for an offer if user is open to money offers.",
        required=False, widget=forms.CheckboxSelectMultiple)
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
        required=False, widget=forms.CheckboxSelectMultiple)
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
                            highest_bid = current_bid.amount + (clean_listing.minimumIncrement * 3)
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

    auctionListing = forms.ModelChoiceField(queryset=AuctionListing.objects.all(),
        required=False, disabled=True, label="Auction Listing",
        widget=forms.Select(attrs={'style': 'width:250px'}))
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
    context = forms.CharField(max_length=250, required=True,
        widget=forms.Textarea(attrs={'rows':5, 'cols':49}),
        help_text=("What is the event for? What will happen/be accomplished?"))

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
                if user == clean_event.host:
                    raise ValidationError("You cannot invite yourself to your own event.")
                if user.invitesOpen == False:
                    raise ValidationError("User {0} is not accepting invitations to events.".format(user))
                elif Invitation.objects.filter(event=clean_event, recipient=user).exists():
                    raise ValidationError("User {0} already has an invitation to this event.".format(user))
            return
        else:
            raise ValidationError("At least one user must be selected to invite.")

    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), label="Users to Invite",
        help_text="Users You Would Like to Invite to Event.", widget=forms.CheckboxSelectMultiple)
    event = forms.ModelChoiceField(queryset=Event.objects.all(), required=False,
        disabled=True)

    #Set the queryset for users to only be ones that have not accepted an invite to event
    def __init__(self, *args, **kwargs):
       event = kwargs.pop('instance')
       super(InvitationForm, self).__init__(*args, **kwargs)

       #Exclude users already in event
       excluded_ids = [user.id for user in event.participants.all()]

       #Exclude users not within a 50m radius of event host
       if isinstance(event.host.profile.latitude, float):
           min_lat = Decimal.from_float(event.host.profile.latitude) - Decimal.from_float(0.8300)
           max_lat = Decimal.from_float(event.host.profile.latitude) + Decimal.from_float(0.8300)
           min_lon = Decimal.from_float(event.host.profile.longitude) - Decimal.from_float(0.8300)
           max_lon = Decimal.from_float(event.host.profile.longitude) + Decimal.from_float(0.8300)
       else:
           min_lat = event.host.profile.latitude - Decimal.from_float(0.8300)
           max_lat = event.host.profile.latitude + Decimal.from_float(0.8300)
           min_lon = event.host.profile.longitude - Decimal.from_float(0.8300)
           max_lon = event.host.profile.longitude + Decimal.from_float(0.8300)

       profiles = Profile.objects.filter(
           latitude__range=[min_lat, max_lat],
           longitude__range=[min_lon, max_lon],
       )

       existing_invites = Invitation.objects.filter(event=event)
       existing_recipient_ids = [invite.recipient.id for invite in existing_invites]
       for id in existing_recipient_ids:
           excluded_ids.append(id)
       not_accepting_invites_ids = [user.id for user in User.objects.all() if
           user.invitesOpen == False]
       for id in not_accepting_invites_ids:
           excluded_ids.append(id)
       excluded_ids.append(event.host.id)
       self.fields['users'].queryset = User.objects.filter(profile__in=profiles).exclude(id__in=excluded_ids)

#Form for a user to create a wishlist
class WishlistForm(ModelForm):

    title = forms.CharField(max_length=50, required=True, help_text="Title of Wishlist.")
    description = forms.CharField(max_length=250, required=True, help_text=("Description for Wishlist" +
        " (what it contains, how you want to accuire the items, etc.)"),
        widget=forms.Textarea(attrs={'rows':5, 'cols':49}))
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(),
        help_text="Items That You Are Seeking.", label="Wishlist Items",
        required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Wishlist
        fields = ['title', 'description', 'items']
        exclude = ['owner']

    #Initializes the items dropdown with items that only relate to the current user
    def __init__(self, *args, **kwargs):
       self.user = kwargs.pop('user')
       super(WishlistForm, self).__init__(*args, **kwargs)
       self.fields['items'].queryset = Item.objects.filter(owner=self.user)

#Form for a user to create a wishlist listing
class WishlistListingForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        clean_money_offer = cleaned_data.get('moneyOffer')
        clean_items_offer = cleaned_data.get('itemsOffer')
        clean_items = cleaned_data.get('items')

        #Check to make sure user selected at least one wishlist item
        if clean_items:
            pass
        else:
            raise forms.ValidationError("You must select at least one " +
                "withlist item.")

        #Check to ensure at least money or item(s) were included in listing
        if clean_money_offer or clean_items_offer:
            if clean_money_offer:
                #Check to ensure amount offered is not negative
                if clean_money_offer < 0.00:
                    raise forms.ValidationError("Monetary amount offered cannot be negative.")
        else:
            raise forms.ValidationError("At least a monetary amount or an item must" +
                " be offered in listing.")

        return

    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), required=True,
        help_text="At least one wishlist item must be selected.",
        label="Wishlist Items", widget=forms.CheckboxSelectMultiple)
    itemsOffer = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), required=False,
        help_text="Items you would exchange for wishlist items.",
        label="Items Being Offered", widget=forms.CheckboxSelectMultiple)
    moneyOffer = forms.DecimalField(max_digits=9, decimal_places=2, required=False,
        help_text="Monetary amount you would exchange for wishlist items.",
        label="Money Being Offered")
    name = forms.CharField(max_length=50, required=True, help_text="Name for listing is required.")
    notes = forms.CharField(max_length=500, required=True,
        widget=forms.Textarea(attrs={'rows':5, 'cols':49}),
        help_text=("Any extra info about the wishlist items and what" +
                "you're offering should go here"))

    class Meta:
        model = WishlistListing
        fields = ['name', 'items', 'endTimeChoices', 'moneyOffer', 'itemsOffer',
            'notes']
        exclude = ['owner', 'description', 'endTime', 'listingEnded']
        labels = {'endTimeChoices': "Ending Time From Now"}

    #Initializes the items dropdown with items that only relate to the current user
    def __init__(self, *args, **kwargs):
       self.user = kwargs.pop('user')
       super(WishlistListingForm, self).__init__(*args, **kwargs)
       wishlist = Wishlist.objects.get(owner=self.user)
       self.fields['items'].queryset = wishlist.items
       self.fields['itemsOffer'].queryset = Item.objects.filter(owner=self.user)

#Form for a user to edit a wishlist listing
class EditWishlistListingForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        clean_money_offer = cleaned_data.get('moneyOffer')
        clean_items_offer = cleaned_data.get('itemsOffer')
        clean_items = cleaned_data.get('items')

        #Check to make sure user selected at least one wishlist item
        if clean_items:
            pass
        else:
            raise forms.ValidationError("You must select at least one " +
                "withlist item.")

        #Check to ensure at least money or item(s) were included in listing
        if clean_money_offer or clean_items_offer:
            if clean_money_offer:
                #Check to ensure amount offered is not negative
                if clean_money_offer < 0.00:
                    raise forms.ValidationError("Monetary amount offered cannot be negative.")
        else:
            raise forms.ValidationError("At least a monetary amount or an item must" +
                " be offered in listing.")

        return

    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), required=True,
        help_text="At least one wishlist item must be selected.",
        label="Wishlist Items", widget=forms.CheckboxSelectMultiple)
    itemsOffer = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), required=False,
        help_text="Items you would exchange for wishlist items.",
        label="Items Being Offered", widget=forms.CheckboxSelectMultiple)
    moneyOffer = forms.DecimalField(max_digits=9, decimal_places=2, required=False,
        help_text="Monetary amount you would exchange for wishlist items.",
        label="Money Being Offered")
    name = forms.CharField(max_length=50, required=True, help_text="Name for listing is required.")
    notes = forms.CharField(max_length=500, required=True,
        widget=forms.Textarea(attrs={'rows':5, 'cols':49}),
        help_text=("Any extra info about the wishlist items and what" +
                "you're offering should go here"))

    class Meta:
        model = WishlistListing
        fields = ['name', 'items', 'moneyOffer', 'itemsOffer',
            'notes']
        exclude = ['owner', 'description', 'endTime', 'listingEnded',
            'endTimeChoices']
        labels = {'endTimeChoices': "Ending Time From Now"}

    #Initializes the items dropdown with items that only relate to the current user
    def __init__(self, *args, **kwargs):
       self.user = kwargs.pop('user')
       super(EditWishlistListingForm, self).__init__(*args, **kwargs)
       wishlist = Wishlist.objects.get(owner=self.user)
       self.fields['items'].queryset = wishlist.items
       self.fields['itemsOffer'].queryset = Item.objects.filter(owner=self.user)

#Form for a user to create a wishlist listing by selecting an item from wishlist
class QuickWishlistListingForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        clean_money_offer = cleaned_data.get('moneyOffer')
        clean_items_offer = cleaned_data.get('itemsOffer')
        clean_items = cleaned_data.get('items')

        #Check to ensure at least one wishlist item was included
        if clean_items:
            #add initial data if it exists
            if self.initial['items'] != None:
                cleaned_data['items'] = clean_items.union(self.initial['items'])
        else:
            #Check if items was initialized
            if self.initial['items'] != None:
                cleaned_data['items'] = self.initial['items']
            else:
                raise forms.ValidationError("At least one wishlist item must be selected.")

        #Check to ensure at least money or item(s) were included in listing
        if clean_money_offer or clean_items_offer:
            if clean_money_offer:
                #Check to ensure amount offered is not negative
                if clean_money_offer < 0.00:
                    raise forms.ValidationError("Monetary amount offered cannot be negative.")
        else:
            raise forms.ValidationError("At least a monetary amount or an item must" +
                " be offered in listing.")

        return cleaned_data

    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), required=False,
        help_text="At least one wishlist item must be selected.",
        label="Wishlist Items", widget=forms.CheckboxSelectMultiple)
    itemsOffer = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), required=False,
        help_text="Items you would exchange for wishlist items.",
        label="Items Being Offered", widget=forms.CheckboxSelectMultiple)
    moneyOffer = forms.DecimalField(max_digits=9, decimal_places=2, required=False,
        help_text="Monetary amount you would exchange for wishlist items.",
        label="Money Being Offered")
    name = forms.CharField(max_length=50, required=True, help_text="Name for listing is required.")
    notes = forms.CharField(max_length=500, required=True,
        widget=forms.Textarea(attrs={'rows':5, 'cols':49}),
        help_text=("Any extra info about the wishlist items and what" +
                "you're offering should go here"))

    class Meta:
        model = WishlistListing
        fields = ['name', 'items', 'endTimeChoices', 'moneyOffer', 'itemsOffer',
            'notes']
        exclude = ['owner', 'description', 'endTime', 'listingEnded']
        labels = {'endTimeChoices': "Ending Time From Now"}

    #Initializes the items dropdown with items that only relate to the current user
    def __init__(self, *args, **kwargs):
       self.user = kwargs.pop('user')
       super(QuickWishlistListingForm, self).__init__(*args, **kwargs)
       wishlist = Wishlist.objects.get(owner=self.user)
       self.fields['items'].queryset = wishlist.items
       self.fields['itemsOffer'].queryset = Item.objects.filter(owner=self.user)

#form for user to edit their profile
class ProfileForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        clean_delivery = cleaned_data.get('delivery')
        clean_delivery_address = cleaned_data.get('deliveryAddress')

        if clean_delivery == True:
            if clean_delivery_address:
                pass
            else:
                raise forms.ValidationError("A delivery address must be included.")
        else:
            return

    bio = forms.CharField(max_length=1000, required=True,
        help_text="A biography for your profile so others can know you better.",
        label="Biography", widget=forms.Textarea(attrs={'rows':5, 'cols':49}))
    deliveryAddress = forms.CharField(max_length=100, required=False,
        help_text=("Submit an delivery address that you pick up items from." +
            "  Required if delivery check box is checked."),
        label="Delivery Address")

    class Meta:
        model = Profile
        fields = ['bio', 'delivery', 'deliveryAddress']
        exclude = ['user', 'country', 'state', 'city', 'zipCode']
        help_texts = {'delivery': "Check this if you are able to deliver items."}
        labels = {'bio': "Biography"}

#Form for user to start a conversation
class ConversationForm(ModelForm):
    topic = forms.CharField(max_length=50, required=True,
        help_text="Topic of the conversation.")
    message = forms.CharField(max_length=250, required=True,
        help_text="Initiating message for the conversation.",
        widget=forms.Textarea(attrs={'rows':5, 'cols':46}))

    class Meta:
        model = Conversation
        fields = ['topic']
        exclude = ['sender', 'recipient']

#Form for user to create a message
class MessageForm(ModelForm):
    content = forms.CharField(max_length=250, required=True,
        widget=forms.Textarea(attrs={'rows':3, 'cols':45}))

    class Meta:
        model = Message
        fields = ['content']
        exclude = ['conversation', 'author', 'dateSent', 'unread']

#Form for a user to report a listing
class ListingReportForm(ModelForm):
    description = forms.CharField(max_length=250, required=True,
        widget=forms.Textarea(attrs={'rows':5, 'cols':49}),
        help_text=("Tell us more in depth about the reason for reporting"))

    class Meta:
        model = ListingReport
        fields = ['reason', 'description']
        exclude = ['dateMade', 'reportType', 'listing']

#Form for a user to report a event
class EventReportForm(ModelForm):
    description = forms.CharField(max_length=250, required=True,
        widget=forms.Textarea(attrs={'rows':5, 'cols':49}),
        help_text=("Tell us more in depth about the reason for reporting"))

    class Meta:
        model = EventReport
        fields = ['reason', 'description']
        exclude = ['dateMade', 'reportType', 'event']

#Form for a user to report a user
class UserReportForm(ModelForm):
    description = forms.CharField(max_length=250, required=True,
        widget=forms.Textarea(attrs={'rows':5, 'cols':49}),
        help_text=("Tell us more in depth about the reason for reporting"))

    class Meta:
        model = UserReport
        fields = ['reason', 'description']
        exclude = ['dateMade', 'reportType', 'user']

#Form for a user to report a wishlist
class WishlistReportForm(ModelForm):
    description = forms.CharField(max_length=250, required=True,
        widget=forms.Textarea(attrs={'rows':5, 'cols':49}),
        help_text=("Tell us more in depth about the reason for reporting"))

    class Meta:
        model = WishlistReport
        fields = ['reason', 'description']
        exclude = ['dateMade', 'reportType', 'user']

#Form for a user to report an image
class ImageReportForm(ModelForm):
    description = forms.CharField(max_length=250, required=True,
        widget=forms.Textarea(attrs={'rows':5, 'cols':49}),
        help_text=("Tell us more in depth about the reason for reporting"))

    class Meta:
        model = ImageReport
        fields = ['reason', 'description']
        exclude = ['dateMade', 'reportType', 'user']

#Form for a user to report a Rating
class RatingReportForm(ModelForm):
    description = forms.CharField(max_length=250, required=True,
        widget=forms.Textarea(attrs={'rows':5, 'cols':49}),
        help_text=("Tell us more in depth about the reason for reporting"))

    class Meta:
        model = RatingReport
        fields = ['reason', 'description']
        exclude = ['dateMade', 'reportType', 'user']

#Form for a user to rate a user and leave feedback
class CreateRatingForm(ModelForm):
    ratingTicket = forms.ModelChoiceField(queryset=RatingTicket.objects.all(),
        help_text="A listing to leave a rating on is required", required=True,
        label="Listing",
        widget=forms.Select(attrs={'style': 'width:300px'}))
    feedback = forms.CharField(max_length=500, required=False,
        widget=forms.Textarea(attrs={'rows':5, 'cols':63}),
        help_text="Leave feedback for the user you're rating.")

    class Meta:
        model = Rating
        fields = ['ratingTicket', 'ratingValue', 'feedback']
        exclude = ['profile', 'reviewer', 'listingName']
        labels = {'ratingValue': "Rating"}

    #Initializes the listing dropdown with listing they completed with the
    #user receiving the rating
    def __init__(self, *args, **kwargs):
       self.user = kwargs.pop('user')
       self.receiver = kwargs.pop('receiver')
       super(CreateRatingForm, self).__init__(*args, **kwargs)
       ticket_ids = [ticket.id for ticket in RatingTicket.objects.all() if
            (ticket.rater == self.user and ticket.receivingUser == self.receiver
            and ticket.listing.listingEnded)]
       self.fields['ratingTicket'].queryset = RatingTicket.objects.filter(
            id__in=ticket_ids)

#form for admin to delete an object from a report
class TakeActionOnReportForm(forms.Form):
    ACTION_CHOICES =(
        ("Delete", "Delete"),
        ("Take Manual Action", "Take Manual Action")
    )
    action_taken = forms.ChoiceField(choices=ACTION_CHOICES,
        help_text=("Action to preform on the object"),
        label="Action to Take", required=True)
    reason = forms.CharField(max_length=250, required=False,
        widget=forms.Textarea(attrs={'rows':5, 'cols':49}),
        help_text=("Reason for taking action on object."),
        label="Reason for Action")
