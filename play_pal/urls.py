from django.urls import path
from . import views
from accounts import views as accounts_views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('faq', views.faq, name='faq'),
    path('developer', views.developer, name='developer'),
    path('signup', accounts_views.signup_user, name="signup"),
    path('signin', accounts_views.signin_user, name="signin"),
    path('signout', accounts_views.signout_user, name="signout"),
]
