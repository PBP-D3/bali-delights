from django import forms
from products.models import Product

class ProductForm(forms.ModelForm):
<<<<<<< HEAD
    image_file = forms.ImageField(required=False)  

    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock", "category", "image_url", "image_file"]
=======
    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock", "category", "photo_upload", "photo_url"]
        
    def clean_photo_upload(self):
        photo_upload = self.cleaned_data.get('photo_upload')
        return photo_upload

    def clean_photo_url(self):
        photo_url = self.cleaned_data.get('photo_url')
        return photo_url
>>>>>>> 96142267eefa9f39795c370ba55897f89fbaa7c9
