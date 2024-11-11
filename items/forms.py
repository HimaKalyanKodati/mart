from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class ProductUploadForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'sell_price', 'mrp', 'description']

#inlineformset_factory is used to combine two forms
product_image_set = forms.inlineformset_factory(Product, ProductImage, fields=['image'], extra=1, can_delete=False)
        
