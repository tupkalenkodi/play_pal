from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Profile

User = get_user_model()


class SignupForm(UserCreationForm):
    """
    Registration form - only email and password
    User will complete profile later
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email address',
            'autocomplete': 'email',
            'class': 'form-input'
        })
    )

    password1 = forms.CharField(
        required=True,
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'autocomplete': 'new-password',
            'class': 'form-input'
        })
    )

    password2 = forms.CharField(
        required=True,
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password',
            'autocomplete': 'new-password',
            'class': 'form-input'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email


class SigninForm(AuthenticationForm):
    """
    Login form - email and password
    """
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email address',
            'autocomplete': 'email',
            'class': 'form-input'
        }),
        label="Email"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password',
            'class': 'form-input'
        })
    )


class ProfileForm(forms.ModelForm):
    """
    Profile form - all personal information
    """

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'age']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Enter your first name',
                'class': 'form-input'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Enter your last name',
                'class': 'form-input'
            }),
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe yourself in a few words',
                'class': 'form-input'
            }),
            'age': forms.NumberInput(attrs={
                'placeholder': 'Enter your age',
                'min': 13,
                'max': 120,
                'class': 'form-input'
            }),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'bio': 'Bio',
            'age': 'Age'
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and (age < 13 or age > 120):
            raise ValidationError("Please enter a valid age between 13 and 120.")
        return age


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Custom password change form with styled fields
    """
    old_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your current password',
            'autocomplete': 'current-password',
            'class': 'form-input'
        })
    )

    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your new password',
            'autocomplete': 'new-password',
            'class': 'form-input'
        })
    )

    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your new password',
            'autocomplete': 'new-password',
            'class': 'form-input'
        })
    )
