
from django import forms

class ProductSearchForm(forms.Form):
    query = forms.CharField(
        label='Search for products',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter product name...'})
    )