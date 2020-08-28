from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('images/', views.ImageListView.as_view(), name='images'),
    path('images/add', views.add_image, name='images-add'),
    path('images/<int:pk>', views.ImageDetailView.as_view(), name='image-detail'),
]
