from django.shortcuts import render


def index(request):
    return render(request, 'play_pal/index.html')
