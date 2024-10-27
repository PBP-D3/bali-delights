from django import forms
from products.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock", "category", "photo_upload", "photo"]
        
    def clean_photo_upload(self):
        photo_upload = self.cleaned_data.get('photo_upload')
        return photo_upload

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        return photo