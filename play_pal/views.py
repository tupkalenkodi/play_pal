from django.shortcuts import render
from django_user_agents.utils import get_user_agent


def homepage(request):
    user_agent = get_user_agent(request)
    context = {}

    # if request.user.is_authenticated:
    #     template_name = 'play_pal/logged/homepage.html'
    #
    #     if user_agent.is_mobile:
    #         layout_name = 'play_pal/logged/layout_mobile.html'
    #     else:
    #         layout_name = 'play_pal/logged/layout_desktop.html'
    # else:
    template_name = 'play_pal/unlogged/homepage.html'

    if user_agent.is_mobile:
        layout_name = 'play_pal/unlogged/layout_mobile.html'
    else:
        layout_name = 'play_pal/unlogged/layout_desktop.html'

    context['layout_name'] = layout_name

    return render(request, template_name, context)
