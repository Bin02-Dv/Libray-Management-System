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
