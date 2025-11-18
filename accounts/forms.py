from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


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
        fields = ['email', 'first_name', 'last_name']
        widgets = {
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

        # PASSWORD STRENGTH VALIDATION
        validate_password(password1, user=None)

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


# PROFILE MANAGEMENT FORM
class UserProfileForm(forms.ModelForm):
    # OPTIONAL PASSWORD FIELDS FOR CHANGING PASSWORD
    password1 = forms.CharField(
        label='New Password',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Enter new password'})
    )
    password2 = forms.CharField(
        label='Confirm New Password',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Confirm new password'})
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder': 'Enter your email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'Enter your last name'}),
        }

    # SAME AS IN REGISTER FORM
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                raise ValidationError("Passwords don't match")
            validate_password(password1, user=None)

        return password2

    def clean_email(self):
        # ENSURE E-MAIL IS UNIQUE, BUT ALLOW CURRENT USER TO KEEP THEIR E-MAIL
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def save(self, **kwargs):
        user = super().save(commit=False)

        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)

        user.save()
        return user
