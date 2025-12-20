from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")

def forget(request):
    return render(request, "forget.html")

def catalog(request):
    return render(request, "book-catalog.html")


# members section

def member_dash(request):
    return render(request, "members/dash.html")

def member_books(request):
    return render(request, "members/my-books.html")

def member_reserve_books(request):
    return render(request, "members/reserve-books.html")

def member_profile(request):
    return render(request, "members/profile.html")

def member_fines(request):
    return render(request, "members/fines.html")

def member_catalog(request):
    return render(request, "members/catalog.html")


# admin section

def admin_dash(request):
    return render(request, "Theadmin/dash.html")

def admin_manage_book(request):
    return render(request, "Theadmin/manage-book.html")

def admin_manage_members(request):
    return render(request, "Theadmin/manage-members.html")

def admin_circulation(request):
    return render(request, "Theadmin/circulation.html")

def admin_fines(request):
    return render(request, "Theadmin/fines.html")

def admin_report(request):
    return render(request, "Theadmin/reports.html")

def admin_settings(request):
    return render(request, "Theadmin/settings.html")

def page_404(request, exception):
    return render(request, "404.html")

def page_500(request):
    return render(request, "500.html")