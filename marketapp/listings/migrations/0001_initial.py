# Generated by Django 3.1 on 2020-08-25 16:31

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('paypalEmail', models.EmailField(help_text='E-mail that is connected to your PayPal account', max_length=100, unique=True, verbose_name='Paypal Email')),
                ('invitesOpen', models.BooleanField(default=True, help_text='Leave this field checked if you are interested in being invited to events.', verbose_name='Allow Invites for Events')),
                ('inquiriesOpen', models.BooleanField(default=True, help_text='Leave this field checked if you are interested in being contacted by users through your profile.  If unchecked, users will only be able to contact you after you accept their offer or bid or you contact them.', verbose_name='Allow Users to Contact You Through Profile')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='marketapp\\listings\\images')),
                ('name', models.TextField(max_length=50, verbose_name='Name of Image')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50, verbose_name='Item Name')),
                ('description', models.TextField(help_text='A brief description of the item in the image(s).', max_length=250)),
                ('images', models.ManyToManyField(to='listings.Image')),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100, verbose_name='Listing Name')),
                ('description', models.TextField(help_text='A short description of what the listing obtains.', max_length=500, verbose_name='Listing Description')),
                ('endTimeChoices', models.CharField(choices=[('1h', 'One Hours'), ('2h', 'Two Hours'), ('4h', 'Four Hours'), ('8h', 'Eight Hours'), ('12h', 'Twelve Hours'), ('1d', 'One Day'), ('3d', 'Three Days'), ('7d', 'Seven Days')], default='1h', max_length=3)),
                ('endTime', models.DateTimeField(blank=True)),
                ('listingEnded', models.BooleanField(default=False)),
                ('items', models.ManyToManyField(to='listings.Item')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, default='None', help_text='A biography for your profile so others can know you better.', max_length=1000, verbose_name='Biography')),
                ('country', models.TextField(default='None', max_length=50)),
                ('state', models.TextField(default='None', max_length=50)),
                ('city', models.TextField(default='None', max_length=50)),
                ('zipCode', models.TextField(default='None', max_length=10, verbose_name='Zip Code')),
                ('delivery', models.BooleanField(default=False, help_text='Check this if you are able to deliver items.')),
                ('deliveryAddress', models.TextField(default='None', help_text='Submit an delivery address that you pick up items from.', max_length=100, verbose_name='Delivery Address')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50, verbose_name='Tag Name')),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='listings.user')),
                ('superAdmin', models.BooleanField(default=False, help_text='Admin that is able to set, remove and configure other Admin accounts.', verbose_name='Super Admin')),
                ('handleListings', models.BooleanField(default=False, help_text='Admin is able to manage user listings.', verbose_name='Can Handle Listings')),
                ('handleEvents', models.BooleanField(default=False, help_text='Admin is able to manage user events.', verbose_name='Can Handle Events')),
                ('handleWishlists', models.BooleanField(default=False, help_text='Admin is able to manage user wishlists.', verbose_name='Can Handle Wishlists')),
                ('handleImages', models.BooleanField(default=False, help_text='Admin is able to manage user images.', verbose_name='Can Handle Images')),
                ('handleRatings', models.BooleanField(default=False, help_text='Admin is able to manage user ratings.', verbose_name='Can Handle Ratings')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('listings.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AuctionListing',
            fields=[
                ('listing_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='listings.listing')),
                ('startingBid', models.DecimalField(decimal_places=2, help_text='Money amount bidding should start at for auction.', max_digits=9, verbose_name='Starting Bid')),
                ('minimumIncrement', models.DecimalField(decimal_places=2, help_text='Minimum increment bid that can be placed on the auction, that cannot be greater than the starting bid (maximum increment bid will be x3 this value).', max_digits=9, verbose_name='Minimum Increment')),
                ('autobuy', models.DecimalField(decimal_places=2, default=None, help_text='If a user bids the amount you set in this field, the auction will close and they will win the auction.', max_digits=9)),
            ],
            bases=('listings.listing',),
        ),
        migrations.CreateModel(
            name='OfferListing',
            fields=[
                ('listing_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='listings.listing')),
                ('openToMoneyOffers', models.BooleanField(default=True, help_text="Leave this field unchecked if you're only interested in item offers.", verbose_name='Open to Money Offers?')),
                ('minRange', models.DecimalField(decimal_places=2, default=None, help_text="Minimum money offers you'll consider.", max_digits=9, verbose_name='Minimum Price Range')),
                ('maxRange', models.DecimalField(decimal_places=2, default=None, help_text="Maximum money offers you'll consider (leave blank if you don't have a maximum).", max_digits=9, verbose_name='Maximum Price Range')),
                ('notes', models.TextField(help_text="Include here what offers you're seeking.", max_length=500)),
            ],
            bases=('listings.listing',),
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=50)),
                ('description', models.TextField(help_text='A brief description of your wishlist and what it contains.', max_length=250)),
                ('items', models.ManyToManyField(to='listings.Item')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratingValue', models.IntegerField(default=1, help_text='Rating for user from 1 to 5, 5 being the best.', verbose_name='Rating')),
                ('feedback', models.TextField(help_text="Leave feedback for the user you're rating.", max_length=500)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='listings.profile')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reviewer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='None', max_length=500)),
                ('dateSent', models.DateTimeField(auto_now_add=True, verbose_name='Date Sent')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='tags',
            field=models.ManyToManyField(help_text='Qualities of the item in the photo, purpose and where one can find it can be used as tags.', to='listings.Tag', verbose_name='Item Tags'),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=50, verbose_name='Title of Event')),
                ('context', models.TextField(help_text='What is the event for?  What will happen/be accomplished?', max_length=250)),
                ('date', models.DateTimeField(verbose_name='Date and Time of Event')),
                ('location', models.TextField(max_length=100, verbose_name='Address where Event is Held')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='host', to=settings.AUTH_USER_MODEL)),
                ('participants', models.ManyToManyField(related_name='participants', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.TextField(help_text='Topic of the Conversation', max_length=100)),
                ('unread', models.BooleanField(default=True)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Warning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warningCount', models.IntegerField(verbose_name='Warning Count')),
                ('reason', models.TextField(help_text='Submit reasoning for why you warned this user.', max_length=250, verbose_name='Reason for Warning')),
                ('actionsTaken', models.TextField(help_text='What actions were made regarding this user?', max_length=500, verbose_name='Actions Taken')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='admin', to='listings.admin')),
            ],
        ),
    ]
