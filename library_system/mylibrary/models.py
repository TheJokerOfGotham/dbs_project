from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Book(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True)  # ISBN as PK
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    published_year = models.IntegerField()
    total_copies = models.IntegerField()
    available_copies = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author}"
    

class Librarian(models.Model):
    librarian_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    membership_date = models.DateField()

    def __str__(self):
        return self.name

# Members Model
class Member(models.Model):
    membership_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    membership_date = models.DateField()

    def __str__(self):
        return self.name


# Manages (Many-to-Many Relationship between Librarian and Book)
class Manages(models.Model):
    librarian = models.ForeignKey(Librarian, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    assigned_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('librarian', 'book')

    def __str__(self):
        return f"{self.librarian.name} manages {self.book.title}"

# Transaction Model (Borrowing)
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    overdue_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.member.name} borrowed {self.book.title}"

# Penalty Model (Imposes)
class Penalty(models.Model):
    penalty_id = models.AutoField(primary_key=True)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    paid_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Penalty {self.penalty_id} - {self.transaction.member.name}"

class Report(models.Model):
    REPORT_TYPES = [
        ('borrowed', 'Borrowed Books'),
        ('overdue', 'Overdue Books'),
        ('returned', 'Returned Books'),
    ]

    report_id = models.AutoField(primary_key=True)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    generated_at = models.DateTimeField(auto_now_add=True)
    details = models.TextField()  # Stores formatted report details

    def __str__(self):
        return f"Report {self.report_id} - {self.get_report_type_display()}"
