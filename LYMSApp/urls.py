from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("forget/", views.forget, name="forget"),
    path("catalog/", views.catalog, name="catalog"),
    
    # members section
    path("member/dash/", views.member_dash, name="member-dash"),
    path("member/my-books/", views.member_books, name="member-books"),
    path("member/reserve-book/", views.member_reserve_books, name="member-reserve-books"),
    path("member/profile/", views.member_profile, name="member-profile"),
    path("member/fines/", views.member_fines, name="member-fines"),
    path("member/catalog/", views.member_catalog, name="member-catalog"),
    
    # admin section
    path("dash/", views.admin_dash, name="dash"),
    path("manage-books/", views.admin_manage_book, name="manage-book"),
    path("manage-members/", views.admin_manage_members, name="manage-members"),
    path("circulation/", views.admin_circulation, name="circulation"),
    path("fines/", views.admin_fines, name="fines"),
    path("reports/", views.admin_report, name="reports"),
    path("settings/", views.admin_settings, name="settings"),
    path("404/", views.page_404, name="404"),
    path("500/", views.page_500, name="500")
]
