# Generated by Django 3.1 on 2020-09-11 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0011_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='listingEnded',
        ),
    ]
