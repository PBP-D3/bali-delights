from django import forms
from products.models import Product

class ProductForm(forms.ModelForm):
    image_file = forms.ImageField(required=False)  

    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock", "category", "image_url", "image_file"]