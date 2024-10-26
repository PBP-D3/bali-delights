from django.db import models
# from stores.models import Store

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.CharField(max_length=100, blank=True, null=True)
    # photo = models.ImageField(upload_to='product_photos/', blank=True, null=True)
    # store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    store_id = models.IntegerField(blank=True, null=True) # temporary
    image_url = models.URLField(max_length=200, blank=True, null=True) #temporary
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
