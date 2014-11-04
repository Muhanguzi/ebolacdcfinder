from django import forms
from django.forms import ModelForm, Textarea
from models import *

class ServicesForm(forms.Form):
    
    country = forms.CharField(max_length= 100)
    city = forms.CharField(max_length= 100)
    roadAddress = forms.CharField(max_length=250)
    centerName = forms.CharField(max_length = 100)
    telephone = forms.CharField(max_length= 100)
    coordinates = forms.CharField(max_length=200, required=True)
  

    def clean(self):
        cleaned_data = self.cleaned_data

        coordinates = cleaned_data.get("coordinates")
        city = cleaned_data.get("city")
        roadAddress = cleaned_data.get("roadAddress")
        centerName = cleaned_data.get("centerName")
        telephone = cleaned_data.get("telephone")

        return cleaned_data

class AbuseForm(forms.Form):

    
    description = forms.CharField(widget = forms.Textarea(attrs={'rows': 10, 'cols': 45}))

    def clean(self):

        cleaned_data = self.cleaned_data

        
        description = cleaned_data.get("description")
       

    