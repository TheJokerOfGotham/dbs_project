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
    path("lib_login/", views.lib_login, name="lib_login"),
    path("lib_dashboard/", views.lib_dashboard, name="lib_dashboard"),
    path("lib_logout/", LogoutView.as_view(next_page="lib_login"), name="lib_logout"),
    path("add_book/", views.add_book, name="add_book"),
    path('borrow/', views.borrow_books_page, name='borrow_books'),
    path('borrow/<str:isbn>/', views.borrow_book, name='borrow_book'),
    path('return/', views.return_books_page, name='return_books_page'),
    path('return/<int:transaction_id>/', views.return_book, name='return_book'),
    path('view_reports/', views.view_reports, name='view_reports'),
    path('pay_penalties/', views.pay_penalties, name='pay_penalties'),




]
