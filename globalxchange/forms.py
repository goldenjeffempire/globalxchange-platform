from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order

# SignUpForm for user registration
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# OrderForm for placing orders
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'status', 'quantity']
