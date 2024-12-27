from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import DashboardListView, DashboardDetailView

urlpatterns = [
    path("", views.index,name="index"),
    path("login", views.user_login,name="login"),
    path("signup", views.signup,name='signup'),
    path("logout", views.logouts,name='logout'),
    path("about", views.about_page,name='about'),
    path("next-steps", views.nextSteps,name='nextSteps'),
    path("dashboards", DashboardListView.as_view(), name='dashboards'),
    path("dashboards/<int:pk>/", views.DashboardDetailView.as_view(), name='dashboard-detail'),
]