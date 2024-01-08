from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from railway_staff.models import *

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class BookingForm(forms.Form):
    num_of_passengers = forms.IntegerField(min_value=1, label='Number of Passengers')


# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['train', 'departure_date', 'num_of_passengers']  # Update the fields based on your model
#         widgets = {
#             'train': forms.HiddenInput(),
#             'departure_date': forms.DateInput(attrs={'type': 'date', 'required': True}),
#             'num_of_passengers': forms.NumberInput(attrs={'min': 1, 'required': True}),
#             # Add more fields as needed for the booking information
#         }


class AddMoneyForm(forms.Form):
    amount_added = forms.IntegerField(min_value=0, label='Amount To Be Added')


class PassengerInformationForm(forms.ModelForm):
    class Meta:
        model = PassengerInformation
        fields = ['passenger_name', 'passenger_email']  # Update the fields based on your model
        widgets = {
            'passenger_name': forms.TextInput(attrs={'required': True}),
            'passenger_email': forms.EmailInput(attrs={'required': True}),
            # Add more fields for other passenger details as needed
        }