from django.urls import path
from . import views
from accounts import views as account_views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register', accounts_views.register_user, name="register"),
    path('login', accounts_views.login_user, name="login"),
    path('logout', accounts_views.logout_user, name="logout"),
]
