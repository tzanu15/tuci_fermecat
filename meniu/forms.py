from django import forms
from django.contrib.auth import get_user_model
from .models import Dish

User = get_user_model()

class DishForm(forms.ModelForm):
    """
    Form for adding a new dish (admin only).
    """
    class Meta:
        model = Dish
        fields = ('name', 'description', 'image')