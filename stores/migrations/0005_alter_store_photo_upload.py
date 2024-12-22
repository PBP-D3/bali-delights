
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0004_alter_store_location_alter_store_photo_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='photo_upload',
            field=models.ImageField(blank=True, null=True, upload_to='store_images/'),
        ),
    ]
