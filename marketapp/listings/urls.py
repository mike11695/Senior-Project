from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('FAQ/', views.faq, name='faq'),
    path('FAQ/images', views.faq_images, name='faq-images'),
    path('FAQ/items', views.faq_items, name='faq-items'),
    path('FAQ/listings', views.faq_listings, name='faq-listings'),
    path('images/', views.ImageListView.as_view(), name='images'),
    path('images/add', views.add_image, name='images-add'),
    path('images/<int:pk>', views.ImageDetailView.as_view(), name='image-detail'),
    path('items/', views.ItemListView.as_view(), name='items'),
    path('items/add', views.add_item, name='items-add'),
    path('items/<int:pk>', views.ItemDetailView.as_view(), name='item-detail'),
    path('offer-listings/', views.OfferListingListView.as_view(), name='offer-listings'),
    path('offer-listings/create-offer-listing', views.create_offer_listing, name='create-offer-listing'),
    path('offer-listings/<int:pk>', views.OfferListingDetailView.as_view(), name='offer-listing-detail'),
    path('offer-listings/<int:pk>/update', views.update_offer_listing, name='update-offer-listing'),
    path('offer-listings/<int:pk>/offer', views.create_offer, name='create-offer'),
    path('offer-listings/offer/<int:pk>', views.OfferDetailView.as_view(), name='offer-detail'),
    path('auction-listings/', views.AuctionListingListView.as_view(), name='auction-listings'),
    path('auction-listings/create-auction-listing', views.create_auction_listing, name='create-auction-listing'),
    path('auction-listings/<int:pk>', views.AuctionListingDetailView.as_view(), name='auction-listing-detail'),
    path('auction-listings/<int:pk>/bid', views.create_bid, name='create-bid'),
]
