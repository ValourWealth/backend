# Generated by Django 5.1.1 on 2025-07-14 04:29

import VWBE.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_nftbadge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nftbadge',
            name='image',
            field=models.ImageField(storage=VWBE.storage_backends.R2Storage(), upload_to='nfts/'),
        ),
    ]
