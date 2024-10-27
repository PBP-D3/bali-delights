from django import forms
from .models import Store

class StoreForm(forms.ModelForm):
    CHOICES = [
        ('upload', 'Upload Image'),
        ('url', 'Image URL')
    ]
    
    choice = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="Choose Image Source")

    class Meta:
        model = Store
        fields = ['name', 'description', 'location', 'photo_upload', 'photo', 'choice']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter image URL'}),
            'photo_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        choice = cleaned_data.get("choice")
        photo_upload = cleaned_data.get("photo_upload")
        photo = cleaned_data.get("photo")
        
        return cleaned_data