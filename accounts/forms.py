from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

 
class LoginUpForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username', 'class' : 'form__control' }))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password' , 'class' : 'form__control'  }))
    

    class Meta:
        model = User
        fields = ('username' , 'password', )


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name' , 'class' : 'form__control'  }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name', 'class' : 'form__control' }))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username', 'class' : 'form__control' }))
    email = forms.EmailField(max_length=254, label='email', help_text='Required. Inform a valid email address.', widget= forms.TextInput
                           (attrs={'placeholder':'Email', 'type': 'email', 'class' : 'form__control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'input your password', 'class' : 'form__control' }))
    password2= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'confirm password', 'class' : 'form__control' }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name','username' , 'email', 'password1', 'password2', )

    def clean(self):
            data = self.cleaned_data
            if "password1" in data and "password2" in data:
                if data["password1"] != data["password2"]:
                    self._errors["password2"] = self.error_class(['Passwords do not match.'])
                    del data['password2']    
            return data
