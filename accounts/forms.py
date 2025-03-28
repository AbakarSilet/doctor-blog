from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from .models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='Requis. Entrez une adresse email valide.'
    )
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'profile_image')


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'profile_image']

class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [ 'email','first_name', 'last_name', 'profile_image',]

    

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Adresse email",
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError("Aucun compte actif trouvé avec cette adresse email.")
        return email

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )