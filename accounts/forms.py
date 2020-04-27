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

    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password1 = self.validated_data['password1']
        password2 = self.validated_data['password2']
        if password1 != password2:
            raise serializers.ValidationError({'password': 'password does not match'})
        user.set_password(password1)
        user.save()
        return user