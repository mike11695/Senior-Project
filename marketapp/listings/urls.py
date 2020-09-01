from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('FAQ/', views.faq, name='faq'),
    path('FAQ/images', views.faq_images, name='faq-images'),
    path('FAQ/items', views.faq_items, name='faq-items'),
    path('images/', views.ImageListView.as_view(), name='images'),
    path('images/add', views.add_image, name='images-add'),
    path('images/<int:pk>', views.ImageDetailView.as_view(), name='image-detail'),
    path('items/', views.ItemListView.as_view(), name='items'),
    path('items/add', views.add_item, name='items-add'),
    path('items/<int:pk>', views.ItemDetailView.as_view(), name='item-detail'),
]
