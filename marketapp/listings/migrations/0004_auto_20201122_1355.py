# Generated by Django 3.1 on 2020-11-22 18:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_auto_20201122_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='listingName',
            field=models.TextField(max_length=100, null=True, verbose_name='Listing Name'),
        ),
        migrations.CreateModel(
            name='RatingTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing')),
                ('rater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating_ticket', to=settings.AUTH_USER_MODEL)),
                ('receivingUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]