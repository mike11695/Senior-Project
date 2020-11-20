from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),

    #Users
    path('profile/<int:pk>', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/<int:pk>/edit', views.edit_profile, name='edit-profile'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('users/<int:pk>/edit', views.edit_account, name='edit-account'),

    #FAQ
    path('FAQ/', views.faq, name='faq'),
    path('FAQ/images', views.faq_images, name='faq-images'),
    path('FAQ/items', views.faq_items, name='faq-items'),
    path('FAQ/listings', views.faq_listings, name='faq-listings'),
    path('FAQ/events', views.faq_events, name='faq-events'),
    path('FAQ/wishlists', views.faq_wishlists, name='faq-wishlists'),
    path('FAQ/profiles', views.faq_profiles, name='faq-profiles'),
    path('FAQ/accounts', views.faq_accounts, name='faq-accounts'),
    path('FAQ/conversations', views.faq_conversations, name='faq-conversations'),
    path('FAQ/receipts', views.faq_receipts, name='faq-receipts'),
    path('FAQ/favorites', views.faq_favorites, name='faq-favorites'),
    path('FAQ/search', views.faq_search, name='faq-search'),

    #Items
    path('images/', views.ImageListView.as_view(), name='images'),
    path('images/add', views.add_image, name='images-add'),
    path('images/<int:pk>', views.ImageDetailView.as_view(), name='image-detail'),
    path('images/<int:pk>/edit', views.ImageEditView.as_view(), name='edit-image'),
    path('images/<int:pk>/delete', views.ImageDeleteView.as_view(), name='delete-image'),

    #Items
    path('items/', views.ItemListView.as_view(), name='items'),
    path('items/add', views.add_item, name='items-add'),
    path('items/<int:pk>', views.ItemDetailView.as_view(), name='item-detail'),
    path('items/<int:pk>/edit', views.edit_item, name='edit-item'),
    path('items/<int:pk>/delete', views.ItemDeleteView.as_view(), name='delete-item'),

    #Offer Listings
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

    #Auction Listings
    path('auction-listings/', views.AuctionListingListView.as_view(), name='auction-listings'),
    path('auction-listings/all', views.AllAuctionListingsListView.as_view(), name='all-auction-listings'),
    path('auction-listings/my-bids', views.MyBidsListView.as_view(), name='my-bids'),
    path('auction-listings/create-auction-listing', views.create_auction_listing, name='create-auction-listing'),
    path('auction-listings/<int:pk>', views.AuctionListingDetailView.as_view(), name='auction-listing-detail'),
    path('auction-listings/<int:pk>/bid', views.create_bid, name='create-bid'),
    path('auction-listings/<int:pk>/relist', views.relist_auction_listing, name='relist-auction-listing'),
    path('auction-listings/<int:pk>/delete', views.AuctionListingDeleteView.as_view(), name='delete-auction-listing'),

    #Wishlists
    path('wishlists/create-wishlist', views.create_wishlist, name='create-wishlist'),
    path('wishlists/<int:pk>', views.WishlistDetailView.as_view(), name='wishlist-detail'),
    path('wishlists/<int:pk>/edit', views.edit_wishlist, name='edit-wishlist'),
    path('wishlists/<int:pk>/quick-add', views.quick_add_item_to_wishlist,
        name='quick-add-item-to-wishlist'),
    path('wishlists/<int:wishlist_pk>/remove-wishlist-item/<int:item_pk>',
        views.remove_wishlist_item, name='remove-wishlist-item'),
    path('wishlists/wishlist-listings', views.WishlistListingListView.as_view(), name='wishlist-listings'),
    path('wishlists/wishlist-listings/all', views.AllWishlistListingsListView.as_view(), name='all-wishlist-listings'),
    path('wishlists/wishlist-listings/<int:pk>', views.WishlistListingDetailView.as_view(),
        name='wishlist-listing-detail'),
    path('wishlists/wishlist-listings/create-wishlist-listing', views.create_wishlist_listing,
        name='create-wishlist-listing'),
    path('wishlists/wishlist-listings/<int:pk>/quick-wishlist-listing', views.quick_wishlist_listing,
        name='quick-wishlist-listing'),
    path('wishlists/wishlist-listings/<int:pk>/edit', views.edit_wishlist_listing,
        name='edit-wishlist-listing'),
    path('wishlists/wishlist-listings/<int:pk>/relist', views.relist_wishlist_listing,
        name='relist-wishlist-listing'),
    path('wishlists/wishlist-listings/<int:pk>/delete', views.WishlistListingDeleteView.as_view(),
        name='delete-wishlist-listing'),

    #Events
    path('events/', views.EventListView.as_view(), name='events'),
    path('events/create-event', views.create_event, name='create-event'),
    path('events/<int:pk>', views.EventDetailView.as_view(), name='event-detail'),
    path('events/<int:pk>/edit', views.edit_event, name='edit-event'),
    path('events/<int:pk>/create-invitations', views.create_invitations, name='create-invitations'),
    path('events/<int:pk>/delete', views.EventDeleteView.as_view(), name='delete-event'),
    path('events/<int:event_pk>/remove-participant/<int:user_pk>', views.remove_participant,
        name='remove-participant'),

    #Invitations
    path('invitations/', views.InvitationListView.as_view(), name='invitations'),
    path('invitations/<int:pk>/accept', views.accept_invitation, name='accept-invitation'),
    path('invitations/<int:pk>/decline', views.decline_invitation, name='decline-invitation'),

    #Conversations
    path('conversations/', views.ConversationListView.as_view(), name='conversations'),
    path('conversations/<int:pk>', views.ConversationDetailView.as_view(),
        name='conversation-detail'),
    path('conversations/<int:pk>/start-conversation', views.start_conversation,
        name='start-conversation'),
    path('conversations/<int:pk>/delete', views.ConversationDeleteView.as_view(),
        name='delete-conversation'),

    #Receipts
    path('receipts/', views.ReceiptListView.as_view(), name='receipts'),
    path('receipts/<int:pk>/send-payment', views.make_paypal_payment,
        name="send-payment"),
    path('receipts/create-payment-receipt', views.create_payment_receipt,
        name="create-payment-receipt"),
    path('receipts/<int:pk>/payment-made', views.paypal_payment_made,
        name="payment-made"),
    path('receipts/<int:pk>/delete', views.ReceiptDeleteView.as_view(),
        name='delete-receipt'),

    #Notifications
    path('notifications/', views.NotificationListView.as_view(), name='notifications'),
    path('notifications/delete', views.delete_notifications, name='delete-notifications'),

    #Favorites
    path('favorites/favorite-listing', views.favorite_listing,
        name="favorite-listing"),
    path('favorites/', views.FavoriteListView.as_view(),
        name="favorites"),

    #Search
    path('search-listings/', views.search_listings,
        name="search-listings"),

    #Reports
    path('report-listing/<int:pk>', views.report_listing,
        name="report-listing"),
]
