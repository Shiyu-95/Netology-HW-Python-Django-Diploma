# Generated by Django 4.2.20 on 2025-05-03 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_social_network', '0006_like_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.AddField(
            model_name='postimage',
            name='image',
            field=models.ImageField(null=True, upload_to='post_images'),
        ),
    ]
