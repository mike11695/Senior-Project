# Generated by Django 3.1 on 2020-11-20 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='reportType',
            field=models.TextField(max_length=50, null=True),
        ),
    ]
