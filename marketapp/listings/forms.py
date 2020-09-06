from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from listings.models import User, Image, Tag, Item, Listing, OfferListing, AuctionListing
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=100, help_text='Enter a valid e-mail address')
    paypalEmail = forms.EmailField(max_length=100, label="Paypal Email",
        help_text='Enter a valid Paypal e-mail address')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'paypalEmail', 'password1', 'password2', )

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
        exclude = ['owner']
        help_texts = {'image': "Image must not be larger than 1250x1250."}

class AddItemForm(ModelForm):
    images = forms.ModelMultipleChoiceField(queryset=None, help_text="An image is required.")
    name = forms.CharField(max_length=50, required=True, help_text="Name for item is required.")

    class Meta:
        model = Item
        fields = ['images', 'name', 'description']
        exclude = ['owner']

    #Initializes the items dropdown with items that only relate to the current user
    def __init__(self, *args, **kwargs):
       self.user = kwargs.pop('user')
       super(AddItemForm, self).__init__(*args, **kwargs)
       self.fields['images'].queryset = Image.objects.filter(owner=self.user)

class CreateOfferListingForm(ModelForm):
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
        exclude = ['owner', 'endTime', 'listingEnded']

    #Initializes the items dropdown with items that only relate to the current user
    def __init__(self, *args, **kwargs):
       self.user = kwargs.pop('user')
       super(CreateOfferListingForm, self).__init__(*args, **kwargs)
       self.fields['items'].queryset = Item.objects.filter(owner=self.user)

class CreateAuctionListingForm(ModelForm):
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
       super(CreateAuctionListingForm, self).__init__(*args, **kwargs)
       self.fields['items'].queryset = Item.objects.filter(owner=self.user)
