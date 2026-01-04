from django.shortcuts import render, redirect
from . import models
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from django.db import transaction
from django.db.models import Exists, OuterRef, Q
from django.utils import timezone
from datetime import timedelta

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
            new_member = models.AuthModel.objects.create_user(email=email, phone_number=phone_number, role="member")
            new_member.set_password(password)
            new_member.save()
            
            if full_name or home_address:
                models.Profile.objects.create(user=new_member, full_name=full_name, home_address=home_address)
            
            return JsonResponse({
                "message": "Registration completed successfully..",
                "success": True
            })
        
    return render(request, "signup.html")

def forget(request):
    return render(request, "forget.html")

def catalog(request):
    return render(request, "book-catalog.html")


# members section

@login_required(login_url='/login/')
def member_dash(request):
    current_user = request.user
    user_profile = models.Profile.objects.filter(user=current_user).first()
    
    context = {
        "profile": user_profile
    }
    return render(request, "members/dash.html", context)

@login_required(login_url='/login/')
def member_books(request):
    current_user = request.user
    user_profile = models.Profile.objects.filter(user=current_user).first()
    
    context = {
        "profile": user_profile
    }
    return render(request, "members/my-books.html", context)

@login_required(login_url='/login/')
def member_reserve_books(request):
    current_user = request.user
    user_profile = models.Profile.objects.filter(user=current_user).first()
    
    context = {
        "profile": user_profile
    }
    return render(request, "members/reserve-books.html", context)

@login_required(login_url='/login/')
def member_profile(request):
    current_user = request.user
    user_profile = models.Profile.objects.filter(user=current_user).first()
    
    context = {
        "profile": user_profile
    }
    return render(request, "members/profile.html", context)

@login_required(login_url='/login/')
def member_fines(request):
    current_user = request.user
    user_profile = models.Profile.objects.filter(user=current_user).first()
    
    context = {
        "profile": user_profile
    }
    return render(request, "members/fines.html", context)

@login_required(login_url='/login/')
def member_catalog(request):
    current_user = request.user
    user_profile = models.Profile.objects.filter(user=current_user).first()
    
    context = {
        "profile": user_profile
    }
    return render(request, "members/catalog.html", context)

@login_required
def search_books_ajax(request):
    q = request.GET.get('q', '')

    books = models.Books.objects.filter(
        Q(title__icontains=q) |
        Q(author__icontains=q) |
        Q(ISBN__icontains=q)
    ).distinct()

    results = []

    for book in books:
        active_issue = models.Issue.objects.filter(
            copy=OuterRef('pk'),
            returned_at__isnull=True
        )

        available_copy = models.BookCopy.objects.filter(
            book=book
        ).annotate(
            has_active_issue=Exists(active_issue)
        ).filter(
            has_active_issue=False
        ).first()

        results.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'available': bool(available_copy),
            'cover': book.cover_image.url if book.cover_image else ''
        })

    return JsonResponse({'results': results})

@login_required
def reserve_book_ajax(request):
    current_user = request.user
    user_profile = models.Profile.objects.filter(user=current_user).first()
    
    book_id = request.POST.get('book_id')
    
    active_issue = models.Issue.objects.filter(
        copy=OuterRef('pk'),
        returned_at__isnull=True
    )

    # Find a free copy
    free_copy = models.BookCopy.objects.filter(
        book_id=book_id
    ).annotate(
        has_active_issue=Exists(active_issue)
    ).filter(
        has_active_issue=False
    ).first()

    if not free_copy:
        return JsonResponse({
            'success': False,
            'message': 'No available copies'
        })

    models.Issue.objects.create(
        member=user_profile,
        copy=free_copy,
        issued_at=timezone.now().date(),
        due_at=timezone.now().date() + timedelta(days=14)
    )

    return JsonResponse({'success': True})

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
        copy_id = request.POST.get("copy_id")
        cover_image = request.FILES.get("cover_image")
        
        new_book = models.Books.objects.create(
            title=title, author=author, ISBN=ISBN, publisher=publisher, category=category, cover_image=cover_image
        )
        
        models.BookCopy.objects.create(
            book=new_book, copy_id=copy_id
        )
        
        return JsonResponse({
            "message": "Book Added successfully..",
            "success": True
        })
    
    context = {
        "current_user": current_user,
        "books": books,
    }
    return render(request, "Theadmin/manage-book.html", context)

@require_POST
def update_book_ajax(request):
    book_id = request.POST.get('book_id')
    book = get_object_or_404(models.Books, id=book_id)

    book.title = request.POST.get('title')
    book.author = request.POST.get('author')
    book.ISBN = request.POST.get('ISBN')
    book.publisher = request.POST.get('publisher')
    book.category = request.POST.get('category')

    if 'cover_image' in request.FILES:
        book.cover_image = request.FILES['cover_image']

    book.save()

    return JsonResponse({
        'success': True,
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'ISBN': book.ISBN,
        'publisher': book.publisher,
        'cover_url': book.cover_image.url if book.cover_image else ''
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
            new_member = models.AuthModel.objects.create_user(email=email, phone_number=phone_number, role="member")
            new_member.set_password(password)
            new_member.save()
            
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
    
    issues = models.Issue.objects.select_related(
        "member__user", "copy__book"
    ).order_by("-issued_at")
    
    context = {
        "current_user": current_user,
        "issues": issues
    }
    return render(request, "Theadmin/circulation.html", context)

@transaction.atomic
def issue_book(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    member_id = request.POST.get("member_id")
    identifier = request.POST.get("identifier")  # ISBN or Copy ID

    try:
        member = models.Profile.objects.get(id=member_id)
    except models.Profile.DoesNotExist:
        return JsonResponse({"error": "Invalid member"}, status=404)

    # Find copy
    copy = (
        models.BookCopy.objects
        .select_for_update()
        .filter(
            is_available=True
        )
        .filter(
            copy_id=identifier
        )
        .first()
    )

    if not copy:
        copy = (
            models.BookCopy.objects
            .select_for_update()
            .filter(
                is_available=True,
                book__ISBN=identifier
            )
            .first()
        )

    if not copy:
        return JsonResponse({"error": "No available copy"}, status=400)

    due_date = timezone.now().date() + timedelta(days=14)

    models.Issue.objects.create(
        member=member,
        copy=copy,
        due_at=due_date
    )

    copy.is_available = False
    copy.save()

    return JsonResponse({
        "message": "Book issued successfully",
        "due_date": due_date
    })


@transaction.atomic
def return_book(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    copy_id = request.POST.get("copy_id")

    try:
        issue = (
            models.Issue.objects
            .select_for_update()
            .get(copy__copy_id=copy_id, returned_at__isnull=True)
        )
    except models.Issue.DoesNotExist:
        return JsonResponse({"error": "Active issue not found"}, status=404)

    issue.returned_at = timezone.now().date()
    issue.save()

    issue.copy.is_available = True
    issue.copy.save()

    return JsonResponse({
        "message": "Book returned",
        "fine": issue.fine_amount
    })

@transaction.atomic
def renew_book(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    copy_id = request.POST.get("copy_id")

    try:
        issue = (
            models.Issue.objects
            .select_for_update()
            .get(copy__copy_id=copy_id, returned_at__isnull=True)
        )
    except models.Issue.DoesNotExist:
        return JsonResponse({"error": "Active issue not found"}, status=404)

    if issue.renewed_times >= issue.MAX_RENEWALS:
        return JsonResponse({"error": "Renewal limit reached"}, status=400)

    issue.due_at += timedelta(days=14)
    issue.renewed_times += 1
    issue.save()

    return JsonResponse({
        "message": "Book renewed",
        "new_due": issue.due_at
    })



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