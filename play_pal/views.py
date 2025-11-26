from django.shortcuts import render


def homepage(request):
    if not request.user.is_authenticated:
        template = 'play_pal/index.html'

    else:
        template = 'users/profile_form.html'
    return render(request, template_name=template)
