from socket import fromshare
from django import forms
from .models import Place
from django.forms import FileInput, DateInput

class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields =('name', 'visited')

#defaults to text
class DateInput(forms.DateInput):
    input_type = 'date'  


class TripReviewForm(forms.ModelForm):
    class Meta:
        #describing metadata
        model = Place
        fields = ('notes', 'date_visited', 'photo')
        #creating a calendar widget 
        widgets = {
            'date_visited': DateInput()
        }
