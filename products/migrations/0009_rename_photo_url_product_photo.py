# Generated by Django 5.1.2 on 2024-10-31 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_rename_photo_product_photo_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='photo_url',
            new_name='photo',
        ),
    ]
