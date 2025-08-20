from django.contrib import admin
from .models import Student, Book, BorrowRecord


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'course')
    search_fields = ('user__username', 'roll_number', 'course')
    list_filter = ('course',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'available')
    search_fields = ('title', 'author')
    list_filter = ('available',)


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'borrow_date', 'return_date')
    search_fields = ('student__user__username', 'book__title')
    list_filter = ('borrow_date', 'return_date')
    date_hierarchy = 'borrow_date'
