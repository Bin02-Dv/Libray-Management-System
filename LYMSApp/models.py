from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.utils import timezone

# Create your models here.

class AuthModel(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=20)
    
    username = models.CharField(unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

class Profile(models.Model):
    user = models.ForeignKey(AuthModel, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=20)
    home_address = models.TextField()
    

class Books(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=20)
    ISBN = models.CharField(max_length=20)
    copies = models.IntegerField()
    pbulisher = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    cover_imge = CloudinaryField('LBRY/books', blank=True, null=True)

class BookCopy(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name="book_copies")
    copy_id = models.CharField(max_length=50, unique=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.book.title} - {self.copy_id}"

class Issue(models.Model):
    member = models.ForeignKey(Profile, on_delete=models.CASCADE)
    copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    issued_at = models.DateField(default=timezone.now)
    due_at = models.DateField()
    returned_at = models.DateField(null=True, blank=True)
    renewed_times = models.PositiveIntegerField(default=0)

    @property
    def status(self):
        return "Returned" if self.returned_at else "Active"
