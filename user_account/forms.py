from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from time import time
from django.contrib.auth import login, authenticate
from user_profile.models import UserProfile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        #raise forms.ValidationError(self.error_messages['duplicate_email'])
        raise forms.ValidationError('duplicate_email')

    def save(self, commit=True):        
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False # nije aktivan sve dok ne otvori aktivacijski link
            user.save()

        return user


