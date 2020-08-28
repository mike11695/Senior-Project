from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from listings.models import Image
from listings.forms import SignUpForm, AddImageForm

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

class ImageListView(generic.ListView):
    model = Image
    context_object_name = 'images'
    template_name = 'images\images.html'

class ImageCreate(CreateView):
    model = Image
    fields = ['owner', 'image', 'name', 'tags']
    template_name = 'images\add_image.html'

    def form_valid(self, form):
        clean_image = form.cleaned_data.get('image')
        if clean_image:
            if clean_image._height > 2000 or clean_image._width > 2000:
                raise ValidationError("Height or Width is larger than limit allowed.")
            else:
                form.instance.owner = self.request.user
                return super(ImageCreate, self).form_valid(form)
        else:
            raise ValidationError("No image found")

def add_image(request):
    if request.method == 'POST':
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            clean_image = form.cleaned_data.get('image')
            clean_name = form.cleaned_data.get('name')
            clean_tags = form.cleaned_data.get('tags')
            owner = request.user
            obj = Image.objects.create(owner=owner, image=clean_image,
                name=clean_name, tags=clean_tags)
            return redirect('images')
            """clean_image = form.cleaned_data.get('image')
            if clean_image:
                if clean_image._height > 2000 or clean_image._width > 2000:
                    raise ValidationError("Height or Width is larger than limit allowed.")
                else:
                    clean_name = form.cleaned_data.get('name')
                    clean_tags = form.cleaned_data.get('tags')
                    owner = request.user
                    obj = Image.objects.create(owner=owner, image=clean_image,
                        name=clean_name, tags=clean_tags)
                    return redirect('images')
            else:
                raise ValidationError("No image found")"""
    else:
        form = AddImageForm()
    return render(request, 'images/add_image.html', {'form': form})
