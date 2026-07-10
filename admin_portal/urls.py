from django.urls import path
from . import views

urlpatterns = [

    path(
    "",
    views.admin_home,
    name="admin_home"
    ),

    path(
        "login/",
        views.admin_login,
        name="admin_login"
    ),

    path(
        "dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "students/",
        views.manage_students,
        name="manage_students"
    ),

    path(
    "students/<int:student_id>/",
    views.student_details,
    name="student_details"
    ),

    path(
    "lecturers/",
    views.manage_lecturers,
    name="manage_lecturers"
    ),

    path(
    "courses/",
    views.manage_courses,
    name="manage_courses"
    ),

    path(
    "feedback/",
    views.manage_feedback,
    name="manage_feedback"
    ),

    path(
    "complaints/",
    views.manage_complaints,
    name="manage_complaints"
    ),

    path(
    "reports/",
    views.reports,
    name="reports"
    ),


]