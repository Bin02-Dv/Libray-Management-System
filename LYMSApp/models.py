from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.utils import timezone

# Create your models here.

class AuthModel(AbstractUser):
    username = None

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

class Profile(models.Model):
    user = models.ForeignKey(AuthModel, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=20)
    home_address = models.TextField()
    

class Books(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    ISBN = models.CharField(max_length=20, unique=True)
    publisher = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    cover_image = CloudinaryField('LBRY/books', blank=True, null=True)

    def available_copies(self):
        return self.book_copies.filter(is_available=True).count()
    
class BookCopy(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name="book_copies")
    copy_id = models.CharField(max_length=50, unique=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.book.title} ({self.copy_id})"

class Issue(models.Model):
    member = models.ForeignKey(Profile, on_delete=models.CASCADE)
    copy = models.ForeignKey(BookCopy, on_delete=models.PROTECT)

    issued_at = models.DateField(default=timezone.now)
    due_at = models.DateField()
    returned_at = models.DateField(null=True, blank=True)

    renewed_times = models.PositiveIntegerField(default=0)
    MAX_RENEWALS = 2

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["copy"],
                condition=models.Q(returned_at__isnull=True),
                name="one_active_issue_per_copy"
            )
        ]

    @property
    def status(self):
        return "Returned" if self.returned_at else "Active"

    @property
    def is_overdue(self):
        return not self.returned_at and timezone.now().date() > self.due_at

    @property
    def fine_amount(self):
        if not self.is_overdue:
            return 0
        days = (timezone.now().date() - self.due_at).days
        return days * 100  # example: ₦100 per day

