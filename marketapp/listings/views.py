from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from listings.models import Image, Item
from listings.forms import SignUpForm, AddImageForm, AddItemForm

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
