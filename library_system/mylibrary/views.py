from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import UserRegistrationForm, MemberForm
from .models import Member, Librarian, Book, Manages, Transaction, Penalty, Report
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import BookForm
from datetime import timedelta, date
from django.utils.timezone import now






# Create your views here.

def entry(request):
    return render(request, "entry.html")


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        member_form = MemberForm(request.POST)

        if user_form.is_valid() and member_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            member = member_form.save(commit=False)
            member.user = user  # Link Member with User
            member.email = user.email  # Sync email
            member.save()

            
            return redirect('login')  # Redirect after registration

    else:
        user_form = UserRegistrationForm()
        member_form = MemberForm()

    return render(request, "register.html", {"user_form": user_form, "member_form": member_form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")  # Redirect after login
    else:
        form = AuthenticationForm()
    
    return render(request, "login.html", {"form": form})

@login_required
def dashboard(request):
    member = request.user.member  # Get the Member object for the logged-in user
    response = render(request, "dashboard.html", {"member": member})
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response


def logout_view(request):
    logout(request)  # Logs out the user
    return redirect("login")  # Redirect to login page


def lib_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # Ensure only librarians can log in
            if hasattr(user, 'librarian'):  
                login(request, user)
                return redirect("lib_dashboard")
            else:
                form.add_error(None, "You are not authorized to access this system.")

    else:
        form = AuthenticationForm()

    return render(request, "lib_login.html", {"form": form})

@login_required
def lib_dashboard(request):
    if not hasattr(request.user, 'librarian'):
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    librarian = request.user.librarian  # Get librarian details
    response = render(request, "lib_dashboard.html", {"librarian": librarian})
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response
    

def lib_logout(request):
    logout(request)
    return redirect("lib_login")


@login_required
def add_book(request):
    if not hasattr(request.user, 'librarian'):
        return HttpResponseForbidden("You are not authorized to access this page.")

    librarian = request.user.librarian  # Get the logged-in librarian

    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)  # Don't save yet
            book.available_copies = book.total_copies  # Auto-set available copies
            book.save()  # Now save the book

            # Add an entry in the Manages table
            Manages.objects.create(librarian=librarian, book=book)

            return redirect("lib_dashboard")

    else:
        form = BookForm()

    return render(request, "add_book.html", {"form": form})



@login_required
def borrow_book(request, isbn):
    # Ensure user is a member
    if not hasattr(request.user, 'member'):
        return HttpResponseForbidden("You are not authorized to borrow books.")

    member = request.user.member  # Get the logged-in member
    book = get_object_or_404(Book, isbn=isbn)  # Get the selected book

    if book.available_copies > 0:  # Ensure book is available
        # Calculate due date (e.g., 14 days from today)
        due_date = date.today() + timedelta(days=14)

        # Create a transaction record
        Transaction.objects.create(
            member=member,
            book=book,
            due_date=due_date
        )

        # Reduce available copies
        book.available_copies -= 1
        book.save()

        return redirect("dashboard")  # Redirect to the dashboard
    else:
        return HttpResponseForbidden("This book is currently unavailable.")
    

def search_books(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    books = Book.objects.filter(title__icontains=query) if query else Book.objects.all()

    return render(request, 'search_books.html', {'books': books, 'query': query})

@login_required
def borrow_books_page(request):
    query = request.GET.get('q', '')  # Get search query from the URL
    books = Book.objects.filter(title__icontains=query) if query else Book.objects.all()
    return render(request, "borrow_books.html", {"books": books, "query": query})

@login_required
def return_books_page(request):
    """ Show all books currently borrowed by the logged-in user """
    member = request.user.member  # Get the logged-in member
    transactions = Transaction.objects.filter(member=member, return_date__isnull=True)  # Get active borrowings
    
    return render(request, "return_books.html", {"transactions": transactions})


@login_required
def return_book(request, transaction_id):
    """ Process returning a book """
    # Use the correct field name, which is transaction_id
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id)

    # Ensure the logged-in user is returning their own book
    if request.user.member != transaction.member:
        return HttpResponseForbidden("You are not authorized to return this book.")

    # Set the return date
    transaction.return_date = now().date()

    # Check for overdue penalty
    if transaction.return_date > transaction.due_date:
        overdue_days = (transaction.return_date - transaction.due_date).days
        penalty_amount = overdue_days * 10  # ₹10 per day fine
        transaction.overdue_fee = penalty_amount

        # Create or update the penalty record with member info
        Penalty.objects.create(transaction=transaction, member=transaction.member, amount=penalty_amount)

    transaction.save()

    # Increase the available copies count
    book = transaction.book
    book.available_copies += 1
    book.save()

    return redirect("return_books_page")
    
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from django.shortcuts import redirect
from .models import Transaction, Penalty, Book

@login_required
def return_book(request, transaction_id):
    """ Process returning a book """
    # Get the transaction object by its ID
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id)

    # Ensure the logged-in user is returning their own book
    if request.user.member != transaction.member:
        return HttpResponseForbidden("You are not authorized to return this book.")

    # Set the return date
    transaction.return_date = now().date()

    # Check for overdue penalty
    if transaction.return_date > transaction.due_date:
        overdue_days = (transaction.return_date - transaction.due_date).days
        penalty_amount = overdue_days * 10  # ₹10 per day fine
        transaction.overdue_fee = penalty_amount

        # Create or update the penalty record
        # Note: No need to pass 'member' directly, as it's already linked through the transaction
        Penalty.objects.create(transaction=transaction, amount=penalty_amount)

    # Save the updated transaction
    transaction.save()

    # Update available copies of the book
    book = transaction.book
    book.available_copies += 1
    book.save()

    return redirect("return_books_page")  # Redirect to the appropriate page after returning the book

@login_required
def view_reports(request):
    user_member = request.user.member  # Get the logged-in member
    report_type = request.GET.get('report_type', 'borrowed')  # Default to 'borrowed' if not specified

    if report_type == 'borrowed':
        transactions = Transaction.objects.filter(member=user_member, return_date__isnull=True)  # Borrowed books
    elif report_type == 'returned':
        transactions = Transaction.objects.filter(member=user_member).exclude(return_date__isnull=True)  # Returned books
    elif report_type == 'overdue':
        # Overdue books: those that have passed the due date but not returned yet
        transactions = Transaction.objects.filter(member=user_member, return_date__isnull=True, due_date__lt=date.today())
    else:
        transactions = []

    # Prepare report details
    report_details = ""
    for transaction in transactions:
        penalty = 0
        if transaction.return_date and transaction.return_date > transaction.due_date:
            overdue_days = (transaction.return_date - transaction.due_date).days
            penalty = overdue_days * 10  # ₹10 per day fine (change the logic as needed)

        report_details += f"Book: {transaction.book.title}, Borrow Date: {transaction.borrow_date}, Due Date: {transaction.due_date}, Return Date: {transaction.return_date}, Penalty: ₹{penalty}\n\n"

    # Create the report entry in the Report table
    report = Report.objects.create(
        report_type=report_type,
        details=report_details
    )

    return render(request, 'view_reports.html', {'report': report, 'report_type': report_type})


@login_required
def pay_penalties(request):
    # Get the logged-in user's penalties via their transactions
    member = request.user.member
    penalties = Penalty.objects.filter(transaction__member=member, paid_status=False)

    if request.method == "POST":
        # Process the payment (this could be an actual payment process or just mark it as paid)
        penalty_ids = request.POST.getlist('penalties')  # List of selected penalties to pay
        for penalty_id in penalty_ids:
            penalty = get_object_or_404(Penalty, penalty_id=penalty_id, transaction__member=member, paid_status=False)
            penalty.paid_status = True
            penalty.save()

        return redirect("pay_penalties")  # Redirect to the same page or to a success page

    return render(request, "pay_penalties.html", {"penalties": penalties})



