# Generated by Django 5.1.2 on 2024-10-31 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_remove_product_image_url_product_photo_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='photo',
            new_name='photo_url',
        ),
    ]
