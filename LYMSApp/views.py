from django.shortcuts import render, redirect
from . import models
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

import logging

logger = logging.getLogger("django.request")

# Create your views here.

def index(request):
    return render(request, "index.html")

def logout(request):
    auth.logout(request)
    return redirect("/login/")

def login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = models.AuthModel.objects.filter(email=email).first()
        
        url = ""
        
        if user:
            
            if user.check_password(password):
                auth.login(request, user)
                
                if user.role == 'admin':
                    url = '/dash/'
                else:
                    url = '/member/dash/'
                    
                return JsonResponse({
                    "message": "Login Successfully...",
                    "success": True,
                    "url": url
                }, status=200)
            else:
                return JsonResponse({
                    "error": "Sorry your password is incorrect!!",
                    "success": False,
                }, status=200)
                
        elif not email or not password:
            return JsonResponse({
                "error": "Your email and passeord are required!!",
                "success": False
            }, status=200)
        
        else:
            return JsonResponse({
                "error": f"Sorry we couldn't find any account with this email - {email}",
                "success": False,
            }, status=400)
    return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")

def forget(request):
    return render(request, "forget.html")

def catalog(request):
    return render(request, "book-catalog.html")


# members section

@login_required(login_url='/login/')
def member_dash(request):
    return render(request, "members/dash.html")

@login_required(login_url='/login/')
def member_books(request):
    return render(request, "members/my-books.html")

@login_required(login_url='/login/')
def member_reserve_books(request):
    return render(request, "members/reserve-books.html")

@login_required(login_url='/login/')
def member_profile(request):
    return render(request, "members/profile.html")

@login_required(login_url='/login/')
def member_fines(request):
    return render(request, "members/fines.html")

@login_required(login_url='/login/')
def member_catalog(request):
    return render(request, "members/catalog.html")


# admin section

@login_required(login_url='/login/')
def admin_dash(request):
    return render(request, "Theadmin/dash.html")

@login_required(login_url='/login/')
def admin_manage_book(request):
    return render(request, "Theadmin/manage-book.html")

@login_required(login_url='/login/')
def admin_manage_members(request):
    return render(request, "Theadmin/manage-members.html")

@login_required(login_url='/login/')
def admin_circulation(request):
    return render(request, "Theadmin/circulation.html")

@login_required(login_url='/login/')
def admin_fines(request):
    return render(request, "Theadmin/fines.html")

@login_required(login_url='/login/')
def admin_report(request):
    return render(request, "Theadmin/reports.html")

@login_required(login_url='/login/')
def admin_settings(request):
    return render(request, "Theadmin/settings.html")

def page_404(request, exception):
    logger.warning("Page not found: %s", request.path)
    return render(request, "404.html", status=404)

def page_500(request):
    logger.exception("Internal Server Error (500)")
    return render(request, "500.html", status=500)