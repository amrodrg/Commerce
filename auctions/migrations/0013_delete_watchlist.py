# Generated by Django 3.1 on 2020-10-11 23:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20201011_2304'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]