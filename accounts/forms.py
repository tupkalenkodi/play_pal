from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError


# REGISTER FORM
class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Enter Password'}, )
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'Choose a username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder': 'Enter your email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'Enter your last name'}),
        }

    def clean_password(self):
        # GET THE PASSWORDS FROM CLEANED DATA DICT PRODUCED BY DJANGO IF form.is_valid()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # CHECK IF ENTERED PASSWORD IS CORRECTLY REPEATED
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")

        return password1

    def clean_email(self):
        # GET THE E-MAIL FROM CLEANED DATA DICT PRODUCED BY DJANGO IF form.is_valid()
        email = self.cleaned_data.get('email')

        # IF A USER WITH THIS E-MAIL IS ALREADY REGISTERED
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")

        return email

    def save(self, **kwargs):
        # CREATE A USER, BUT DO NOT SAVE
        user = super().save(commit=False)
        # SET PASSWORD
        user.set_password(self.cleaned_data['password1'])
        # SAVE PREVIOUSLY CREATED USER
        user.save()
        return user


# LOGIN FORM
class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control',
                                       'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Enter your password'})
    )

    # IF THE USER WANTS TO STAY LOGGED IN
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

