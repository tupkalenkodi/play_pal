from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm


def register_user(request):
    form = UserRegistrationForm
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            user = authenticate(request, email=request.POST['email'], password=request.POST['password1'])

            if user is not None:
                login(request, user)
                return redirect('homepage')

    return render(request, 'register/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            error_message = "Invalid login credentials"
            flag = True
            return render(request, 'register/login.html', {'error_message': error_message, 'flag': flag})

    return render(request, 'register/login.html')


def logout_user(request):
    logout(request)
    return redirect('homepage')
