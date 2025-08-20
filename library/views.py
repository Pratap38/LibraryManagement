from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from .forms import LoginForm, StudentForm, BookForm
from .models import Book, Student, BorrowRecord

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

def user_login(request):
    """Handle login for both admin and student users."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_staff:
                return redirect("admin_dashboard")
            else:
                return redirect("student_dashboard")
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, "login.html")

def user_logout(request):
    """Logout user and redirect to login page."""
    logout(request)
    return redirect("login")


@login_required
def admin_dashboard(request):
    """Admin can see all students and books."""
    students = Student.objects.all()
    books = Book.objects.all()
    return render(request, "admin_dashboard.html", {"students": students, "books": books})

@login_required
def add_student(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        roll_number = request.POST.get("roll_number")
        course = request.POST.get("course")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please choose another.")
            return render(request, "add_student.html")

        # Create a Django user
        user = User.objects.create_user(username=username, password=password)

        # Create Student linked to that user
        Student.objects.create(
            user=user,
            roll_number=roll_number,
            course=course
        )

        messages.success(request, "Student added successfully!")
        return redirect("student_list")

    return render(request, "add_student.html")



@login_required
def add_book(request):
    """Admin can add a new book."""
    form = BookForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("admin_dashboard")
    return render(request, "add_book.html", {"form": form})


@login_required
def report(request):
    """Admin can view all borrow/return records."""
    records = BorrowRecord.objects.all()
    return render(request, "report.html", {"records": records})


@login_required
def student_dashboard(request):
    """Students can view available books and their borrow history."""
    student = get_object_or_404(Student, user=request.user)
    books = Book.objects.all()
    records = BorrowRecord.objects.filter(student=student)
    return render(request, "student_dashboard.html", {"books": books, "records": records})


@login_required
def borrow_book(request, book_id):
    """Student borrows a book (if available)."""
    student = get_object_or_404(Student, user=request.user)
    book = get_object_or_404(Book, id=book_id)

    already_borrowed = BorrowRecord.objects.filter(
        student=student, book=book, return_date__isnull=True
    ).exists()

    if book.available and not already_borrowed:
        BorrowRecord.objects.create(student=student, book=book)
        book.available = False
        book.save()

    return redirect("student_dashboard")


@login_required
def return_book(request, record_id):
    """Student returns a borrowed book."""
    student = get_object_or_404(Student, user=request.user)
    record = get_object_or_404(BorrowRecord, id=record_id, student=student)

    if not record.return_date:  # Only mark return if still borrowed
        record.return_date = timezone.now()
        record.book.available = True
        record.book.save()
        record.save()

    return redirect("student_dashboard")


@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, "student_list.html", {"students": students})
