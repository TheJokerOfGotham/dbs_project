from django.contrib import admin
from django.urls import path
from mylibrary import views
from .views import register, login_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.entry, name="entry"),
    # path("register_member", views.register_member, name="register_member"),
    # spath("search", views.search_member, name='search_member'),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),

]
