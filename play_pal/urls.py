from django.urls import path
from . import views
from accounts import views as accounts_views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('signup', accounts_views.register_user, name="signup"),
    path('login', accounts_views.login_user, name="login"),
    path('logout', accounts_views.logout_user, name="logout"),
]
