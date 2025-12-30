from django.shortcuts import render, redirect
from . import models
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

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
    current_user = models.Profile.objects.filter(user=request.user).first()
    total_books = models.Books.objects.all().count()
    total_books_formatted = f"{total_books:,}"
    
    total_members = models.AuthModel.objects.filter(role="member").count()
    total_members_formatted = f"{total_members:,}"
    
    context = {
        "current_user": current_user,
        "total_books": total_books_formatted,
        "total_members": total_members_formatted
    }
    return render(request, "Theadmin/dash.html", context)

@login_required(login_url='/login/')
def admin_manage_book(request):
    current_user = models.Profile.objects.filter(user=request.user).first()
    
    books = models.Books.objects.all().order_by("-id")
    
    if request.method == 'POST':
        title = request.POST.get("title")
        author = request.POST.get("author")
        ISBN = request.POST.get("ISBN")
        publisher = request.POST.get("publisher")
        category = request.POST.get("category")
        copies = request.POST.get("copies")
        cover_image = request.FILES.get("cover_image")
        
        models.Books.objects.create(
            title=title, author=author, ISBN=ISBN, pbulisher=publisher, category=category, copies=copies,
            cover_imge=cover_image
        )
        
        return JsonResponse({
            "message": "Book Added successfully..",
            "success": True
        })
    
    context = {
        "current_user": current_user,
        "books": books
    }
    return render(request, "Theadmin/manage-book.html", context)

@require_POST
def update_book_ajax(request):
    book_id = request.POST.get('book_id')
    book = get_object_or_404(models.Books, id=book_id)

    book.title = request.POST.get('title')
    book.author = request.POST.get('author')
    book.ISBN = request.POST.get('ISBN')
    book.pbulisher = request.POST.get('publisher')
    book.category = request.POST.get('category')
    book.copies = request.POST.get('copies')

    if 'cover_image' in request.FILES:
        book.cover_imge = request.FILES['cover_image']

    book.save()

    return JsonResponse({
        'success': True,
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'ISBN': book.ISBN,
        'publisher': book.pbulisher,
        'copies': book.copies,
        'cover_url': book.cover_imge.url if book.cover_imge else ''
    })

@login_required(login_url='/login/')
def admin_manage_members(request):
    current_user = models.Profile.objects.filter(user=request.user).first()
    
    members = models.Profile.objects.filter(user__role="member")
    
    
    if request.method == 'POST':
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        home_address = request.POST.get("home_address")
        
        if models.AuthModel.objects.filter(email=email).exists():
            return JsonResponse({
                "error": f"Sorry this email {email}, already exist!!",
                "success": False
            })
        elif confirm_password != password:
            return JsonResponse({
                "error": "Sorry you password and confirm password missed match!!",
                "success": False
            })
        
        else:
            new_member = models.AuthModel.objects.create_user(email=email, phone_number=phone_number, role="member", username=email)
            
            if full_name or home_address:
                models.Profile.objects.create(user=new_member, full_name=full_name, home_address=home_address)
            
            return JsonResponse({
                "message": "New Member added successfully..",
                "success": True
            })
    
    context = {
        "current_user": current_user,
        "members": members
    }
    return render(request, "Theadmin/manage-members.html", context)

@login_required(login_url='/login/')
def admin_circulation(request):
    current_user = models.Profile.objects.filter(user=request.user).first()
    
    context = {
        "current_user": current_user
    }
    return render(request, "Theadmin/circulation.html", context)

@login_required(login_url='/login/')
def admin_fines(request):
    current_user = models.Profile.objects.filter(user=request.user).first()
    
    context = {
        "current_user": current_user
    }
    return render(request, "Theadmin/fines.html")

@login_required(login_url='/login/')
def admin_report(request):
    current_user = models.Profile.objects.filter(user=request.user).first()
    
    context = {
        "current_user": current_user
    }
    return render(request, "Theadmin/reports.html")

@login_required(login_url='/login/')
def admin_settings(request):
    current_user = models.Profile.objects.filter(user=request.user).first()
    
    context = {
        "current_user": current_user
    }
    return render(request, "Theadmin/settings.html")

def page_404(request, exception):
    logger.warning("Page not found: %s", request.path)
    return render(request, "404.html", status=404)

def page_500(request):
    logger.exception("Internal Server Error (500)")
    return render(request, "500.html", status=500)