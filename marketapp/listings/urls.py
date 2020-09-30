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
    path('images/<int:pk>/edit', views.ImageEditView.as_view(), name='edit-image'),
    path('images/<int:pk>/delete', views.ImageDeleteView.as_view(), name='delete-image'),
    path('items/', views.ItemListView.as_view(), name='items'),
    path('items/add', views.add_item, name='items-add'),
    path('items/<int:pk>', views.ItemDetailView.as_view(), name='item-detail'),
    path('items/<int:pk>/edit', views.edit_item, name='edit-item'),
    path('items/<int:pk>/delete', views.ItemDeleteView.as_view(), name='delete-item'),
    path('offer-listings/', views.OfferListingListView.as_view(), name='offer-listings'),
    path('offer-listings/all', views.AllOfferListingsListView.as_view(), name='all-offer-listings'),
    path('offer-listings/my-offers', views.MyOffersListView.as_view(), name='my-offers'),
    path('offer-listings/create-offer-listing', views.create_offer_listing, name='create-offer-listing'),
    path('offer-listings/<int:pk>', views.OfferListingDetailView.as_view(), name='offer-listing-detail'),
    path('offer-listings/<int:pk>/update', views.update_offer_listing, name='update-offer-listing'),
    path('offer-listings/<int:pk>/relist', views.relist_offer_listing, name='relist-offer-listing'),
    path('offer-listings/<int:pk>/offer', views.create_offer, name='create-offer'),
    path('offer-listings/<int:pk>/delete', views.OfferListingDeleteView.as_view(), name='delete-offer-listing'),
    path('offer-listings/offer/<int:pk>', views.OfferDetailView.as_view(), name='offer-detail'),
    path('offer-listings/offer/<int:pk>/accept', views.accept_offer, name='accept-offer'),
    path('offer-listings/offer/<int:pk>/edit', views.edit_offer, name='edit-offer'),
    path('offer-listings/offer/<int:pk>/delete', views.OfferDeleteView.as_view(), name='delete-offer'),
    path('auction-listings/', views.AuctionListingListView.as_view(), name='auction-listings'),
    path('auction-listings/all', views.AllAuctionListingsListView.as_view(), name='all-auction-listings'),
    path('auction-listings/my-bids', views.MyBidsListView.as_view(), name='my-bids'),
    path('auction-listings/create-auction-listing', views.create_auction_listing, name='create-auction-listing'),
    path('auction-listings/<int:pk>', views.AuctionListingDetailView.as_view(), name='auction-listing-detail'),
    path('auction-listings/<int:pk>/bid', views.create_bid, name='create-bid'),
    path('auction-listings/<int:pk>/relist', views.relist_auction_listing, name='relist-auction-listing'),
    path('auction-listings/<int:pk>/delete', views.AuctionListingDeleteView.as_view(), name='delete-auction-listing'),
    #path('wishlist/<int:pk>', views.WishlistDetailView.as_view(), name='wishlist-detail'),
    #path('wishlist/create-wishlist', views.create_wishlist, name='create-wishlist'),
    path('events/', views.EventListView.as_view(), name='events'),
    path('events/create-event', views.create_event, name='create-event'),
]
