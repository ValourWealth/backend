# Generated by Django 5.1.1 on 2025-06-28 12:49

import VWBE.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlatformWalkthroughVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('video_file', models.FileField(blank=True, null=True, storage=VWBE.storage_backends.R2Storage(), upload_to='walkthrough_videos/')),
                ('manual_video_url', models.URLField(blank=True, null=True)),
                ('thumbnail_file', models.ImageField(blank=True, null=True, storage=VWBE.storage_backends.R2Storage(), upload_to='walkthrough_thumbnails/')),
                ('manual_thumbnail_url', models.URLField(blank=True, null=True)),
                ('author_name', models.CharField(default='Jack G', max_length=100)),
                ('author_role', models.CharField(default='ValourWealth Analyst', max_length=100)),
                ('author_image', models.URLField()),
                ('schedule_days', models.CharField(default='Monday to Friday', max_length=255)),
                ('schedule_time', models.CharField(default='7:00pm - 8:00pm EST', max_length=100)),
                ('is_verified', models.BooleanField(default=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
