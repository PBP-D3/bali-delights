from django import forms
from products.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock", "category", "photo_upload", "photo_url"]
        
    def clean_photo_upload(self):
        photo_upload = self.cleaned_data.get('photo_upload')
        return photo_upload

    def clean_photo_url(self):
        photo_url = self.cleaned_data.get('photo_url')
        return photo_url
