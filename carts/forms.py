from django import forms
from django.contrib.auth import authenticate
from django import forms
from django.utils.html import strip_tags
from .models import CartItem

class PasswordConfirmForm(forms.Form):
  password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

  def __init__(self, user, *args, **kwargs):
    self.user = user
    super().__init__(*args, **kwargs)

  def clean_password(self):
    password = self.cleaned_data.get("password")
    if not authenticate(username=self.user.username, password=password):
      raise forms.ValidationError("Incorrect password")
    return password

class CartItemUpdateForm(forms.Form):
  item_id = forms.CharField()
  quantity = forms.IntegerField(min_value=0)

  def clean_item_id(self):
    return strip_tags(self.cleaned_data["item_id"])

  def clean_quantity(self):
    return strip_tags(self.cleaned_data["quantity"])