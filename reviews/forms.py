from django import forms
from .models import Review, Like

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment']