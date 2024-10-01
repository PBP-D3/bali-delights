from django.forms import ModelForm
from main.models import ShopEntry

class ShopEntryForm(ModelForm):
    class Meta:
        model = ShopEntry
        fields = ["name", "price", "description", "sold", "rating"]