from django.shortcuts import render


def homepage(request):
    return render(request, 'play_pal/homepage.html')


def faq(request):
    return render(request, 'play_pal/faq.html')


def developer(request):
    return render(request, 'play_pal/developer.html')
