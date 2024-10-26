from django import forms
from .models import Review, Like

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 1}),
        }
