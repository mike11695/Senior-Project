# Generated by Django 3.1 on 2020-12-04 17:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_report_actiontaken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='reviewer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewer', to=settings.AUTH_USER_MODEL),
        ),
    ]
