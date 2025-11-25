from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm
from .models import Profile


def signup_user(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            user = authenticate(
                request,
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )

            if user is not None:
                login(request, user)
                return redirect('homepage')
    else:
        form = SignupForm()

    return render(request, 'users/signup.html',
                  {'form': form})


def signin_user(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['email'],
            password=request.POST['password']
        )

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            error_message = "Invalid login credentials"
            return render(request, 'users/signin.html', {
                'error_message': error_message,
                'flag': True
            })

    return render(request,
                  'users/signin.html')


def signout_user(request):
    logout(request)
    return redirect('homepage')
