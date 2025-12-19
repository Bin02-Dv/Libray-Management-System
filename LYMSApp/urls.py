from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("forget/", views.forget, name="forget"),
    path("catalog/", views.catalog, name="catalog"),
    
    # members section
    path("member/dash", views.member_dash, name="member-dash"),
    path("member/my-books", views.member_mooks, name="member-books")
]
