from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, SigninForm, ProfileForm, CustomPasswordChangeForm


def signup_user(request):
    """
    Handle user registration
    After signup, redirect to profile completion
    """
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create user
            user = form.save()

            # Authenticate and login
            user = authenticate(
                request,
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )

            if user is not None:
                login(request, user)
                messages.success(request, 'Account created successfully! Please complete your profile.')
                return redirect('profile_form')  # Redirect to profile completion
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignupForm()

    return render(request, 'users/signup_form.html', {'form': form})


def signin_user(request):
    """
    Handle user login
    """
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        # AuthenticationForm requires request as first argument!
        form = SigninForm(request, data=request.POST)
        if form.is_valid():
            # Form already authenticated the user
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.email}!')

            # Redirect to 'next' parameter or homepage
            next_url = request.GET.get('next', 'homepage')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = SigninForm()

    return render(request, 'users/signin_form.html', {'form': form})


@login_required(login_url='signin_form')
def manage_profile(request):
    if request.method == 'POST' and request.POST.get('action') == 'signout':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('homepage')

    profile = request.user.profile  # Get user's profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_form')  # Redirect to avoid resubmission
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill form with existing data
        form = ProfileForm(instance=profile)

    return render(request, 'users/profile_form.html', {
        'form': form,
        'profile': profile
    })


@login_required(login_url='signin_form')
def change_password(request):
    """
    Handle password change for logged-in users
    """
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Important: Update session to prevent logout after password change
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('profile_form')  # Redirect to profile or wherever
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'users/change_password_form.html', {'form': form})
