from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index,name="index"),
    path("login", views.user_login,name="login"),
    path("signup", views.signup,name='signup'),
    path("logout", views.logouts,name='logout'),
    path("about", views.about_page,name='about'),
    path("next-steps", views.nextSteps,name='nextSteps'),
]