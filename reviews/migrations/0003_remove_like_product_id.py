# Generated by Django 5.1.2 on 2024-10-26 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_review_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='product_id',
        ),
    ]