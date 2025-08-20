from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("add-student/", views.add_student, name="add_student"),
    path("add-book/", views.add_book, name="add_book"),
    path("report/", views.report, name="report"),
    path("student-dashboard/", views.student_dashboard, name="student_dashboard"),
    path("borrow/<int:book_id>/", views.borrow_book, name="borrow_book"),
    path("return/<int:record_id>/", views.return_book, name="return_book"),
]
