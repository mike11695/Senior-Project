# Generated by Django 3.1 on 2020-09-02 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0006_auto_20200902_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='endTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]